from datetime import datetime
from typing import cast

import streamlit as st

from assets.css import MODEL_DOCK_CSS
from assets.js import DOCK_ALIGN_JS
from core import SUPPORTED_FILE_EXTENSIONS, Database, get_chat
from core.models import IUser
from ui import model_selector, web_search_button
from utils import generate_conversation_id

if not st.session_state.is_logged_in:
    st.switch_page('pages/login.py')
db = cast(Database, st.session_state.db)

examples = [
    {
        'icon': 'fa-solid fa-terminal',
        'title': 'Explain Python Decorators',
        'caption': 'Deep Dive into functional programming concepts and syntax.',
        'prompt': 'Explain Python decorators, how they work, and show me a practical example.',
    },
    {
        'icon': 'fa-solid fa-database',
        'title': 'Optimize an SQL query',
        'caption': 'Improve performance of complex joins and nested subqueries.',
        'prompt': 'Help me optimize a complex SQL query with joins and nested subqueries.',
    },
    {
        'icon': 'fa-solid fa-file-lines',
        'title': 'Summarize an article',
        'caption': 'Extract key insights and bullet points from any long-form text.',
        'prompt': 'Summarize the following article into key insights and bullet points.',
    },
    {
        'icon': 'fa-solid fa-laptop-code',
        'title': 'Generate Streamlit code',
        'caption': 'Build rapid dashboards with clean Python implementation.',
        'prompt': 'Generate clean Streamlit Python code for a simple dashboard.',
    },
]

st.set_page_config('New chat - AI Studio', layout='wide', page_icon=':material/add_comment:')
st.markdown(
    """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
.example-card {
    display: block;
    border: 1px solid rgba(49, 51, 63, 0.2);
    border-radius: 0.5rem;
    padding: 16px 20px;
    height: 150px;
    text-decoration: none !important;
    color: inherit !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    cursor: pointer;
}
.example-card:hover {
    transform: scale(1.04);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    border-color: rgba(49, 51, 63, 0.4);
    z-index: 2;
}
.example-card .card-icon {
    font-size: 22px;
    margin-bottom: 6px;
}
.example-card .card-title {
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 4px;
}
.example-card .card-caption {
    font-size: 13px;
    color: rgba(49, 51, 63, 0.7);
    margin: 0;
}
.example-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}
</style>
""",
    unsafe_allow_html=True,
)
user = cast(IUser, st.session_state.user)
first_name = user['full_name'].split(' ')[0]
current_hour = datetime.now().hour

st.markdown(MODEL_DOCK_CSS, unsafe_allow_html=True)
st.html(DOCK_ALIGN_JS, unsafe_allow_javascript=True)
subheader_column, _ = st.columns([8, 3])

if current_hour < 12:
    greeting = 'Morning'
elif current_hour < 18:
    greeting = 'Afternoon'
else:
    greeting = 'Evening'

st.markdown('<h1 style="margin-top: -150px;">AI Studio</h1>', unsafe_allow_html=True)
st.markdown('<hr style="margin-top: -50px; margin-bottom: 20px; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.3);">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; margin-top: 80px; margin-bottom: 60px;">
        <p style="font-family: 'Helvetica Neue', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 300; font-size: 1.5rem; opacity: 0.7; letter-spacing: 0.02em; margin: 0;">
            {greeting}, {first_name}. What would you like to work on today?
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
card_blocks = []
for i, ex in enumerate(examples):
    card_blocks.append(
        f'<a class="example-card" href="?example={i}" target="_self"><div class="card-icon"><i class="{ex["icon"]}"></i></div><div class="card-title">{ex["title"]}</div><p class="card-caption">{ex["caption"]}</p></a>'
    )
cards_html = '<div class="example-grid">' + ''.join(card_blocks) + '</div>'
st.markdown(cards_html, unsafe_allow_html=True)
st.write('')
st.write('')
st.write('')

dock = st.container(key='model_dock')
dock_button_col, dock_select_col = dock.columns([1, 1.6])
web_search_button(dock_button_col, key='web_search_btn_new')
model_selector(dock_select_col, key='model_widget', compact=True)
prompt_value = st.chat_input('Ask me anything...', accept_file=True, max_upload_size=15, file_type=SUPPORTED_FILE_EXTENSIONS)

prompt_text = prompt_value.text if prompt_value else None
prompt_files = prompt_value.files if prompt_value else []
clicked_prompt = None
example_param = st.query_params.get('example')

if example_param is not None:
    try:
        index = int(example_param)
        clicked_prompt = examples[index]['prompt']
    except (ValueError, IndexError):
        pass
    st.query_params.clear()

final_prompt = clicked_prompt or prompt_text
final_files = [] if clicked_prompt else prompt_files

if (final_prompt and final_prompt.strip()) or final_files:
    try:
        chat = get_chat(
            st.session_state.client,
            st.session_state.model,
            st.session_state.temperature,
            st.session_state.max_output_tokens,
            st.session_state.top_k,
            st.session_state.top_p,
            web_search=st.session_state.web_search,
        )
        conversation_id = generate_conversation_id()
        db.create_conversation(conversation_id, user['id'], 'New Chat', st.session_state.model)
        new_chat_data = {'title': None, 'messages': [], 'chat': chat}
        st.session_state.chats = {conversation_id: new_chat_data, **st.session_state.chats}
        st.session_state.pending_prompt = final_prompt or ''
        st.session_state.pending_files = final_files
        st.session_state.pending_chat_id = conversation_id
        st.session_state.chats_count['chat_session'] += 1
        st.session_state.current_conversation_id = conversation_id
        st.switch_page('pages/chat.py')
    except RuntimeError as err:
        print(err)
        st.error(f'Something went wrong: {str(err)}')
