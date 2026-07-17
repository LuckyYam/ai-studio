from typing import Literal, cast

import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from google.genai.types import ContentOrDict

from auth import cookie_controller, decode_auth_token
from core import AUTH_COOKIE_NAME, DEFAULTS, Database, get_chat, load_config
from core.models import ISession, IUser
from ui import render_chat_list, render_user_profile
from utils import decode_history_from_storage, mark_attachments_unavailable

if 'db' not in st.session_state:
    st.session_state.db = Database(
        host=st.secrets['mysql']['host'],
        port=st.secrets['mysql'].get('port', 3306),
        user=st.secrets['mysql']['user'],
        password=st.secrets['mysql']['password'],
        database=st.secrets['mysql']['database'],
    )
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value
if 'user' not in st.session_state:
    st.session_state.user = None
if 'client' not in st.session_state:
    try:
        config = load_config()
        if 'jwt_secret' not in st.session_state:
            st.session_state.jwt_secret = config['JWT_SECRET']
        st.session_state.client = genai.Client(api_key=config['GEMINI_API_KEY'])
        st.session_state.client.models.list()
    except ClientError as err:
        print(err)
        st.error(str(err))
        st.stop()
    except RuntimeError as err:
        print(err)
        st.error(str(err))
        st.stop()
    except Exception as err:
        print(err)
        st.error(f'Unexpected exception: {str(err)}')
        st.stop()
if not st.session_state.is_logged_in:
    token = None
    if hasattr(st, 'context') and hasattr(st.context, 'cookies'):
        token = st.context.cookies.get(AUTH_COOKIE_NAME)
    else:
        token = cookie_controller.get(AUTH_COOKIE_NAME)
    if token:
        payload = decode_auth_token(st.session_state.jwt_secret, token)
        if payload is not None:
            db = cast(Database, st.session_state.db)
            user = db.get_user_by_id(int(payload['sub']))
            if user and user.get('is_active'):
                st.session_state.is_logged_in = True
                st.session_state.user = user
            else:
                cookie_controller.remove(AUTH_COOKIE_NAME)
        else:
            cookie_controller.remove(AUTH_COOKIE_NAME)
if st.session_state.is_logged_in and 'user' in st.session_state and not st.session_state.is_loaded:
    try:
        data = st.session_state.db.load_data(cast(int, cast(IUser, st.session_state.user)['id']))
        client = cast(genai.Client, st.session_state.client)
        if data:
            st.session_state['model'] = data['model']
            st.session_state['temperature'] = data['temperature']
            st.session_state['max_output_tokens'] = data['max_output_tokens']
            st.session_state['top_p'] = data['top_p']
            st.session_state['top_k'] = data['top_k']
            st.session_state['chats_count'] = data['chats_count']
            st.session_state['words_count'] = data['words_count']
            st.session_state['start_time'] = data['start_time']
            st.session_state['web_search'] = data['web_search']
            st.session_state['pinned'] = data['pinned']
            chats: dict[str, ISession] = {}
            for chat_id, saved_session in data['chats'].items():
                try:
                    history_raw = decode_history_from_storage(cast(list[dict], saved_session['history']))
                    history = cast(list[ContentOrDict], [types.Content.model_validate(c) for c in history_raw])
                    chat_obj = get_chat(
                        client, cast(Literal['gemini-2.5-flash'], data['model']), data['temperature'], data['max_output_tokens'], data['top_k'], data['top_p'], history, st.session_state.web_search
                    )
                    messages = saved_session['messages']
                except Exception as err:
                    st.toast(f'Could not restore attachments for "{saved_session.get("title") or chat_id}": {err}', icon=':material/warning:')
                    chat_obj = client.chats.create(model=data['model'], history=[])
                    messages = mark_attachments_unavailable(saved_session['messages'])
                chats[chat_id] = {'title': saved_session['title'], 'messages': messages, 'chat': chat_obj}
            st.session_state['chats'] = chats
            st.session_state.is_loaded = True
    except RuntimeError as err:
        st.toast(f'Failed loading the data: {str(err)}')
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

new_chat_page = st.Page('pages/new_chat.py', title='New Chat', icon=':material/add_comment:')
dashboard_page = st.Page('pages/dashboard.py', title='Dashboard', icon=':material/dashboard:')
settings_page = st.Page('pages/settings.py', title='Settings', icon=':material/settings:')
chat_page = st.Page('pages/chat.py', title='Chat', icon=':material/chat:', url_path='chat')
login_page = st.Page('pages/login.py', title='Login')
verify_page = st.Page('pages/verify.py', title='Verify')
nav = st.navigation([new_chat_page, chat_page, dashboard_page, settings_page, login_page, verify_page], position='hidden')
if st.session_state.is_logged_in:
    st.sidebar.markdown('<p style="font-weight: 800; font-size: 24px; margin-top: -45px; padding-top: 10px;"><strong>AI STUDIO</strong></p>', unsafe_allow_html=True)
    st.sidebar.caption('<p style="margin-top: -25px;">v2.4 Pro</p>', unsafe_allow_html=True)
    st.sidebar.write('')
    st.sidebar.page_link(new_chat_page, label='New Chat', icon=':material/add_comment:')
    st.sidebar.page_link(dashboard_page, label='Dashboard', icon=':material/dashboard:')
    st.sidebar.page_link(settings_page, label='Settings', icon=':material/settings:')
    render_chat_list(is_on_chat_page=(nav is chat_page))
    render_user_profile()
nav.run()
