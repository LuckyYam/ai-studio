from datetime import datetime

from .base import IDate
from .chat import ModelType


class IUser(IDate):
    full_name: str
    email: str
    password_hash: str
    model: ModelType
    temperature: float
    max_output_tokens: int
    top_p: float
    top_k: int
    web_search: bool
    is_active: bool
    email_verified_at: datetime
    last_login_at: datetime
