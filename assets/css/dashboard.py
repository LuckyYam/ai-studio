RECENT_CONVOS_CSS = """
<style>
div[class*="st-key-recent_convo_row_"][data-testid="stVerticalBlock"] {
    padding: 10px 16px !important;
}
div[class*="st-key-recent_convo_row_"] div[data-testid="stHorizontalBlock"] {
    align-items: center !important;
}
div[class*="st-key-recent_convo_row_"] div[data-testid="stButton"] > button {
    width: 100% !important;
}
.recent-convo-title {
    font-weight: 600;
    font-size: 14.5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.recent-convo-meta {
    font-size: 12.5px;
    opacity: 0.65;
    margin-top: 2px;
}
</style>
"""
