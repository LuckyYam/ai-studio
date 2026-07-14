import time
from datetime import datetime
from typing import cast

import streamlit as st
from google.genai.chats import Chat
from google.genai.types import ContentOrDict

from assets.css import ATTACHMENT_BUTTON_CSS, DOCUMENT_CARD_CSS, MESSAGE_CSS, MODEL_DOCK_CSS, SOURCES_BUTTON_CSS, USER_ATTACHMENT_CARD_CSS
from assets.js import DOCK_ALIGN_JS
from core import SUPPORTED_FILE_EXTENSIONS, Database, get_chat, get_chat_title
from core.models import ISession
from services import bump_chat_to_top, stream_chat_response
from ui import display_user_turn, entry_role, model_selector, render_copy_overlay, render_document_card, render_generating_indicator, render_sources_trigger, web_search_button
from utils import build_message_parts, count_words, encode_history_for_storage, files_to_attachments, get_timestamp, split_new_history_entries

if not st.session_state.is_logged_in:
    st.switch_page('pages/login.py')
db = cast(Database, st.session_state.db)
current_id = st.query_params.get('chat_id')
if current_id is None:
    current_id = st.session_state.get('current_conversation_id')
if current_id is None or current_id not in st.session_state.chats:
    st.switch_page('pages/new_chat.py')
