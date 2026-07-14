from typing import Literal, NotRequired, TypedDict

from google.genai.chats import Chat
from pydantic import BaseModel, model_validator

ModelType = Literal['gemini-3.1-flash-lite', 'gemini-3.5-flash', 'gemini-3-flash-preview', 'gemini-2.5-flash', 'gemini-2.5-flash-lite']


class ResponseModel(BaseModel):
    intent_analysis: str | None = None
    text: str
    document: bool = False
    extension: Literal['pdf', 'docx', 'csv'] | None = None
    html: str | None = None
    filename: str | None = None

    @model_validator(mode='after')
    def validate_document_fields(self):
        if self.document:
            if self.intent_analysis is None:
                raise ValueError('intent_analysis is required when document=True')
            if self.extension is None:
                raise ValueError('extension is required when document=True')
            if self.html is None:
                raise ValueError('html is required when document=True')
            if self.filename is None:
                raise ValueError('filename is required when document=True')
        return self


class IParsedResponse(TypedDict):
    text: str
    html: str
    extension: Literal['pdf', 'docx', 'csv']
    filename: str
    document: bool


class IAttachment(TypedDict):
    name: str
    mime_type: str
    size: int
    available: bool
    data: NotRequired[str]


class ISource(TypedDict):
    uri: str
    title: str


class ISessionMessage(TypedDict):
    id: NotRequired[int]
    role: Literal['assistant', 'user']
    message: str
    timestamp: str
    attachments: list[IAttachment]
    sources: NotRequired[list[ISource]]


class ISession(TypedDict):
    title: str
    messages: list[ISessionMessage]
    chat: Chat
