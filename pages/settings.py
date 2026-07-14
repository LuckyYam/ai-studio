import streamlit as st

from services import sync_config

if not st.session_state.is_logged_in:
    st.switch_page('pages/login.py')
for key in ('temperature', 'max_output_tokens', 'top_p', 'top_k'):
    st.session_state.setdefault(f'widget_{key}', st.session_state[key])
st.set_page_config('Settings', page_icon=':material/settings:', layout='wide')
st.markdown('<h1 style="margin-top: -110px;">Settings</h1>', unsafe_allow_html=True)
st.caption('<p style="margin-top: -40px;">Configure how the AI generates its answers.</p>', unsafe_allow_html=True)
st.markdown('<hr style="margin-top: 0px; margin-bottom: 20px; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.3);">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
col1.container(border=True).slider(
    'Maximum Output Tokens',
    help='Sets the maximum number of tokens (words and punctuation) the AI can generate in a single response.',
    min_value=128,
    max_value=8192,
    step=128,
    key='widget_max_output_tokens',
    on_change=sync_config,
)
col2.container(border=True).slider(
    'Temperature',
    min_value=0.0,
    max_value=2.0,
    step=0.1,
    format='%.1f',
    key='widget_temperature',
    on_change=sync_config,
    help="Controls the randomness of the AI's responses, with lower values producing more focused outputs and higher values generating more creative ones.",
)
col1.container(border=True).slider(
    'Top P',
    min_value=0.0,
    max_value=1.0,
    format='%.1f',
    step=0.1,
    key='widget_top_p',
    on_change=sync_config,
    help='Restricts the AI to selecting the next token from the smallest group of tokens whose combined probability reaches P, enabling more natural and flexible generation.',
)
col2.container(border=True).slider(
    'Top K',
    min_value=1,
    max_value=64,
    step=1,
    key='widget_top_k',
    on_change=sync_config,
    help='Limits the AI to choosing the next token from the K most likely options, balancing diversity and predictability.',
)
