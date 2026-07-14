import base64
import time
from typing import cast

import streamlit as st
from google.genai.chats import Chat
from streamlit.delta_generator import DeltaGenerator

from core import GEMINI_2_MODELS
from core.models import IAttachment, IParsedResponse, ISessionMessage, ISource, ResponseModel
from services import create_document
from utils import get_timestamp


def extract_sources_from_chunk(chunk) -> list[ISource]:
    candidates = getattr(chunk, 'candidates', None) or []
    if not candidates:
        return []
    grounding_metadata = getattr(candidates[0], 'grounding_metadata', None)
    if not grounding_metadata:
        return []
    grounding_chunks = getattr(grounding_metadata, 'grounding_chunks', None) or []
    sources: list[ISource] = []
    seen: set[str] = set()
    for gc in grounding_chunks:
        web = getattr(gc, 'web', None)
        if not web:
            continue
        uri = getattr(web, 'uri', None)
        if not uri or uri in seen:
            continue
        seen.add(uri)
        sources.append({'uri': uri, 'title': getattr(web, 'title', None) or uri})
    return sources


def parse_llm_response(raw: str) -> ResponseModel:
    cleaned = raw.strip()
    try:
        return ResponseModel.model_validate_json(cleaned)
    except Exception as err:
        print(f'Failed to parse structured response, falling back to raw text: {err}')
        return ResponseModel(text=raw, document=False)


def stream_chat_response(chat: Chat, parts, stream_card, response_placeholder: DeltaGenerator, uid: str) -> ISessionMessage:
    from ui import render_document_card, render_generating_indicator

    raw_response = ''
    sources: list[ISource] = []
    stream = chat.send_message_stream(parts)
    flag = st.session_state.web_search and st.session_state.model in GEMINI_2_MODELS
    if flag:
        full_response = ''
        for chunk in stream:
            chunk_sources = extract_sources_from_chunk(chunk)
            if chunk_sources:
                sources = chunk_sources
            if chunk.text:
                for ch in chunk.text:
                    full_response += ch
                    response_placeholder.markdown(full_response + '▌')
                    time.sleep(0.01)
                response_placeholder.markdown(full_response)
        return {'role': 'assistant', 'message': full_response, 'timestamp': get_timestamp(), 'attachments': [], 'sources': sources}
    for chunk in stream:
        if chunk.text:
            raw_response += chunk.text
    parsed = (
        cast(IParsedResponse, {'text': raw_response, 'document': False})
        if st.session_state.web_search and st.session_state.model in GEMINI_2_MODELS
        else cast(IParsedResponse, parse_llm_response(raw_response).model_dump())
    )
    typed = ''
    for ch in parsed['text']:
        typed += ch
        response_placeholder.markdown(typed + '▌')
        time.sleep(0.01)
    response_placeholder.markdown(parsed['text'])
    attachments: list[IAttachment] = []
    if parsed['document'] and parsed['extension'] and parsed['html']:
        doc_placeholder = stream_card.empty()
        doc_placeholder.markdown(render_generating_indicator('Creating document'), unsafe_allow_html=True)
        try:
            data, mime_type, filename = create_document(parsed['extension'], parsed['html'], parsed['filename'])
            attachment: IAttachment = {'name': filename, 'mime_type': mime_type, 'data': base64.b64encode(data).decode('utf-8'), 'available': True, 'size': len(data)}  # pyright: ignore[reportAssignmentType]
            attachments.append(attachment)
            doc_placeholder.empty()
            render_document_card(stream_card, attachment, f'{uid}_0')
        except Exception as doc_err:
            doc_placeholder.empty()
            print(doc_err)
            st.toast(f'Failed to create the document: {doc_err}', icon=':material/error:')
    return {'role': 'assistant', 'message': parsed['text'], 'timestamp': get_timestamp(), 'attachments': attachments, 'sources': sources}
