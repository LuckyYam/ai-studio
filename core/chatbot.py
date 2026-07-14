from google import genai
from google.genai import types
from google.genai.chats import Chat
from google.genai.errors import APIError
from google.genai.types import ContentOrDict
from core.config import GEMINI_2_MODELS
from core.models import ModelType, ResponseModel
from prompts import DOCUMENT_ASSISTANT_INSTRUCTION, TITLE_GENERATION_INSTRUCTION


def get_chat(
    client: genai.Client,
    model: ModelType = 'gemini-3.1-flash-lite',
    temperature: float = 0.1,
    maximum_output_tokens: int | None = None,
    top_k: int | None = None,
    top_p: float | None = None,
    history: list[ContentOrDict] | None = None,
    web_search=False,
) -> Chat:
    try:
        flag = False
        search_tool = None
        if web_search and model in GEMINI_2_MODELS:
            flag = True
            search_tool = types.Tool(google_search=types.GoogleSearch())
        chat_config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=maximum_output_tokens,
            top_k=top_k,
            top_p=top_p,
            tools=[search_tool] if search_tool and flag else None,
            system_instruction=None if flag else DOCUMENT_ASSISTANT_INSTRUCTION,
            response_mime_type=None if flag else 'application/json',
            response_schema=None if flag else ResponseModel,
        )
        chat = client.chats.create(model=model, config=chat_config, history=history)
        return chat
    except APIError as err:
        raise RuntimeError(f'Google GenAI API Error [Status {err.code}]: {err.message}')
    except Exception as err:
        raise RuntimeError(f'Unexpected error occurred: {err}')


def get_chat_title(client: genai.Client, parts: list[str | types.Part]) -> str:
    try:
        if not parts:
            raise RuntimeError('Nothing to generate a title from.')
        sending_config = types.GenerateContentConfig(system_instruction=TITLE_GENERATION_INSTRUCTION, temperature=1.5, max_output_tokens=20)
        content_parts = [types.Part.from_text(text=p) if isinstance(p, str) else p for p in parts]
        contents = types.Content(role='user', parts=content_parts)
        response = client.models.generate_content(model='gemini-3.1-flash-lite', contents=contents, config=sending_config)
        if response.text:
            return response.text.strip()
        else:
            raise RuntimeError("Couldn't generate the title.")
    except APIError as err:
        raise RuntimeError(f'Google GenAI API Error [Status {err.code}]: {err.message}')
    except Exception as err:
        raise RuntimeError(f'Unexpected error occurred: {err}')
