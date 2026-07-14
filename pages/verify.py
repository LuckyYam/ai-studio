import time
from typing import cast

import streamlit as st

from assets.css import AUTH_HTML, HIDE_SIDEBAR_CSS
from assets.js import AUTH_VALIDATION_JS, KUTE_INJECTION
from auth import hash_password, set_auth_cookie
from core import Database, generate_otp, send_otp_email

db = cast(Database, st.session_state.db)
st.set_page_config(page_title='Verify your email · AI Studio', layout='centered', page_icon=':material/mark_email_read:')
st.markdown(HIDE_SIDEBAR_CSS, unsafe_allow_html=True)
st.markdown(AUTH_HTML, unsafe_allow_html=True)
st.html(AUTH_VALIDATION_JS, unsafe_allow_javascript=True)
st.html(KUTE_INJECTION, unsafe_allow_javascript=True)
if st.session_state.get('is_logged_in'):
    st.switch_page('pages/new_chat.py')
if 'user' not in st.session_state:
    st.switch_page('pages/login.py')
verify_purpose = st.session_state.get('verify_purpose')
if verify_purpose not in ('register', 'forgot'):
    st.switch_page('pages/new_chat.py')
user = st.session_state.user
email = user['email']
is_forgot_password = verify_purpose == 'forgot'
row = st.container(key='auth_row')
left_col, right_col = row.columns([1, 1])
left = left_col.container(key='auth_left')
left.markdown('<h1>Verification</h1>', unsafe_allow_html=True)
if is_forgot_password:
    left.markdown(f'<p class="subtitle">We have sent a password reset OTP to <b>{email}</b>. Please enter it below.</p>', unsafe_allow_html=True)
else:
    left.markdown(f'<p class="subtitle">We have sent an activation OTP to <b>{email}</b>. Please enter it below.</p>', unsafe_allow_html=True)
awaiting_new_password = is_forgot_password and st.session_state.get('otp_confirmed', False)
if not awaiting_new_password:
    form = left.form('verify_form')
    otp = form.text_input('Enter OTP Code', placeholder='• • • • • •')
    submitted = form.form_submit_button('Verify Code')
    if submitted:
        if not otp.strip():
            left.error('Please enter the OTP.')
        elif otp.strip() != st.session_state.get('otp'):
            left.error('Invalid or expired OTP.')
        elif verify_purpose == 'register':
            db.mark_email_verified(user['id'])
            st.session_state.is_logged_in = True
            st.session_state.is_loaded = False
            set_auth_cookie(user['id'], remember_me=False)
            st.session_state.pop('otp', None)
            st.session_state.pop('verify_purpose', None)
            st.switch_page('pages/new_chat.py')
        else:
            st.session_state.otp_confirmed = True
            st.rerun()
else:
    form = left.form('reset_password_form')
    new_password = form.text_input('New password', type='password', placeholder='••••••••')
    confirm_password = form.text_input('Confirm new password', type='password', placeholder='••••••••')
    submitted = form.form_submit_button('Reset password')
    if submitted:
        if not new_password or not confirm_password:
            left.error('All fields are required.')
        elif new_password != confirm_password:
            left.error('Passwords do not match.')
        elif len(new_password) < 8:
            left.error('Password must be at least 8 characters.')
        else:
            password_hash = hash_password(new_password)
            db.update_password(user['id'], password_hash)
            for key in ('otp', 'verify_purpose', 'otp_confirmed', 'user'):
                st.session_state.pop(key, None)
            st.toast('Password updated. Please log in with your new password.')
            time.sleep(3)
            st.switch_page('pages/login.py')
right = right_col.container(key='auth_right')
right.markdown('<h1>Check Inbox.</h1>', unsafe_allow_html=True)
right.markdown('<p class="subtitle">Check your email and spam folder for the one-time passcode to securely access your account.</p>', unsafe_allow_html=True)
right.markdown('<div class="auth-switch-line">Did not receive the email?</div>', unsafe_allow_html=True)
if right.button('Resend Code', key='switch_mode_btn_1'):
    new_otp = generate_otp()
    st.session_state.otp = new_otp
    send_otp_email(email, new_otp, purpose=verify_purpose)
    st.toast('Verification code resent!')
right.markdown('<div class="auth-switch-line">Entered the wrong email?</div>', unsafe_allow_html=True)
if right.button('Back to login', key='switch_mode_btn_2'):
    for key in ('otp', 'verify_purpose', 'otp_confirmed', 'user'):
        st.session_state.pop(key, None)
    st.switch_page('pages/login.py')
