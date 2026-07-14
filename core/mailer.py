import random
import string

import streamlit as st
from redmail.email.sender import EmailSender


def get_mailer() -> EmailSender:
    smtp = st.secrets['smtp']
    return EmailSender(host=smtp['host'], port=smtp['port'], username=smtp['username'], password=smtp['password'])


def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))


def send_otp_email(to_email: str, otp: str, purpose: str) -> None:
    mailer = get_mailer()
    smtp = st.secrets['smtp']
    if purpose == 'forgot':
        subject = 'Your AI Studio password reset code'
        heading = 'Reset your password'
    else:
        subject = 'Verify your AI Studio account'
        heading = 'Confirm your email'
    mailer.send(
        subject=subject,
        sender=smtp.get('sender', smtp['username']),
        receivers=[to_email],
        html=f"""
            <h2>{heading}</h2>
            <p>Your one-time code is:</p>
            <h1 style='letter-spacing:6px'>{otp}</h1>
            <p>This code expires shortly. If you didn't request this, ignore this email.</p>
        """,
        text=f'{heading}\n\nYour one-time code is: {otp}',
    )
