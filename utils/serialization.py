import base64
import enum
from datetime import date, datetime
from typing import Any, cast

from google.genai.types import Content, ContentOrDict


def _json_safe(obj: Any):
    if isinstance(obj, bytes):
        return {'__b64__': base64.b64encode(obj).decode('ascii')}
    if isinstance(obj, enum.Enum):
        return obj.value
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    return obj


def _restore_bytes(obj: Any):
    if isinstance(obj, dict):
        if set(obj.keys()) == {'__b64__'}:
            return base64.b64decode(obj['__b64__'])
        return {k: _restore_bytes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_restore_bytes(v) for v in obj]
    return obj


def encode_history_for_storage(history: list[ContentOrDict] | list[Content]) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], [_json_safe(cast(Content, content).model_dump(mode='python')) for content in history])


def decode_history_from_storage(saved: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], [_restore_bytes(content) for content in saved])


def split_new_history_entries(entries: list[dict]) -> tuple[dict | None, list[dict]]:
    user_entry = next((e for e in entries if e.get('role') == 'user'), None)
    model_entries = [e for e in entries if e.get('role') != 'user']
    return user_entry, model_entries
