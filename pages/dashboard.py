from typing import cast

import pandas as pd
import plotly.express as px
import streamlit as st

from assets.css import RECENT_CONVOS_CSS
from assets.js import DURATION_LIVE_JS
from core import Database
from core.models import IChatsCount, ITodayMessagesCount, IWordsCount
from utils import format_display_timestamp, format_duration

if not st.session_state.is_logged_in:
    st.switch_page('pages/login.py')
db = cast(Database, st.session_state.db)
st.set_page_config('Dashboard', page_icon=':material/dashboard:', layout='wide')
st.markdown('<h1 style="margin-top: -110px;">Dashboard</h1>', unsafe_allow_html=True)
st.caption('<p style="margin-top: -40px;">Analyze your AI conversations and usage statistics.</p>', unsafe_allow_html=True)
st.markdown('<hr style="margin-top: 0px; margin-bottom: 20px; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.3);">', unsafe_allow_html=True)
chats_count = cast(IChatsCount, st.session_state.chats_count)
words_count = cast(IWordsCount, st.session_state.words_count)
try:
    avg = int((words_count['ai'] + words_count['user']) / (chats_count['ai'] + chats_count['user']))
except ZeroDivisionError:
    avg = 0
try:
    today_messages = db.get_today_messages_count(st.session_state.user['id'])
except RuntimeError:
    today_messages: ITodayMessagesCount = {'user': 0, 'ai': 0, 'total': 0}

col1, col2, col3 = st.columns(3)
duration_card = col1.container(border=True, key='duration_metric_card')
duration_card.metric(':material/schedule: DURATION', format_duration(st.session_state.start_time) if st.session_state.start_time else '00:00:00', help="Calculated from the user's last login time.")
if st.session_state.start_time:
    start_epoch_ms = int(st.session_state.start_time.timestamp() * 1000)
    st.html(DURATION_LIVE_JS.format(start_epoch_ms=start_epoch_ms), unsafe_allow_javascript=True)
col2.container(border=True).metric(':material/forum: TOTAL MESSAGES', chats_count['ai'] + chats_count['user'], help='Total messages sent by the user and the AI.')
col3.container(border=True).metric(':material/text_fields: TOTAL WORDS', words_count['ai'] + words_count['user'], help='Total words sent by the user and the AI.')
col1.container(border=True).metric(':material/forum: TOTAL CHAT SESSIONS', chats_count['chat_session'], help='Total chat sessions created.')
col2.container(border=True).metric(':material/today: TODAY TOTAL MESSAGES', today_messages['total'], help='Total messages exchanged today (user and AI).')
col3.container(border=True).metric(':material/person: TODAY USER MESSAGES', today_messages['user'], help='Messages sent by the user today.')
col1.container(border=True).metric(':material/smart_toy: TODAY AI MESSAGES', today_messages['ai'], help='Messages sent by the AI today.')
col2.container(border=True).metric(':material/person: USER MESSAGES', chats_count['user'], help='Total messages sent by the user.')
col3.container(border=True).metric(':material/smart_toy: AI MESSAGES', chats_count['ai'], help='Total messages sent by the AI.')
col1.container(border=True).metric(':material/edit_note: USER WORDS', words_count['user'], help='Total words sent by the user.')
col2.container(border=True).metric(':material/psychology: AI WORDS', words_count['ai'], help='Total words sent by the AI.')
col3.container(border=True).metric(':material/functions: AVERAGE WORDS PER MESSAGE', avg, help='Average number of words per message across both the user and the AI.')
st.write('')
st.markdown(RECENT_CONVOS_CSS, unsafe_allow_html=True)
st.subheader('Recent Conversations')
recent_chats = [(chat_id, data) for chat_id, data in st.session_state.get('chats', {}).items() if data.get('title')][:5]
if not recent_chats:
    st.container(border=True).info('No conversations yet. Start a new chat to see it here.')
else:
    list_container = st.container(border=True)
    for chat_id, chat_data in recent_chats:
        messages = chat_data.get('messages', [])
        message_count = len(messages)
        last_ts = format_display_timestamp(messages[-1]['timestamp']) if messages else '—'
        row = list_container.container(key=f'recent_convo_row_{chat_id}')
        title_col, action_col = row.columns([6, 1])
        title_col.markdown(f'<div class="recent-convo-title">{chat_data["title"]}</div>', unsafe_allow_html=True)
        title_col.markdown(f'<div class="recent-convo-meta">{message_count} messages · {last_ts}</div>', unsafe_allow_html=True)
        if action_col.button('Open', key=f'recent_open_{chat_id}', icon=':material/open_in_new:'):
            st.session_state.current_conversation_id = chat_id
            st.switch_page('pages/chat.py')
        if chat_id != recent_chats[-1][0]:
            row.markdown('<hr style="margin: 6px 0; border: 0; border-top: 1px solid rgba(128,128,128,0.15);">', unsafe_allow_html=True)
if words_count['user'] and words_count['ai']:
    df = pd.DataFrame({'Role': ['User', 'AI'], 'Words': [words_count['user'], words_count['ai']]})
    bar_df = pd.DataFrame({'Metric': ['Chat Sessions', 'Messages'], 'Count': [chats_count['chat_session'], chats_count['user'] + chats_count['ai']]})
    sunburst_df = pd.DataFrame(
        {'Category': ['Messages', 'Messages', 'Words', 'Words'], 'Role': ['User', 'AI', 'User', 'AI'], 'Value': [chats_count['user'], chats_count['ai'], words_count['user'], words_count['ai']]}
    )
    fig_sunburst = px.sunburst(sunburst_df, path=['Category', 'Role'], values='Value', title='Distribution of Messages and Words')
    fig_sunburst.update_traces(textinfo='label+percent entry')
    fig = px.pie(df, names='Role', values='Words', title='Comparison of User and AI words', hole=0.5)
    fig_bar = px.bar(bar_df, x='Metric', y='Count', title='Comparison of Chat Sessions and Total Messages', text='Count')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(xaxis_title=None, yaxis_title='Count')
    st.container(border=True).plotly_chart(fig_sunburst, width='stretch')
    chart_col = st.columns(2)
    chart_col[0].container(border=True).plotly_chart(fig, width='stretch')
    chart_col[1].container(border=True).plotly_chart(fig_bar, width='stretch')
