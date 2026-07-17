import base64
from datetime import datetime
from unittest.mock import MagicMock
import mysql.connector
import pytest
from core.database import Database

FAKE_ATTACHMENT_DATA = base64.b64encode(b'x').decode('ascii')


@pytest.fixture
def db(mock_db_pool: MagicMock) -> Database:
    return Database(host='localhost', user='root', password='', database='ai_studio_db')


def test_get_user_by_email_returns_row(db: Database, mock_db_pool: MagicMock):
    mock_cursor = mock_db_pool.get_connection.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = {'id': 1, 'email': 'a@b.com'}
    user = db.get_user_by_email('a@b.com')
    assert user == {'id': 1, 'email': 'a@b.com'}
    sql, params = mock_cursor.execute.call_args[0]
    assert 'FROM users WHERE email = %s' in sql
    assert params == ('a@b.com',)


def test_get_user_by_email_returns_none_when_not_found(db: Database, mock_db_pool: MagicMock):
    mock_cursor = mock_db_pool.get_connection.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = None
    assert db.get_user_by_email('nobody@example.com') is None


def test_query_closes_connection_even_on_success(db: Database, mock_db_pool: MagicMock):
    mock_conn = mock_db_pool.get_connection.return_value
    mock_conn.cursor.return_value.fetchone.return_value = {'id': 1}
    db.get_user_by_id(1)
    mock_conn.close.assert_called_once()


def test_query_raises_runtime_error_when_connection_pool_exhausted(db: Database, mock_db_pool: MagicMock):
    mock_db_pool.get_connection.side_effect = mysql.connector.Error('pool exhausted')
    with pytest.raises(RuntimeError, match='Could not connect'):
        db.get_user_by_email('a@b.com')


def test_query_raises_runtime_error_on_query_failure_and_still_closes(db: Database, mock_db_pool: MagicMock):
    mock_conn = mock_db_pool.get_connection.return_value
    mock_conn.cursor.return_value.execute.side_effect = mysql.connector.Error('syntax error')
    with pytest.raises(RuntimeError, match='Database query failed'):
        db.get_user_by_email('a@b.com')
    mock_conn.close.assert_called_once()


def test_execute_rolls_back_on_failure(db: Database, mock_db_pool: MagicMock):
    mock_conn = mock_db_pool.get_connection.return_value
    mock_conn.cursor.return_value.execute.side_effect = mysql.connector.Error('write failed')
    with pytest.raises(RuntimeError, match='Database write failed'):
        db.touch_last_login(1)
    mock_conn.rollback.assert_called_once()
    mock_conn.commit.assert_not_called()


def test_register_user_returns_new_id(db: Database, mock_db_pool: MagicMock):
    mock_cursor = mock_db_pool.get_connection.return_value.cursor.return_value
    mock_cursor.lastrowid = 99
    new_id = db.register_user('Full Name', 'fullname@example.com', 'hashed-pw')
    assert new_id == 99


def test_register_user_raises_friendly_error_on_duplicate_email(db: Database, mock_db_pool: MagicMock):
    mock_cursor = mock_db_pool.get_connection.return_value.cursor.return_value
    mock_cursor.execute.side_effect = mysql.connector.IntegrityError('Duplicate entry')
    with pytest.raises(RuntimeError, match='already exists'):
        db.register_user('Full Name', 'fullname@example.com', 'hashed-pw')


def test_add_message_inserts_message_and_attachments_then_commits(db: Database, mock_db_pool: MagicMock):
    mock_conn = mock_db_pool.get_connection.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.lastrowid = 55
    message_id = db.add_message(
        conversation_id='conv-1',
        role='user',
        message='hello world',
        raw_parts=[{'role': 'user'}],
        attachments=[{'name': 'a.png', 'mime_type': 'image/png', 'size': 10, 'available': True, 'data': FAKE_ATTACHMENT_DATA}],
        sources=[{'uri': 'https://example.com', 'title': 'Example'}],
    )
    assert message_id == 55
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_conn.close.assert_called_once()
    executed_sql = [call.args[0] for call in mock_cursor.execute.call_args_list]
    assert any('INSERT INTO messages' in sql for sql in executed_sql)
    assert any('INSERT INTO message_attachments' in sql for sql in executed_sql)
    assert any('INSERT INTO message_sources' in sql for sql in executed_sql)
    assert any('UPDATE conversations SET message_count' in sql for sql in executed_sql)


def test_add_message_word_count_uses_message_text(db: Database, mock_db_pool: MagicMock):
    mock_cursor = mock_db_pool.get_connection.return_value.cursor.return_value
    mock_cursor.lastrowid = 1
    db.add_message(conversation_id='conv-1', role='assistant', message='four words go here', raw_parts=None)
    update_call = next(call for call in mock_cursor.execute.call_args_list if 'message_count' in call.args[0])
    _, params = update_call.args
    assert params[0] == 4


