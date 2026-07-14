from typing import cast

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from assets.css import SIDEBAR_CSS
from assets.js import MENU_CLOSE_JS
from core.models import ISession
from utils import highlight

from . import delete_chat, export_chat_dialog, rename_chat


def toggle_pin(chat_id: str) -> None:
    pinned = list(st.session_state.get('pinned', []))
    if chat_id in pinned:
        pinned.remove(chat_id)
    else:
        pinned.append(chat_id)
    st.session_state.pinned = list(reversed(pinned))
    st.session_state.db.set_pinned(chat_id, chat_id in pinned)


def render_menu_summary(chat_id: str) -> str:
    return """
        <div class="chat-menu-wrap">
            <details class="chat-menu-details">
                <summary class="chat-menu-dots" title="More options">
                    <i class="fa-solid fa-ellipsis-vertical"></i>
                </summary>
                <div class="chat-menu-dropdown"></div>
            </details>
        </div>
        """


def render_chat_row(container: DeltaGenerator, chat_id: str, active_conversation_id: str | None, is_generating: bool, keyword: str) -> None:
    entry_session = cast(ISession, st.session_state.chats[chat_id])
    slot = container.empty()
    st.session_state.sidebar_slots[chat_id] = slot
    title = entry_session['title']
    if title is None:
        slot.markdown('<div class="chat-link-skeleton"></div>', unsafe_allow_html=True)
        return
    is_pinned = chat_id in st.session_state.get('pinned', [])
    use_overlay = bool(keyword) and keyword.lower() in title.lower()
    row_key = f'chat_row_hl_{chat_id}' if use_overlay else f'chat_row_{chat_id}'
    row = slot.container(key=row_key)
    clicked = row.button(title, key=f'select_{chat_id}', width='stretch', type='primary' if chat_id == active_conversation_id else 'secondary', disabled=is_generating)
    if use_overlay:
        row.markdown(f'<div class="chat-highlight-overlay">{highlight(title, keyword)}</div>', unsafe_allow_html=True)
    menu_wrap = row.container(key=f'menu_btn_{chat_id}')
    menu_wrap.markdown(render_menu_summary(chat_id), unsafe_allow_html=True)
    actions = menu_wrap.container(key=f'menu_actions_{chat_id}')
    action_label = 'Unpin chat' if is_pinned else 'Pin chat'
    pin_icon = ':material/keep_off:' if is_pinned else ':material/push_pin:'
    if actions.button(action_label, key=f'pin_toggle_{chat_id}', icon=pin_icon, width='stretch'):
        toggle_pin(chat_id)
        st.rerun()
    if actions.button('Rename chat', key=f'rename_toggle_{chat_id}', icon=':material/edit:', width='stretch'):
        rename_chat(chat_id, entry_session)
    if actions.button('Export chat', key=f'export_toggle_{chat_id}', icon=':material/download:', width='stretch'):
        export_chat_dialog(chat_id, entry_session)
    if actions.button('Delete chat', key=f'delete_toggle_{chat_id}', icon=':material/delete:', width='stretch'):
        delete_chat(chat_id, entry_session)
    if clicked and chat_id != active_conversation_id:
        st.session_state.current_conversation_id = chat_id
        st.switch_page('pages/chat.py')


def render_chat_list(is_on_chat_page: bool = False) -> None:
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    st.html(MENU_CLOSE_JS, unsafe_allow_javascript=True)
    is_generating = st.session_state.get('is_generating', False)
    st.session_state.sidebar_slots = {}
    if not st.session_state.get('chats'):
        return
    st.sidebar.divider()
    st.sidebar.text_input('Search chats', key='chat_search', placeholder='Search chats...', label_visibility='collapsed')
    keyword = st.session_state.get('chat_search', '').strip()
    active_chat_id = st.session_state.get('current_conversation_id') or st.query_params.get('chat_id') if is_on_chat_page else None
    pinned = st.session_state.get('pinned', [])
    pinned_set = set(pinned)
    all_ids = list(st.session_state.chats.keys())
    unpinned = [cid for cid in all_ids if cid not in pinned_set]
    if keyword:
        pinned = [cid for cid in pinned if keyword.lower() in (st.session_state.chats[cid]['title'] or '').lower()]
        unpinned = [cid for cid in unpinned if keyword.lower() in (st.session_state.chats[cid]['title'] or '').lower()]
    if pinned:
        st.sidebar.caption('PINNED CHATS')
        pinned_container = st.sidebar.container(key='chat_sidebar_list_pinned')
        for chat_id in pinned:
            render_chat_row(pinned_container, chat_id, active_chat_id, is_generating, keyword)
    if unpinned:
        st.sidebar.caption('CHATS')
        list_container = st.sidebar.container(key='chat_sidebar_list')
        for chat_id in unpinned:
            render_chat_row(list_container, chat_id, active_chat_id, is_generating, keyword)
