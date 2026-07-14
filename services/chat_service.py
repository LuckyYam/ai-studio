from typing import cast

import streamlit as st
from google.genai.errors import APIError
from google.genai.types import ContentOrDict

from core import GEMINI_2_MODELS, Database, get_chat
from core.models import ISession


def update_chat() -> None:
    if not st.session_state.chats:
        return None
    chats = cast(dict[str, ISession], st.session_state.chats)
    for key, value in chats.items():
        try:
            old_chat = value['chat']
            history = cast(list[ContentOrDict], old_chat.get_history())
            st.session_state.chats[key]['chat'] = get_chat(
                st.session_state.client,
                st.session_state.model,
                st.session_state.temperature,
                st.session_state.max_output_tokens,
                st.session_state.top_k,
                st.session_state.top_p,
                history,
                st.session_state.web_search,
            )
        except APIError as err:
            st.error(f'For Title: {value["title"]} {str(err)}')
        except RuntimeError as err:
            st.error(f'For Title: {value["title"]} {str(err)}')
        except Exception as err:
            st.error(f'For Title: {value["title"]} {str(err)}')
    try:
        db = cast(Database, st.session_state.db)
        db.update_user_settings(
            cast(int, st.session_state.user['id']),
            st.session_state.model,
            st.session_state.temperature,
            st.session_state.max_output_tokens,
            st.session_state.top_p,
            st.session_state.top_k,
            st.session_state.web_search,
        )
    except RuntimeError as err:
        st.error(f'Failed to save settings: {err}')


def bump_chat_to_top(chat_id: str) -> None:
    chats = st.session_state.chats
    chat = chats[chat_id]
    st.session_state.chats = {chat_id: chat, **st.session_state.chats}


def sync_config() -> None:
    keys = ['temperature', 'max_output_tokens', 'top_p', 'top_k']
    for key in keys:
        st.session_state[key] = st.session_state[f'widget_{key}']
    update_chat()


def on_model_change():
    st.session_state.model = st.session_state.model_widget
    if st.session_state.get('web_search') and st.session_state.model not in GEMINI_2_MODELS:
        st.session_state.web_search = False
    update_chat()