def test_add_message_rolls_back_when_attachment_insert_fails(db: Database, mock_db_pool: MagicMock):
    mock_conn = mock_db_pool.get_connection.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.lastrowid = 1
    mock_cursor.execute.side_effect = [None, RuntimeError('disk full')]
    with pytest.raises(RuntimeError, match='disk full'):
        db.add_message(
            conversation_id='conv-1',
            role='user',
            message='hi',
            raw_parts=None,
            attachments=[{'name': 'a.png', 'mime_type': 'image/png', 'size': 10, 'available': True, 'data': FAKE_ATTACHMENT_DATA}],
        )
    mock_conn.rollback.assert_called_once()
    mock_conn.commit.assert_not_called()
    mock_conn.close.assert_called_once()


def test_load_data_returns_none_when_user_missing(db: Database, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(db, '_query', MagicMock(return_value=None))
    assert db.load_data(user_id=1) is None


def test_load_data_assembles_conversations_and_counts(db: Database, monkeypatch: pytest.MonkeyPatch):
    user_row = {
        'model': 'gemini-3.1-flash-lite',
        'temperature': 0.1,
        'max_output_tokens': 2048,
        'top_p': 0.95,
        'top_k': 64,
        'web_search': 0,
        'last_login_at': datetime(2026, 7, 1, 9, 0, 0),
    }
    conversations = [
        {'id': 'conv-1', 'title': 'First chat', 'is_pinned': True, 'word_count': 12, 'pinned_at': datetime(2026, 7, 2)},
        {'id': 'conv-2', 'title': 'Second chat', 'is_pinned': False, 'word_count': 3, 'pinned_at': None},
    ]
    messages_conv1 = [
        {'id': 1, 'role': 'user', 'message': 'hi', 'raw_parts': None, 'created_at': datetime(2026, 7, 1, 9, 5)},
        {'id': 2, 'role': 'assistant', 'message': 'hello', 'raw_parts': None, 'created_at': datetime(2026, 7, 1, 9, 6)},
    ]
    messages_conv2 = [
        {'id': 3, 'role': 'user', 'message': 'yo', 'raw_parts': None, 'created_at': datetime(2026, 7, 2, 10, 0)},
    ]

    def fake_query(sql: str, params: tuple = (), fetchone: bool = False):
        if 'FROM users WHERE id' in sql:
            return user_row
        if 'FROM conversations WHERE user_id' in sql:
            return conversations
        if 'FROM messages WHERE conversation_id' in sql:
            return messages_conv1 if params[0] == 'conv-1' else messages_conv2
        if 'FROM message_attachments' in sql:
            return []
        if 'FROM message_sources' in sql:
            return []
        raise AssertionError(f'unexpected query: {sql}')

    monkeypatch.setattr(db, '_query', MagicMock(side_effect=fake_query))
    result = db.load_data(user_id=1)
    assert result is not None
    assert result['model'] == 'gemini-3.1-flash-lite'
    assert result['pinned'] == ['conv-1']
    assert set(result['chats'].keys()) == {'conv-1', 'conv-2'}
    assert len(result['chats']['conv-1']['messages']) == 2
    assert result['chats_count'] == {'ai': 1, 'user': 2, 'chat_session': 2}
    assert result['words_count'] == {'ai': 1, 'user': 2}
    assert result['web_search'] is False


def test_load_data_orders_multiple_pinned_conversations_by_pinned_at_desc(db: Database, monkeypatch: pytest.MonkeyPatch):
    user_row = {
        'model': 'gemini-3.1-flash-lite',
        'temperature': 0.1,
        'max_output_tokens': 2048,
        'top_p': 0.95,
        'top_k': 64,
        'web_search': 1,
        'last_login_at': None,
    }
    conversations = [
        {'id': 'older-pin', 'title': 'A', 'is_pinned': True, 'word_count': 0, 'pinned_at': datetime(2026, 1, 1)},
        {'id': 'newer-pin', 'title': 'B', 'is_pinned': True, 'word_count': 0, 'pinned_at': datetime(2026, 6, 1)},
    ]

    def fake_query(sql: str, params: tuple = (), fetchone: bool = False):
        if 'FROM users WHERE id' in sql:
            return user_row
        if 'FROM conversations WHERE user_id' in sql:
            return conversations
        if 'FROM messages WHERE conversation_id' in sql:
            return []
        raise AssertionError(f'unexpected query: {sql}')

    monkeypatch.setattr(db, '_query', MagicMock(side_effect=fake_query))
    result = db.load_data(1)
    assert result is not None
    assert result['pinned'] == ['newer-pin', 'older-pin']