st.session_state.current_conversation_id = current_id
st.query_params['chat_id'] = current_id
st.markdown(
    """
    <style>
    div.block-container {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.set_page_config(st.session_state.chats[current_id]['title'] or 'New Chat', layout='wide', page_icon=':material/chat:')
if not st.session_state.get('chats'):
    st.switch_page('pages/new_chat.py')
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
is_generating = st.session_state.is_generating
st.markdown(MESSAGE_CSS, unsafe_allow_html=True)
st.markdown(ATTACHMENT_BUTTON_CSS, unsafe_allow_html=True)
st.markdown(USER_ATTACHMENT_CARD_CSS, unsafe_allow_html=True)
st.markdown(SOURCES_BUTTON_CSS, unsafe_allow_html=True)
st.markdown(DOCUMENT_CARD_CSS, unsafe_allow_html=True)
st.markdown(MODEL_DOCK_CSS, unsafe_allow_html=True)
st.html(DOCK_ALIGN_JS, unsafe_allow_javascript=True)
session = cast(ISession, st.session_state.chats[current_id])
chat = session['chat']
last_assistant_index = next((i for i in range(len(session['messages']) - 1, -1, -1) if session['messages'][i]['role'] == 'assistant'), None)
for i, msg in enumerate(session['messages']):
    if msg['role'] == 'user':
        display_user_turn(f'hist_{i}', msg['message'], msg.get('attachments', []), is_generating)
    else:
        render_sources_trigger(f'hist_{i}', msg.get('sources', []))
        ai_container = st.container(key=f'ai_msg_{i}')
        ai_container.markdown(msg['message'])
        for j, att in enumerate(msg.get('attachments', [])):
            render_document_card(ai_container, att, f'hist_{i}_{j}')
        if not is_generating:
            ai_container.markdown(render_copy_overlay(msg['message']), unsafe_allow_html=True)
            if i == last_assistant_index:
                if ai_container.button('', icon=':material/refresh:', key=f'regen_btn_{i}', help='Regenerate response'):
                    if session['messages'] and session['messages'][-1]['role'] == 'assistant':
                        popped = session['messages'].pop()
                        st.session_state.popped_ai_msg = popped
                        st.session_state.words_count['ai'] -= count_words(popped['message'])
                        st.session_state.chats_count['ai'] -= 1
                    st.session_state.pending_regenerate = True
                    st.session_state.is_generating = True
                    bump_chat_to_top(current_id)
                    if 'id' in popped:
                        db.delete_message(popped['id'])
                    db.touch_conversation(current_id)
                    st.rerun()
is_pending_first_message = st.session_state.get('pending_prompt') is not None and st.session_state.get('pending_chat_id') == current_id
has_pending_followup = st.session_state.get('pending_followup') is not None
is_pending_regenerate = st.session_state.get('pending_regenerate', False)
st.write('')
prompt_value = st.chat_input('Ask me anything...', disabled=is_pending_first_message or is_generating, accept_file=True, file_type=SUPPORTED_FILE_EXTENSIONS, max_upload_size=15)
if prompt_value and ((prompt_value.text and prompt_value.text.strip()) or prompt_value.files) and not is_generating:
    bump_chat_to_top(current_id)
    st.session_state.pending_followup = prompt_value.text or ''
    st.session_state.pending_followup_files = prompt_value.files or []
    st.session_state.is_generating = True
    st.rerun()
if is_pending_first_message and not is_generating:
    st.session_state.is_generating = True
    st.rerun()
if is_pending_first_message and is_generating:
    if not st.session_state.start_time:
        st.session_state.start_time = datetime.now()
    pending_prompt = st.session_state.pop('pending_prompt')
    pending_files = st.session_state.pop('pending_files', [])
    pending_prompt_words = count_words(pending_prompt)
    attachments = files_to_attachments(pending_files)
    parts = build_message_parts(pending_prompt, pending_files)
    st.session_state.pop('pending_chat_id')
    display_user_turn('live_first', pending_prompt, attachments, is_generating)
    session['messages'].append({'role': 'user', 'message': pending_prompt, 'timestamp': get_timestamp(), 'attachments': attachments})
    st.session_state.chats_count['user'] += 1
    st.session_state.words_count['user'] += pending_prompt_words
    stream_card = st.container(key='ai_card_stream')
    response_placeholder = stream_card.empty()
    response_placeholder.markdown(render_generating_indicator(), unsafe_allow_html=True)
    try:
        title = get_chat_title(st.session_state.client, parts)
    except RuntimeError as err:
        title = 'New Chat'
        print(err)
    slot = st.session_state.get('sidebar_slots', {}).get(current_id)
    typed = ''
    if slot:
        for ch in title:
            typed += ch
            slot.markdown(f'<div class="chat-link-typing">{typed + "▌"}</div>', unsafe_allow_html=True)
            time.sleep(0.02)
    session['title'] = title
    db.rename_conversation(current_id, title)
    try:
        history_len_before = len(chat.get_history())
        assistant_message = stream_chat_response(chat, parts, stream_card, response_placeholder, 'live_first')
        new_entries = encode_history_for_storage(cast(list[ContentOrDict], chat.get_history()[history_len_before:]))
        user_entry, model_entries = split_new_history_entries(new_entries)
        user_msg = session['messages'][-1]
        user_msg['id'] = db.add_message(current_id, 'user', pending_prompt, [user_entry] if user_entry else None, attachments=attachments)
        session['messages'].append(assistant_message)  # pyright: ignore[reportArgumentType]
        st.session_state.chats_count['ai'] += 1
        st.session_state.words_count['ai'] += count_words(assistant_message['message'])
        assistant_message['id'] = db.add_message(
            current_id, 'assistant', assistant_message['message'], model_entries, attachments=assistant_message.get('attachments'), sources=assistant_message.get('sources')
        )
        st.session_state.is_generating = False
        st.rerun()
    except Exception as err:
        st.session_state.chats_count['user'] -= 1
        st.session_state.chats_count['chat_session'] -= 1
        st.session_state.words_count['user'] -= pending_prompt_words
        del st.session_state.chats[current_id]
        db.delete_conversation(current_id)
        st.session_state.is_generating = False
        print(err)
        st.toast(f'Something went wrong: {err}', icon=':material/error:')
        st.switch_page('pages/new_chat.py')
elif has_pending_followup and is_generating:
    followup_prompt = st.session_state.pop('pending_followup')
    followup_prompt_words = count_words(followup_prompt)
    followup_files = st.session_state.pop('pending_followup_files', [])
    followup_attachments = files_to_attachments(followup_files)
    display_user_turn('live_followup', followup_prompt, followup_attachments, is_generating)
    session['messages'].append({'role': 'user', 'message': followup_prompt, 'timestamp': get_timestamp(), 'attachments': followup_attachments})
    db.touch_conversation(current_id)
    st.session_state.chats_count['user'] += 1
    st.session_state.words_count['user'] += followup_prompt_words
    stream_card = st.container(key='ai_card_stream')
    response_placeholder = stream_card.empty()
    response_placeholder.markdown(render_generating_indicator(), unsafe_allow_html=True)
    parts = build_message_parts(followup_prompt, followup_files)
    try:
        history_len_before = len(chat.get_history())
        assistant_message = stream_chat_response(chat, parts, stream_card, response_placeholder, 'live_followup')
        new_entries = encode_history_for_storage(cast(list[ContentOrDict], chat.get_history()[history_len_before:]))
        user_entry, model_entries = split_new_history_entries(new_entries)
        followup_msg = session['messages'][-1]
        followup_msg['id'] = db.add_message(current_id, 'user', followup_prompt, [user_entry] if user_entry else None, attachments=followup_attachments)
        assistant_message['id'] = db.add_message(
            current_id, 'assistant', assistant_message['message'], model_entries, attachments=assistant_message.get('attachments'), sources=assistant_message.get('sources')
        )
        session['messages'].append(assistant_message)  # pyright: ignore[reportArgumentType]
        st.session_state.chats_count['ai'] += 1
        st.session_state.words_count['ai'] += count_words(assistant_message['message'])
        st.session_state.pop('popped_ai_msg', None)
    except Exception as err:
        response_placeholder.empty()
        if session['messages'] and session['messages'][-1]['role'] == 'user':
            session['messages'].pop()
            st.session_state.chats_count['user'] -= 1
            st.session_state.words_count['user'] -= followup_prompt_words
        print(err)
        st.toast(f'Something went wrong: {err}', icon=':material/error:')
        time.sleep(3)
    st.session_state.is_generating = False
    st.rerun()
elif is_pending_regenerate and is_generating:
    st.session_state.pop('pending_regenerate', None)
    last_user_msg = next((m for m in reversed(session['messages']) if m['role'] == 'user'), None)
    regenerate_prompt = last_user_msg['message'] if last_user_msg else ''
    stream_card = st.container(key='ai_card_stream')
    response_placeholder = stream_card.empty()
    response_placeholder.markdown(render_generating_indicator(), unsafe_allow_html=True)
    old_chat = cast(Chat, st.session_state.chats[current_id]['chat'])
    try:
        old_history = cast(list[ContentOrDict], old_chat.get_history())
        last_user_index = next((index for index in range(len(old_history) - 1, -1, -1) if entry_role(old_history[index]) == 'user'), None)
        last_user_content = old_history[last_user_index] if last_user_index is not None else None
        history = old_history[:last_user_index] if last_user_index is not None else []
        chat = get_chat(
            st.session_state.client,
            st.session_state.model,
            st.session_state.temperature,
            st.session_state.max_output_tokens,
            st.session_state.top_k,
            st.session_state.top_p,
            history,
            st.session_state.web_search,
        )
        st.session_state.chats[current_id]['chat'] = chat
        resend_parts = getattr(last_user_content, 'parts', None) or (cast(dict, last_user_content)['parts'] if last_user_content else '')
        history_len_before = len(chat.get_history())
        assistant_message = stream_chat_response(chat, resend_parts, stream_card, response_placeholder, 'live_regen')
        new_entries = encode_history_for_storage(cast(list[ContentOrDict], chat.get_history()[history_len_before:]))
        _, model_entries = split_new_history_entries(new_entries)
        assistant_message['id'] = db.add_message(
            current_id, 'assistant', assistant_message['message'], model_entries, attachments=assistant_message.get('attachments'), sources=assistant_message.get('sources')
        )
        session['messages'].append(assistant_message)  # pyright: ignore[reportArgumentType]
        st.session_state.chats_count['ai'] += 1
        st.session_state.words_count['ai'] += count_words(assistant_message['message'])
    except Exception as err:
        st.session_state.chats[current_id]['chat'] = old_chat
        response_placeholder.empty()
        old_msg = st.session_state.pop('popped_ai_msg', None)
        if old_msg:
            session['messages'].append(old_msg)
            st.session_state.chats_count['ai'] += 1
            st.session_state.words_count['ai'] += count_words(old_msg['message'])
            response_placeholder.markdown(old_msg['message'])
        print(err)
        st.toast(f'Something went wrong: {err}', icon=':material/error:')
        time.sleep(3)
    st.session_state.is_generating = False
    st.rerun()
dock = st.container(key='model_dock')
dock_button_col, dock_select_col = dock.columns([1, 1.6])
web_search_button(dock_button_col, key='web_search_btn_new')
model_selector(dock_select_col, key='model_widget', compact=True)
