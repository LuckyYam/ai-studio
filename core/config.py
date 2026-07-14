import os
from typing import cast

from dotenv import load_dotenv

from .models import IConfig, ModelType

VARIABLES = ['GEMINI_API_KEY', 'JWT_SECRET']
SUPPORTED_FILE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'webp', 'heic', 'heif', 'mp4', 'mpeg', 'mpg', 'mov', 'avi', 'flv', 'mpg', 'webm', 'wmv', '3gp', 'wav', 'mp3', 'aiff', 'aac', 'ogg', 'flac', 'pdf']
PREVIEWABLE_PREFIXES = ('image/', 'audio/', 'video/')
MODELS: dict[ModelType, str] = {
    'gemini-3.1-flash-lite': 'Gemini 3.1 Flash Lite',
    'gemini-3.5-flash': 'Gemini 3.5 Flash',
    'gemini-3-flash-preview': 'Gemini 3 Flash',
    'gemini-2.5-flash': 'Gemini 2.5 Flash',
    'gemini-2.5-flash-lite': 'Gemini 2.5 Flash-Lite',
}
GEMINI_2_MODELS: list[ModelType] = ['gemini-2.5-flash-lite', 'gemini-2.5-flash']
JWT_ALGORITHM = 'HS256'
JWT_EXPIRY_DAYS_REMEMBERED = 30
JWT_EXPIRY_DAYS_DEFAULT = 1
AUTH_COOKIE_NAME = 'ai_studio_session'
DEFAULTS = {
    'model': 'gemini-3.1-flash-lite',
    'temperature': 0.1,
    'top_p': 0.95,
    'top_k': 64,
    'max_output_tokens': 2048,
    'chats': {},
    'chats_count': {'ai': 0, 'user': 0, 'chat_session': 0},
    'words_count': {'ai': 0, 'user': 0},
    'start_time': None,
    'is_loaded': False,
    'web_search': False,
    'pinned': [],
    'is_logged_in': False,
    'current_conversation_id': None,
}


def load_config() -> IConfig:
    load_dotenv()
    data = cast(IConfig, {})
    for name in VARIABLES:
        value = os.getenv(name)
        if not value or not value.strip():
            raise RuntimeError(f'`{name}` value not set in the environmental variables file (`.env`).')
        data[name] = value
    return data
