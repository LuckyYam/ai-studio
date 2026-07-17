from __future__ import annotations
import json
from datetime import datetime
from typing import Any, cast
import mysql.connector
from mysql.connector import pooling
from core.models import IAttachment, IConversation, IMessageDB, ISavedData, ISavedSession, ISerializedContent, ISessionMessage, ISource, ITodayMessagesCount, IUser


class Database:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306, pool_size: int = 5) -> None:
        self._pool = pooling.MySQLConnectionPool(pool_name='ai_studio_pool', pool_size=pool_size, host=host, port=port, user=user, password=password, database=database, autocommit=False)

    def _connect(self) -> mysql.connector.pooling.PooledMySQLConnection:
        conn = self._pool.get_connection()
        try:
            conn.ping(reconnect=True, attempts=2, delay=1)
        except mysql.connector.Error:
            try:
                conn.close()
            except mysql.connector.Error:
                pass
            conn = self._pool.get_connection()
            conn.ping(reconnect=True, attempts=2, delay=1)
        return conn

    def _query(self, sql: str, params: tuple = (), fetchone: bool = False):
        try:
            conn = self._connect()
        except mysql.connector.Error as err:
            raise RuntimeError('Could not connect to the database.') from err
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params)
            result = cursor.fetchone() if fetchone else cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            raise RuntimeError(f'Database query failed: {err}') from err
        finally:
            conn.close()

    def _execute(self, sql: str, params: tuple = (), return_lastrowid: bool = False):
        try:
            conn = self._connect()
        except mysql.connector.Error as err:
            raise RuntimeError('Could not connect to the database.') from err
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            lastrowid = cursor.lastrowid
            cursor.close()
            return lastrowid if return_lastrowid else None
        except mysql.connector.IntegrityError:
            conn.rollback()
            raise
        except mysql.connector.Error as err:
            conn.rollback()
            raise RuntimeError(f'Database write failed: {err}') from err
        finally:
            conn.close()

    @staticmethod
    def _dump_json(value: Any) -> str | None:
        return json.dumps(value) if value is not None else None

    @staticmethod
    def _raw_parts_from_json(value: Any) -> list[ISerializedContent] | None:
        if value is None:
            return None
        return json.loads(value) if isinstance(value, str) else value

    def get_user_by_id(self, id: int) -> IUser | None:
        return self._query('SELECT * FROM users WHERE id = %s', (str(id),), fetchone=True)

    def get_user_by_email(self, email: str) -> IUser | None:
        return self._query('SELECT id, full_name, email, password_hash, is_active, email_verified_at FROM users WHERE email = %s', (email,), fetchone=True)

    def touch_last_login(self, user_id: int) -> None:
        self._execute('UPDATE users SET last_login_at = %s WHERE id = %s', (datetime.now(), user_id))

    def mark_email_verified(self, user_id: int) -> None:
        self._execute('UPDATE users SET email_verified_at = %s WHERE id = %s', (datetime.now(), user_id))

    def update_password(self, user_id: int, hash_password: str) -> None:
        self._execute('UPDATE users set password_hash = %s WHERE id = %s', (hash_password, user_id))

    def load_data(self, user_id: int) -> ISavedData | None:
        user = cast(IUser, self._query('SELECT model, temperature, max_output_tokens, top_p, top_k, web_search, last_login_at FROM users WHERE id = %s', (user_id,), fetchone=True))
        if not user:
            return None
        conversations = cast(list[IConversation], self._query('SELECT id, title, is_pinned, word_count, pinned_at FROM conversations WHERE user_id = %s ORDER BY updated_at DESC', (user_id,)))
        chats: dict[str, ISavedSession] = {}
        pinned_entries: list[tuple[str, datetime | None]] = []
        message_counts = {'ai': 0, 'user': 0}
        word_counts = {'ai': 0, 'user': 0}
        for conv in conversations:
            conv_id = conv['id']
            if conv['is_pinned']:
                pinned_entries.append((conv_id, conv.get('pinned_at')))
            message_rows = cast(list[IMessageDB], self._query('SELECT id, role, message, raw_parts, created_at FROM messages WHERE conversation_id = %s ORDER BY created_at', (conv['id'],)))
            messages: list[ISessionMessage] = []
            history: list[ISerializedContent] = []
            for row in message_rows:
                attachments_raw = self._query('SELECT name, mime_type, size, available, data FROM message_attachments WHERE message_id = %s', (row['id'],))
                attachments = cast(list[IAttachment], [{**a, 'data': a['data'].decode('utf-8') if isinstance(a['data'], (bytes, bytearray)) else a['data']} for a in attachments_raw])
                sources = cast(list[ISource], self._query('SELECT uri, title FROM message_sources WHERE message_id = %s', (row['id'],)))
                msg: ISessionMessage = {'role': row['role'], 'message': row['message'], 'timestamp': row['created_at'].isoformat(), 'attachments': attachments}
                if sources:
                    msg['sources'] = sources
                messages.append(msg)
                role_key = 'ai' if row['role'] == 'assistant' else 'user'
                message_counts[role_key] += 1
                word_counts[role_key] += len(row['message'].split())
                parts = self._raw_parts_from_json(row['raw_parts'])
                if parts:
                    history.extend(parts)
            chats[conv_id] = {'title': conv['title'], 'messages': messages, 'history': history}
        pinned_entries.sort(key=lambda entry: (entry[1] is None, entry[1]), reverse=True)
        pinned = [conv_id for conv_id, _ in pinned_entries]
        return {
            'model': user['model'],
            'temperature': user['temperature'],
            'max_output_tokens': user['max_output_tokens'],
            'top_p': user['top_p'],
            'top_k': user['top_k'],
            'chats': chats,
            'chats_count': {'ai': message_counts['ai'], 'user': message_counts['user'], 'chat_session': len(conversations)},
            'words_count': {'ai': word_counts['ai'], 'user': word_counts['user']},
            'web_search': bool(user['web_search']),
            'pinned': pinned,
            'start_time': user['last_login_at'],
        }

    def create_conversation(self, conversation_id: str, user_id: int, title: str, model: str, is_pinned: bool = False) -> None:
        self._execute('INSERT INTO conversations (id, user_id, title, model, is_pinned) VALUES (%s, %s, %s, %s, %s)', (conversation_id, user_id, title, model, is_pinned))

    def rename_conversation(self, conversation_id: str, title: str) -> None:
        self._execute('UPDATE conversations SET title=%s WHERE id=%s', (title, conversation_id))

    def set_pinned(self, conversation_id: str, is_pinned: bool) -> None:
        self._execute('UPDATE conversations SET is_pinned=%s, pinned_at = %s WHERE id=%s', (is_pinned, datetime.now() if is_pinned else None, conversation_id))

    def delete_conversation(self, conversation_id: str) -> None:
        self._execute('DELETE FROM conversations WHERE id=%s', (conversation_id,))

    def add_message(self, conversation_id: str, role: str, message: str, raw_parts: list[dict] | None, attachments: list[IAttachment] | None = None, sources: list[ISource] | None = None) -> int:
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (conversation_id, role, message, raw_parts) VALUES (%s, %s, %s, %s)', (conversation_id, role, message, self._dump_json(raw_parts)))
            message_id = cursor.lastrowid
            for att in attachments or []:
                cursor.execute(
                    'INSERT INTO message_attachments (message_id, name, mime_type, size, available, data) VALUES (%s, %s, %s, %s, %s, %s)',
                    (message_id, att['name'], att['mime_type'], att['size'], att['available'], att.get('data')),
                )
            for src in sources or []:
                cursor.execute('INSERT INTO message_sources (message_id, uri, title) VALUES (%s, %s, %s)', (message_id, src['uri'], src['title']))
            cursor.execute('UPDATE conversations SET message_count = message_count + 1, word_count = word_count + %s WHERE id = %s', (len(message.split()), conversation_id))
            conn.commit()
            cursor.close()
            return message_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update_user_settings(self, user_id: int, model: str, temperature: float, max_output_tokens: int, top_p: float, top_k: int, web_search: bool) -> None:
        self._execute(
            'UPDATE users SET model=%s, temperature=%s, max_output_tokens=%s, top_p=%s, top_k=%s, web_search=%s WHERE id=%s', (model, temperature, max_output_tokens, top_p, top_k, web_search, user_id)
        )

    def register_user(self, full_name: str, email: str, password_hash: str) -> int:
        try:
            return cast(int, self._execute('INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)', (full_name, email, password_hash), return_lastrowid=True))
        except mysql.connector.IntegrityError as err:
            raise RuntimeError('An account with that email already exists.') from err

    def touch_conversation(self, conversation_id: str) -> None:
        self._execute('UPDATE conversations SET updated_at = %s WHERE id = %s', (datetime.now(), conversation_id))

    def delete_message(self, message_id: int) -> None:
        self._execute('DELETE FROM messages WHERE id = %s', (message_id,))

    def get_today_messages_count(self, user_id: int) -> ITodayMessagesCount:
        return cast(
            ITodayMessagesCount,
            self._query(
                """
            SELECT
                COUNT(*) AS total,
                SUM(m.role = 'user') AS user,
                SUM(m.role = 'assistant') AS ai
            FROM messages m
            JOIN conversations c
                ON m.conversation_id = c.id
            WHERE c.user_id = %s
            AND m.created_at >= CURDATE()
            AND m.created_at < CURDATE() + INTERVAL 1 DAY""",
                (user_id,),
                fetchone=True,
            ),
        )
