import json

from core.models import ISession

EXPORT_FORMATS = [
    ('json', 'json-icon', 'JSON File', 'Recommended for data migration and developers.'),
    ('markdown', 'fa-brands fa-markdown', 'Markdown', 'Preserves headings, lists, and code block styling.'),
    ('text', 'fa-solid fa-file-lines', 'Plain Text', 'Simple text file without any rich formatting.'),
]


def build_json_export(chat_id: str, session_data: ISession) -> str:
    messages = []
    for msg in session_data['messages']:
        entry = {k: v for k, v in msg.items() if k not in ('id', 'attachments', 'sources')}
        attachments = msg.get('attachments') or []
        if attachments:
            entry['attachments'] = [att['name'] for att in attachments]
        sources = msg.get('sources') or []
        if sources:
            entry['sources'] = sources
        messages.append(entry)
    export_payload = {'chat_id': chat_id, 'title': session_data['title'], 'messages': messages}
    return json.dumps(export_payload, indent=4, default=str)


def build_text_export(session_data: ISession) -> str:
    lines: list[str] = []
    for msg in session_data['messages']:
        role_label = 'USER' if msg['role'] == 'user' else 'ASSISTANT'
        lines.append(f'[{msg["timestamp"]}]')
        lines.append(f'[{role_label}] - {msg["message"]}')
        for att in msg.get('attachments') or []:
            lines.append(f'[ATTACHMENT] - {att["name"]}')
        for src in msg.get('sources') or []:
            lines.append(f'[SOURCE] - {src["title"]} ({src["uri"]})')
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'


def build_markdown_export(session_data: ISession) -> str:
    lines: list[str] = [f'# {session_data["title"] or "Untitled Chat"}', '']
    for msg in session_data['messages']:
        role_label = 'User' if msg['role'] == 'user' else 'Assistant'
        lines.append(f'**{role_label}** · _{msg["timestamp"]}_')
        lines.append('')
        lines.append(msg['message'])
        attachments = msg.get('attachments') or []
        if attachments:
            lines.append('')
            for att in attachments:
                lines.append(f'- Attachment: {att["name"]}')
        sources = msg.get('sources') or []
        if sources:
            lines.append('')
            for src in sources:
                lines.append(f'- Source: [{src["title"]}]({src["uri"]})')
        lines.append('')
        lines.append('---')
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'
