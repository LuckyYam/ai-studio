EXPORT_FORMAT_CSS = """
<style>
div[class*="st-key-export_fmt_card_"][data-testid="stVerticalBlock"] {
    position: relative !important;
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 12px;
    padding: 24px 18px 20px 18px !important;
    min-height: 96px !important;
    margin-bottom: -4px;
    background: transparent;
    box-sizing: border-box !important;
    transition: background 0.15s ease, border-color 0.15s ease;
}
div[class*="st-key-export_fmt_card_"][data-testid="stVerticalBlock"]:has(.export-fmt-radio.checked) {
    background: rgba(79,139,249,0.08);
    border-color: #4F8BF9;
}
div[class*="st-key-export_fmt_card_"] div[data-testid="stHorizontalBlock"] {
    align-items: center !important;
    gap: 14px;
}
.export-fmt-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    border: 1px solid rgba(128,128,128,0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    background: rgba(128,128,128,0.05);
}
.export-fmt-title {
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 2px;
}
.export-fmt-desc {
    font-size: 13px;
    opacity: 0.75;
    line-height: 1.4;
}
.export-fmt-radio {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 2px solid rgba(128,128,128,0.4);
    flex-shrink: 0;
    box-sizing: border-box;
    position: relative;
    margin-left: 24px;
}
.export-fmt-radio.checked {
    border-color: #4F8BF9;
}
.export-fmt-radio.checked::after {
    content: '';
    position: absolute;
    top: 3px;
    left: 3px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #4F8BF9;
}
div[class*="st-key-export_fmt_click_"] {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    z-index: 10 !important;
    margin: 0 !important;
    padding: 0 !important;
}
div[class*="st-key-export_fmt_click_"] button {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 10px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    cursor: pointer !important;
    padding: 0 !important;
    margin: 0 !important;
}
div[class*="st-key-export_dialog_actions"] div[data-testid="stButton"] > button,
div[class*="st-key-export_dialog_actions"] div[data-testid="stDownloadButton"] > button {
    min-height: 48px !important;
    height: 48px !important;
    padding: 12px 16px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    box-sizing: border-box !important;
    margin-top: 30px !important;
}
div[class*="st-key-export_dialog_actions"] div[data-testid="stButton"] > button p,
div[class*="st-key-export_dialog_actions"] div[data-testid="stDownloadButton"] > button p {
    margin: 0 !important;
    line-height: 1 !important;
}
div[class*="st-key-export_dialog_actions"] div[data-testid="stDownloadButton"] > button[kind="primary"] {
    background-color: #1a2744 !important;
    border-color: #1a2744 !important;
    color: #ffffff !important;
}
div[class*="st-key-export_dialog_actions"] div[data-testid="stDownloadButton"] > button[kind="primary"]:hover {
    background-color: #24325a !important;
    border-color: #24325a !important;
}
.json-icon {
    font-style: normal;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
.json-icon::before {
    content: "{ }";
    font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-weight: 400;
    letter-spacing: -1px;
    font-size: 1.1em;
}
</style>
"""

RENAME_DIALOG_CSS = """
<style>
div[class*="st-key-rename_dialog_actions"] div[data-testid="stButton"] > button {
    min-height: 42px !important;
    height: 42px !important;
    padding: 8px 22px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    box-sizing: border-box !important;
    margin-top: 20px !important;
    white-space: nowrap !important;
}
div[class*="st-key-rename_dialog_actions"] div[data-testid="stButton"] > button p {
    margin: 0 !important;
    line-height: 1 !important;
    white-space: nowrap !important;
}
div[class*="st-key-rename_dialog_actions"] div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #1a2744 !important;
    border-color: #1a2744 !important;
    color: #ffffff !important;
}
div[class*="st-key-rename_dialog_actions"] div[data-testid="stButton"] > button[kind="primary"]:hover:not(:disabled) {
    background-color: #24325a !important;
    border-color: #24325a !important;
}
div[class*="st-key-rename_dialog_actions"] div[data-testid="stButton"] > button[kind="primary"]:disabled {
    background-color: rgba(128,128,128,0.25) !important;
    border-color: rgba(128,128,128,0.25) !important;
    color: rgba(255,255,255,0.55) !important;
    cursor: not-allowed !important;
}
</style>
"""
