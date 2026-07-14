import base64
import mimetypes
import re

from google.genai import types
from streamlit.runtime.uploaded_file_manager import UploadedFile

from core.models import IAttachment, ISessionMessage


def files_to_attachments(files: list[UploadedFile]) -> list[IAttachment]:
    result: list[IAttachment] = []
    for f in files:
        mime = f.type or mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
        att: IAttachment = {'name': f.name, 'mime_type': mime, 'size': f.size, 'available': True}
        if mime.startswith(('image/', 'audio/', 'video/')) or mime == 'application/pdf':
            att['data'] = base64.b64encode(f.getvalue()).decode('ascii')
        result.append(att)
    return result


def build_message_parts(text: str, files: list[UploadedFile]) -> list[str | types.Part]:
    parts: list[str | types.Part] = []
    remaining_text = text or ''
    YOUTUBE_URL_RE = re.compile(r'https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=[\w-]+(?:&\S*)?|shorts/[\w-]+(?:\?\S*)?)|youtu\.be/[\w-]+(?:\?\S*)?)', re.IGNORECASE)
    youtube_urls: list[str] = YOUTUBE_URL_RE.findall(remaining_text)
    if youtube_urls:
        remaining_text = YOUTUBE_URL_RE.sub('', remaining_text)
        remaining_text = re.sub(r'\s{2,}', ' ', remaining_text).strip()
    if remaining_text:
        parts.append(remaining_text)
    for url in youtube_urls:
        parts.append(types.Part.from_uri(file_uri=url, mime_type='video/*'))
    for f in files:
        mime = f.type or mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
        parts.append(types.Part.from_bytes(data=f.getvalue(), mime_type=mime))
    return parts


def mark_attachments_unavailable(messages: list[ISessionMessage]) -> list[ISessionMessage]:
    updated = []
    for m in messages:
        m = dict(m)
        if m.get('attachments'):
            m['attachments'] = [{**a, 'available': False} for a in m['attachments']]  # pyright: ignore[reportGeneralTypeIssues]
        updated.append(m)
    return updated
