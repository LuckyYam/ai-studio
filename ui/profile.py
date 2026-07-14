import streamlit as st

from assets.js import PROFILE_CARD_FIX_JS
from auth import logout


def _display_name(name: str, limit: int = 16) -> str:
    name = (name or '').strip()
    return name if len(name) <= limit else name[:limit].rstrip() + '...'


def render_user_profile():
    user = st.session_state.user or {}
    user_name = user.get('full_name', 'User')
    user_email = user.get('email', '')
    initials = ''.join([n[0] for n in user_name.split()[:2]]).upper() or 'U'
    display_name = _display_name(user_name)
    profile_container = st.sidebar.container(key='user_profile_container')
    profile_html = f"""
    <div class="user-profile-wrapper">
        <details class="user-menu-details">
            <summary class="user-profile-card">
                <div class="user-avatar">{initials}</div>
                <div class="user-info">
                    <div class="user-name">{display_name}</div>
                    <div class="user-role">USER</div>
                </div>
            </summary>
            <div class="user-menu-dropdown"></div>
        </details>
    </div>
    """
    profile_container.markdown(profile_html, unsafe_allow_html=True)
    st.html(PROFILE_CARD_FIX_JS, unsafe_allow_javascript=True)
    menu_actions = profile_container.container(key='user_menu_actions')
    menu_actions.markdown(
        f"""
        <div class="user-menu-profile-row">
            <div class="user-avatar">{initials}</div>
            <div class="user-info">
                <div class="user-name">{display_name}</div>
                <div class="user-role">{user_email}</div>
            </div>
        </div>
        <div class="user-menu-divider"></div>
        """,
        unsafe_allow_html=True,
    )
    if menu_actions.button('Log out', icon=':material/logout:', width='stretch', key='logout_btn'):
        logout()
