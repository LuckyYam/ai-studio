import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from core import GEMINI_2_MODELS, MODELS
from services import on_model_change, update_chat


def model_selector(container: DeltaGenerator, key: str = 'model_widget', compact: bool = False) -> None:
    options = list(MODELS.keys())
    container.selectbox(
        'Model',
        options=options,
        index=options.index(st.session_state.model),
        format_func=lambda key: MODELS[key],
        key=key,
        on_change=on_model_change,
        label_visibility='collapsed' if compact else 'visible',
    )


def web_search_button(container: DeltaGenerator, key: str = 'web_search_btn') -> None:
    active = st.session_state.get('web_search', False)
    if container.button('Web Search', key=key, icon=':material/travel_explore:', type='primary' if active else 'secondary'):
        if active:
            st.session_state.web_search = False
        else:
            st.session_state.web_search = True
            if st.session_state.model not in GEMINI_2_MODELS:
                st.session_state.model = GEMINI_2_MODELS[0]
                st.session_state.model_widget = GEMINI_2_MODELS[0]
        update_chat()
        st.rerun()
