import base64
import time
from urllib.parse import urlparse

import streamlit as st

from assets.css import EXPORT_FORMAT_CSS, RENAME_DIALOG_CSS
from assets.js import RENAME_LIVE_WATCHER_JS
from core.models import IAttachment, ISession, ISource
from services import EXPORT_FORMATS, build_json_export, build_markdown_export, build_text_export
from utils import count_words


def _select_export_format(fmt: str) -> None:
    st.session_state.export_format = fmt


def render_export_format_card(fmt: str, icon: str, title: str, desc: str, selected: bool) -> None:
    card = st.container(key=f'export_fmt_card_{fmt}')
    icon_col, text_col, radio_col = card.columns([0.14, 0.72, 0.14])
    icon_col.markdown(f'<div class="export-fmt-icon"><i class="{icon}"></i></div>', unsafe_allow_html=True)
    text_col.markdown(f'<div class="export-fmt-title">{title}</div><div class="export-fmt-desc">{desc}</div>', unsafe_allow_html=True)
    radio_col.markdown(f'<div class="export-fmt-radio {"checked" if selected else ""}"></div>', unsafe_allow_html=True)
    card.button('', key=f'export_fmt_click_{fmt}', on_click=_select_export_format, args=(fmt,))


@st.dialog('Sources')
def show_sources_dialog(sources: list[ISource]) -> None:
    if not sources:
        st.info('No sources available for this response.')
        return
    for src in sources:
        host = urlparse(src['uri']).netloc
        st.markdown(
            f'<div class="source-item"><a class="source-title" href="{src["uri"]}" target="_blank" rel="noopener">{src["title"]}</a><div class="source-host">{host}</div></div>', unsafe_allow_html=True
        )


@st.dialog('Preview attachment')
def preview_attachment_dialog(att: IAttachment) -> None:
    mime = att.get('mime_type', '')
    data = att.get('data')
    st.write(f'**{att["name"]}**')
    if not data:
        st.info('This attachment is no longer available.')
        return
    raw = base64.b64decode(data)
    if mime.startswith('video/'):
        st.video(raw)
    elif mime == 'application/pdf':
        st.markdown(
            f'<embed src="data:application/pdf;base64,{data}" width="100%" height="600" type="application/pdf" style="border-radius:8px;border:1px solid rgba(128,128,128,0.3);" />',
            unsafe_allow_html=True,
        )
    st.download_button('Download', data=raw, file_name=att['name'], mime=mime, width='stretch')


@st.dialog('Rename this chat')
def rename_chat(chat_id: str, session_data: ISession) -> None:
    st.markdown(RENAME_DIALOG_CSS, unsafe_allow_html=True)
    current_title = session_data['title'] or ''
    input_key = f'rename_input_{chat_id}'
    st.text_input('New title', value=current_title, key=input_key, label_visibility='collapsed')
    st.html(RENAME_LIVE_WATCHER_JS, unsafe_allow_javascript=True)
    trimmed = st.session_state[input_key].strip()
    is_disabled = not trimmed or trimmed == current_title
    actions = st.container(key='rename_dialog_actions')
    _, cancel_col, rename_col = actions.columns([2, 1.3, 1.3])
    if cancel_col.button('Cancel', width='stretch', key='rename_cancel_btn'):
        st.session_state.pop(input_key, None)
        st.rerun()
    if rename_col.button('Rename', type='primary', width='stretch', key='rename_confirm_btn', disabled=is_disabled):
        session_data['title'] = trimmed
        st.session_state.db.rename_conversation(chat_id, trimmed)
        st.session_state.pop(input_key, None)
        st.toast('Chat renamed!')
        time.sleep(1.5)
        st.rerun()


@st.dialog('Delete chat?')
def delete_chat(chat_id: str, session_data: ISession) -> None:
    st.write(f'Are you sure you want to delete **{session_data["title"]}**?')
    cancel_col, delete_col = st.columns(2)
    if cancel_col.button('Cancel', width='stretch'):
        st.rerun()
    elif delete_col.button('Delete', type='primary', width='stretch'):
        user_count = sum(1 for m in session_data['messages'] if m['role'] == 'user')
        ai_count = sum(1 for m in session_data['messages'] if m['role'] == 'assistant')
        user_words = sum(count_words(m['message']) for m in session_data['messages'] if m['role'] == 'user')
        ai_words = sum(count_words(m['message']) for m in session_data['messages'] if m['role'] == 'assistant')
        st.session_state.chats_count['user'] -= user_count
        st.session_state.chats_count['ai'] -= ai_count
        st.session_state.chats_count['chat_session'] -= 1
        st.session_state.words_count['ai'] -= ai_words
        st.session_state.words_count['user'] -= user_words
        del st.session_state.chats[chat_id]
        st.session_state.db.delete_conversation(chat_id)
        st.toast('Chat deleted!')
        time.sleep(1.5)
        if st.session_state.current_conversation_id == chat_id:
            if st.session_state.chats:
                st.session_state.current_conversation_id = next(reversed(st.session_state.chats))
            else:
                st.session_state.current_conversation_id = None
            st.switch_page('pages/new_chat.py')
        st.rerun()


@st.dialog('Export Conversation')
def export_chat_dialog(chat_id: str, session_data: ISession) -> None:
    st.markdown(EXPORT_FORMAT_CSS, unsafe_allow_html=True)
    st.write('Select your preferred file format to save this conversation. Your formatting and links will be preserved.')
    if 'export_format' not in st.session_state:
        st.session_state.export_format = 'json'
    selected_format = st.session_state.export_format
    for fmt, icon, title, desc in EXPORT_FORMATS:
        render_export_format_card(fmt, icon, title, desc, selected_format == fmt)
    if selected_format == 'json':
        export_data = build_json_export(chat_id, session_data)
        file_name, mime = f'chat_{chat_id}.json', 'application/json'
    elif selected_format == 'markdown':
        export_data = build_markdown_export(session_data)
        file_name, mime = f'chat_{chat_id}.md', 'text/markdown'
    else:
        export_data = build_text_export(session_data)
        file_name, mime = f'chat_{chat_id}.txt', 'text/plain'
    actions = st.container(key='export_dialog_actions')
    cancel_col, download_col = actions.columns(2)
    if cancel_col.button('Cancel', width='stretch'):
        st.rerun()
    download_col.download_button('Download', icon=':material/download:', data=export_data, file_name=file_name, mime=mime, width='stretch', type='primary')
    st.caption('Exports include all messages and system prompts.')
