from datetime import datetime
from typing import TypedDict

from .chat import ISessionMessage


class ISerializedContent(TypedDict):
    role: str
    parts: list[dict[str, object]]


class ISavedSession(TypedDict):
    title: str
    messages: list[ISessionMessage]
    history: list[ISerializedContent]


class IWordsCount(TypedDict):
    ai: int
    user: int


class IChatsCount(IWordsCount):
    chat_session: int


class ISavedData(TypedDict):
    model: str
    temperature: float
    max_output_tokens: int
    top_p: float
    top_k: int
    chats: dict[str, ISavedSession]
    chats_count: IChatsCount
    words_count: IWordsCount
    start_time: datetime
    web_search: bool
    pinned: list[str]
