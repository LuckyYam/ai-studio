from typing import cast

import streamlit as st

from assets.css import AUTH_HTML, HIDE_SIDEBAR_CSS
from assets.js import AUTH_VALIDATION_JS, KUTE_INJECTION
from auth import hash_password, set_auth_cookie, validate_password
from core import Database, generate_otp, send_otp_email

db = cast(Database, st.session_state.db)
st.set_page_config(page_title='Login | AI Studio', layout='centered', page_icon=':material/login:')
st.markdown(HIDE_SIDEBAR_CSS, unsafe_allow_html=True)
st.markdown(AUTH_HTML, unsafe_allow_html=True)
st.html(KUTE_INJECTION, unsafe_allow_javascript=True)
st.html(AUTH_VALIDATION_JS, unsafe_allow_javascript=True)
if st.session_state.get('is_logged_in'):
    st.switch_page('pages/new_chat.py')
mode = st.query_params.get('type', 'login')
row = st.container(key='auth_row')
left_col, right_col = row.columns([1, 1])
if mode == 'register':
    left = left_col.container(key='auth_left')
    left.markdown('<h1>AI Studio</h1>', unsafe_allow_html=True)
    form = left.form('register_form')
    full_name = form.text_input('Full name', value=st.query_params.get('fullname', ''), placeholder='John Doe')
    email = form.text_input('Email', value=st.query_params.get('email', ''), placeholder='john@example.com')
    password = form.text_input('Password', type='password', placeholder='••••••••')
    confirm_password = form.text_input('Confirm password', type='password', placeholder='••••••••')
    submitted = form.form_submit_button('**Register**')
    if submitted:
        if not full_name.strip() or not email.strip() or not password or not confirm_password:
            left.error('All fields are required.')
        elif password != confirm_password:
            left.error('Passwords do not match.')
        elif len(password) < 8:
            left.error('Password must be at least 8 characters.')
        elif db.get_user_by_email(email.strip()):
            left.error('An account with that email already exists.')
        else:
            try:
                password_hash = hash_password(password)
                new_user_id = db.register_user(full_name.strip(), email.strip(), password_hash)
                new_user = db.get_user_by_email(email.strip())
                otp = generate_otp()
                if new_user:
                    send_otp_email(new_user['email'], otp, purpose='register')
                st.session_state.user = new_user
                st.session_state.otp = otp
                st.session_state.verify_purpose = 'register'
                st.query_params.clear()
                st.switch_page('pages/verify.py')
            except RuntimeError as err:
                print(err)
                left.error(str(err))
    right = right_col.container(key='auth_right')
    right.markdown('<h1>Join us.</h1>', unsafe_allow_html=True)
    right.markdown('<p class="subtitle">Create an account to start chatting with AI Studio.</p>', unsafe_allow_html=True)
    right.markdown('<div class="auth-switch-line">Already have an account?</div>', unsafe_allow_html=True)
    if right.button('Log in', key='switch_mode_btn'):
        st.query_params.clear()
        st.query_params['type'] = 'login'
        st.rerun()
elif mode == 'forgot':
    left = left_col.container(key='auth_left')
    left.markdown('<h1>Reset Password</h1>', unsafe_allow_html=True)
    form = left.form('forgot_form')
    email = form.text_input('Email', value=st.query_params.get('email', ''), placeholder='john@example.com')
    submitted = form.form_submit_button('Send OTP')
    if submitted:
        if not email.strip():
            left.error('Enter your email address.')
        else:
            user = db.get_user_by_email(email.strip())
            if not user:
                left.error('No account found with that email address.')
            elif not user['is_active']:
                left.error('This account has been deactivated.')
            else:
                otp = generate_otp()
                send_otp_email(user['email'], otp, purpose='forgot')
                left.success('A reset code has been sent to your email.')
                st.session_state.user = user
                st.session_state.otp = otp
                st.session_state.verify_purpose = 'forgot'
                st.query_params.clear()
                st.switch_page('pages/verify.py')
    right = right_col.container(key='auth_right')
    right.markdown('<h1>Forgot password?</h1>', unsafe_allow_html=True)
    right.markdown('<p class="subtitle">Enter a valid email address and we will help you recover your account.</p>', unsafe_allow_html=True)
    right.markdown('<div class="auth-switch-line">Remembered your password?</div>', unsafe_allow_html=True)
    if right.button('Log in', key='switch_mode_btn'):
        st.query_params.clear()
        st.query_params['type'] = 'login'
        st.rerun()
else:
    left = left_col.container(key='auth_left')
    left.markdown('<h1>AI Studio</h1>', unsafe_allow_html=True)
    form = left.form('login_form')
    email = form.text_input('Email', value=st.query_params.get('email', ''), placeholder='john@example.com')
    password = form.text_input('Password', type='password', placeholder='••••••••')
    remember_row = form.container(key='remember_row')
    remember_me = remember_row.checkbox('Remember me')
    submitted = form.form_submit_button('**Login**')
    if submitted:
        if not email.strip() or not password:
            left.error('Enter your email and password.')
        else:
            user = db.get_user_by_email(email.strip())
            if not user:
                left.error('No account found with that email address.')
            elif not validate_password(password, user['password_hash']):
                left.error('Incorrect password.')
            elif not user['is_active']:
                left.error('This account has been deactivated.')
            elif not user.get('email_verified_at'):
                otp = generate_otp()
                send_otp_email(user['email'], otp, purpose='register')
                st.session_state.user = user
                st.session_state.otp = otp
                st.session_state.verify_purpose = 'register'
                st.query_params.clear()
                st.switch_page('pages/verify.py')
            else:
                db.touch_last_login(user['id'])
                st.session_state.is_logged_in = True
                st.session_state.user = user
                st.session_state.is_loaded = False
                st.session_state.remember_me = remember_me
                set_auth_cookie(user['id'], remember_me)
                st.switch_page('pages/new_chat.py')
                st.rerun()
    right = right_col.container(key='auth_right')
    right.markdown('<h1>Welcome back.</h1>', unsafe_allow_html=True)
    right.markdown('<p class="subtitle">Log in to keep chatting where you left off.</p>', unsafe_allow_html=True)
    if right.button('Forgot password?', key='forgot_btn'):
        st.query_params.clear()
        st.query_params['type'] = 'forgot'
        st.rerun()
    right.markdown('<div class="auth-switch-line">New here?</div>', unsafe_allow_html=True)
    if right.button('Create new account', key='switch_mode_btn'):
        st.query_params.clear()
        st.query_params['type'] = 'register'
        st.rerun()
