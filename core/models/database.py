from datetime import datetime
from typing import Literal, TypedDict

from .base import IDate
from .chat import IAttachment, ISource, ModelType
from .storage import IWordsCount


class IConversation(IDate):
    id: str
    user_id: int
    title: str
    model: ModelType
    is_pinned: bool
    message_count: int
    word_count: int
    pinned_at: datetime


class IMessageDB(IDate):
    conversation_id: int
    role: Literal['user', 'assistant']
    message: str
    raw_parts: list[dict]


class IMessageAttachment(IDate, IAttachment):
    message_id: int


class IMessageSources(IDate, ISource):
    message_id: int


class ISessionDB(TypedDict):
    id: str
    user_id: int
    expires_at: datetime
    created_at: datetime


class ITodayMessagesCount(IWordsCount):
    total: int
