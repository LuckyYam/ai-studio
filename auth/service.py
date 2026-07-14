import time

import streamlit as st
from streamlit_cookies_controller import CookieController

from core import AUTH_COOKIE_NAME, JWT_EXPIRY_DAYS_DEFAULT, JWT_EXPIRY_DAYS_REMEMBERED

from .tokens import create_auth_token

cookie_controller = CookieController()


def set_auth_cookie(user_id: int, remember_me: bool = False):
    token = create_auth_token(st.session_state.jwt_secret, str(user_id), remember_me)
    days = JWT_EXPIRY_DAYS_REMEMBERED if remember_me else JWT_EXPIRY_DAYS_DEFAULT
    cookie_controller.set(AUTH_COOKIE_NAME, token, max_age=days * 24 * 60 * 60, path='/')
    time.sleep(0.2)


def logout():
    st.session_state.is_logged_in = False
    del st.session_state.user
    try:
        cookie_controller.remove(AUTH_COOKIE_NAME)
    except KeyError:
        st.html(
            f"""
            <script>
            (function () {{
                document.cookie = "{AUTH_COOKIE_NAME}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax";
                window.parent.location.reload();
            }})();
            </script>
        """,
            unsafe_allow_javascript=True,
        )
    keys_to_clear = ['is_loaded', 'otp', 'verify_purpose', 'otp_confirmed', 'remember_me']
    for key in keys_to_clear:
        st.session_state.pop(key, None)
    time.sleep(0.2)
