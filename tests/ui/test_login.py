from unittest.mock import MagicMock, patch
import streamlit as st
from streamlit.testing.v1 import AppTest
from auth.passwords import hash_password

RUN_TIMEOUT = 15


def _run_login_page(mock_db, *, is_logged_in=False, jwt_secret='test-secret'):
    at = AppTest.from_file('pages/login.py')
    at.session_state['db'] = mock_db
    at.session_state['is_logged_in'] = is_logged_in
    at.session_state['jwt_secret'] = jwt_secret
    at.run(timeout=RUN_TIMEOUT)
    return at


def test_login_form_renders_email_and_password_fields():
    at = _run_login_page(MagicMock())
    assert at.exception == []
    labels = [ti.label for ti in at.text_input]
    assert 'Email' in labels
    assert 'Password' in labels


def test_login_redirects_when_already_logged_in():
    with patch.object(st, 'switch_page', MagicMock()) as mock_switch:
        _run_login_page(MagicMock(), is_logged_in=True)
    mock_switch.assert_called_once_with('pages/new_chat.py')


def test_login_rejects_empty_fields():
    at = _run_login_page(MagicMock())
    email_input, password_input = at.text_input
    email_input.set_value('')
    password_input.set_value('')
    at.button(key='FormSubmitter:login_form-**Login**').click().run(timeout=RUN_TIMEOUT)
    assert [e.value for e in at.error] == ['Enter your email and password.']


def test_login_rejects_unknown_email():
    mock_db = MagicMock()
    mock_db.get_user_by_email.return_value = None
    at = _run_login_page(mock_db)
    email_input, password_input = at.text_input
    email_input.set_value('nobody@example.com')
    password_input.set_value('whatever123')
    at.button(key='FormSubmitter:login_form-**Login**').click().run(timeout=RUN_TIMEOUT)
    assert [e.value for e in at.error] == ['No account found with that email address.']


def test_login_rejects_wrong_password():
    real_hash = hash_password('correctpw')
    mock_db = MagicMock()
    mock_db.get_user_by_email.return_value = {
        'id': 1,
        'email': 'a@b.com',
        'password_hash': real_hash,
        'is_active': True,
        'email_verified_at': '2026-01-01',
    }
    at = _run_login_page(mock_db)
    email_input, password_input = at.text_input
    email_input.set_value('a@b.com')
    password_input.set_value('wrongpass')
    at.button(key='FormSubmitter:login_form-**Login**').click().run(timeout=RUN_TIMEOUT)
    assert [e.value for e in at.error] == ['Incorrect password.']


def test_login_rejects_deactivated_account():
    real_hash = hash_password('correctpw')
    mock_db = MagicMock()
    mock_db.get_user_by_email.return_value = {
        'id': 1,
        'email': 'a@b.com',
        'password_hash': real_hash,
        'is_active': False,
        'email_verified_at': '2026-01-01',
    }
    at = _run_login_page(mock_db)
    email_input, password_input = at.text_input
    email_input.set_value('a@b.com')
    password_input.set_value('correctpw')
    at.button(key='FormSubmitter:login_form-**Login**').click().run(timeout=RUN_TIMEOUT)
    assert [e.value for e in at.error] == ['This account has been deactivated.']


def test_login_sends_otp_for_unverified_email():
    real_hash = hash_password('correctpw')
    mock_db = MagicMock()
    mock_db.get_user_by_email.return_value = {
        'id': 1,
        'email': 'a@b.com',
        'password_hash': real_hash,
        'is_active': True,
        'email_verified_at': None,
    }
    at = _run_login_page(mock_db)
    email_input, password_input = at.text_input
    email_input.set_value('a@b.com')
    password_input.set_value('correctpw')
    with patch.object(st, 'switch_page', MagicMock()) as mock_switch, patch('core.send_otp_email') as mock_send_otp:
        at.button(key='FormSubmitter:login_form-**Login**').click().run(timeout=RUN_TIMEOUT)
    mock_send_otp.assert_called_once()
    mock_switch.assert_called_once_with('pages/verify.py')
    assert at.session_state['verify_purpose'] == 'register'


def test_login_succeeds_with_correct_credentials():
    real_hash = hash_password('correctpw')
    mock_db = MagicMock()
    mock_db.get_user_by_email.return_value = {
        'id': 7,
        'email': 'a@b.com',
        'password_hash': real_hash,
        'is_active': True,
        'email_verified_at': '2026-01-01',
    }
    at = _run_login_page(mock_db)
    email_input, password_input = at.text_input
    email_input.set_value('a@b.com')
    password_input.set_value('correctpw')
    with patch.object(st, 'switch_page', MagicMock()):
        at.button(key='FormSubmitter:login_form-**Login**').click().run(timeout=RUN_TIMEOUT)
    assert at.exception == []
    assert [e.value for e in at.error] == []
    mock_db.touch_last_login.assert_called_once_with(7)
    assert at.session_state['is_logged_in'] is True


def test_switching_to_register_mode_via_query_param():
    at = AppTest.from_file('pages/login.py')
    at.session_state['db'] = MagicMock()
    at.session_state['is_logged_in'] = False
    at.query_params['type'] = 'register'
    at.run(timeout=RUN_TIMEOUT)
    assert at.exception == []
    labels = [ti.label for ti in at.text_input]
    assert 'Full name' in labels
    assert 'Confirm password' in labels


def test_register_rejects_short_password():
    at = AppTest.from_file('pages/login.py')
    at.session_state['db'] = MagicMock()
    at.session_state['is_logged_in'] = False
    at.query_params['type'] = 'register'
    at.run(timeout=RUN_TIMEOUT)
    full_name, email, password, confirm = at.text_input
    full_name.set_value('Full Name')
    email.set_value('fullname@example.com')
    password.set_value('short')
    confirm.set_value('short')
    at.button(key='FormSubmitter:register_form-**Register**').click().run(timeout=RUN_TIMEOUT)
    assert [e.value for e in at.error] == ['Password must be at least 8 characters.']


def test_register_rejects_mismatched_passwords():
    at = AppTest.from_file('pages/login.py')
    at.session_state['db'] = MagicMock()
    at.session_state['is_logged_in'] = False
    at.query_params['type'] = 'register'
    at.run(timeout=RUN_TIMEOUT)
    full_name, email, password, confirm = at.text_input
    full_name.set_value('Full Name')
    email.set_value('fullname@example.com')
    password.set_value('longenough1')
    confirm.set_value('longenough2')
    at.button(key='FormSubmitter:register_form-**Register**').click().run(timeout=RUN_TIMEOUT)
    assert [e.value for e in at.error] == ['Passwords do not match.']
