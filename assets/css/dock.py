MODEL_DOCK_CSS = """
<style>
[class*="st-key-model_dock"] {
    position: fixed;
    width: 300px;
    z-index: 999;
    transition: left 0.1s ease-out, top 0.1s ease-out;
}
[class*="st-key-model_dock"] div[data-testid="stHorizontalBlock"] {
    gap: 8px;
    align-items: center;
    justify-content: flex-end;
}
[class*="st-key-model_dock"] div[data-baseweb="select"] {
    min-height: 32px !important;
}
[class*="st-key-model_dock"] div[data-baseweb="select"] > div {
    font-size: 12px !important;
    font-weight: 400 !important;
    padding-top: 2px !important;
    padding-bottom: 2px !important;
    min-height: 32px !important;
    border-radius: 8px !important;
}
[class*="st-key-model_dock"] svg {
    width: 14px !important;
    height: 14px !important;
}
[class*="st-key-model_dock"] div[data-testid="stButton"] button {
    height: 32px !important;
    padding: 0 10px !important;
    border-radius: 8px !important;
    white-space: nowrap !important;
    margin-top: 2px !important;
}
[class*="st-key-model_dock"] div[data-testid="stButton"] button,
[class*="st-key-model_dock"] div[data-testid="stButton"] button p {
    font-size: 12px !important;
    font-family: inherit !important;
    font-weight: 400 !important;
    line-height: 1 !important;
    margin: 0 !important;
}
[class*="st-key-model_dock"] div[data-testid="stButton"] button[kind="primary"] {
    background-color: #5AC8E0 !important;
    border-color: #5AC8E0 !important;
    color: #1a1a1a !important;
}
[class*="st-key-model_dock"] div[data-testid="stButton"] button[kind="primary"]:hover {
    background-color: #9ecbe0 !important;
    border-color: #9ecbe0 !important;
    color: #1a1a1a !important;
}
[class*="st-key-model_dock"] div[data-testid="stButton"] {
    position: relative;
    left: 10px;
}
</style>
"""
