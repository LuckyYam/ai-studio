SIDEBAR_CSS = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
div[class*="st-key-chat_sidebar_list"][data-testid="stVerticalBlock"],
div[class*="st-key-chat_sidebar_list_pinned"][data-testid="stVerticalBlock"] {
    gap: 0px !important;
    row-gap: 0px !important;
}
div[class*="st-key-chat_sidebar_list"] div[data-testid="stVerticalBlockBorderWrapper"],
div[class*="st-key-chat_sidebar_list_pinned"] div[data-testid="stVerticalBlockBorderWrapper"] {
    gap: 0px !important;
    margin: 0px !important;
}
div[class*="st-key-chat_sidebar_list"] div[data-testid="stElementContainer"],
div[class*="st-key-chat_sidebar_list_pinned"] div[data-testid="stElementContainer"],
div[class*="st-key-chat_sidebar_list"] div[data-testid="element-container"],
div[class*="st-key-chat_sidebar_list_pinned"] div[data-testid="element-container"] {
    margin: 0px !important;
}
div[class*="st-key-chat_row_"] {
    margin: 0px 0px -15px 0px !important;
}
div[class*="st-key-chat_sidebar_list"] div[data-testid="stButton"],
div[class*="st-key-chat_sidebar_list"] div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]),
div[class*="st-key-chat_row_"] div:has(> button) {
    width: 100% !important;
}
div[class*="st-key-chat_row_"] button {
    width: 100% !important;
    display: block !important;
}
div[class*="st-key-chat_sidebar_list"] div[data-testid="stButton"] > button {
    width: 100% !important;
    border: none !important;
    text-align: left !important;
    padding: 6px 34px 6px 12px !important;
    min-height: 32px !important;
    margin: 0px !important;
    display: flex !important;
    justify-content: flex-start !important;
}
div[class*="st-key-chat_sidebar_list"] div[data-testid="stButton"] > button,
div[class*="st-key-chat_sidebar_list"] div[data-testid="stButton"] > button * {
    text-align: left !important;
    justify-content: flex-start !important;
}
div[class*="st-key-chat_sidebar_list"] div[data-testid="stButton"] > button p {
    margin: 0px !important;
    padding: 0px !important;
    font-size: 14px !important;
    width: 100% !important;
    min-width: 0 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
div[class*="st-key-chat_sidebar_list"] div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: transparent !important;
    color: inherit !important;
}
div[class*="st-key-chat_sidebar_list"] div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background-color: rgba(150, 150, 150, 0.15) !important;
}
div[class*="st-key-chat_sidebar_list"] div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #36454F80 !important;
    color: white !important;
}
div[class*="st-key-chat_row_"] {
    position: relative;
}
div[class*="st-key-chat_row_hl_"] button p {
    color: transparent !important;
}
div[data-testid="stElementContainer"]:has(.chat-highlight-overlay) {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    pointer-events: none !important;
    z-index: 10 !important;
}
div[data-testid="stMarkdownContainer"]:has(.chat-highlight-overlay) p,
.chat-highlight-overlay p {
    margin: 0 !important;
    padding: 0 !important;
}
.chat-highlight-overlay {
    position: absolute !important;
    top: -8px !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    height: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    padding: 6px 34px 6px 12px !important;
    font-size: 14px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    pointer-events: none !important;
    color: inherit !important;
}
.chat-highlight-overlay mark {
    background: rgba(79,139,249,0.35);
    color: inherit;
    border-radius: 3px;
    padding: 0 1px;
}
.chat-menu-wrap {
    position: relative;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s ease;
}
div[class*="st-key-chat_row_"]:hover .chat-menu-wrap,
.chat-menu-wrap:has(details[open]) {
    opacity: 1;
    pointer-events: auto;
}
.chat-menu-details {
    position: relative;
}
.chat-menu-dots {
    box-sizing: border-box;
    width: 26px;
    height: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background-color: rgba(30,30,30,0.85);
    color: #FAFAFA;
    font-size: 13px;
    cursor: pointer;
    list-style: none;
    transition: background-color 0.15s ease;
}
.chat-menu-dots::-webkit-details-marker {
    display: none;
}
.chat-menu-dots:hover {
    background-color: rgba(79,139,249,0.35);
}
.chat-menu-dropdown {
    position: absolute;
    top: 30px;
    right: 0;
    min-width: 150px;
    z-index: 999999;
}
div[class*="st-key-menu_btn_"] {
    position: absolute !important;
    top: 35% !important;
    right: 4px !important;
    transform: translateY(-50%) !important;
    width: auto !important;
    height: auto !important;
    margin: 0px !important;
    padding: 0px !important;
    z-index: 50;
}
div[class*="st-key-menu_actions_"] {
    position: absolute;
    top: 30px;
    right: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 170px;
    width: max-content;
    background-color: #1e1f22;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.45);
    padding: 6px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s ease;
    z-index: 999999;
}
div[class*="st-key-menu_actions_"].open-upwards {
    top: auto !important;
    bottom: 30px !important;
}
div[class*="st-key-menu_btn_"]:has(details[open]) div[class*="st-key-menu_actions_"] {
    opacity: 1;
    pointer-events: auto;
}
div[class*="st-key-chat_row_"] div[class*="st-key-menu_actions_"] {
    width: max-content !important;
}
div[class*="st-key-menu_actions_"] div[data-testid="stButton"] > button {
    width: 100% !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 10px !important;
    padding: 10px 12px !important;
    min-height: 0 !important;
    color: #E8EAED !important;
    font-size: 14px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    white-space: nowrap !important;
    text-decoration: none !important;
    gap: 12px !important;
}
div[class*="st-key-menu_actions_"] div[data-testid="stButton"] > button p {
    color: #E8EAED !important;
    text-decoration: none !important;
    font-size: 14px !important;
    white-space: nowrap !important;
}
div[class*="st-key-menu_actions_"] div[data-testid="stButton"] > button svg {
    fill: #E8EAED !important;
    width: 18px !important;
    height: 18px !important;
}
div[class*="st-key-menu_actions_"] div[data-testid="stButton"] > button:hover {
    background-color: rgba(255,255,255,0.08) !important;
}
div[class*="st-key-delete_toggle_"] button,
div[class*="st-key-delete_toggle_"] button p {
    color: #ff6b6b !important;
}
div[class*="st-key-delete_toggle_"] button svg {
    fill: #ff6b6b !important;
}
div[class*="st-key-delete_toggle_"] button:hover {
    background-color: rgba(255,107,107,0.12) !important;
}
.chat-link-skeleton {
    height: 32px !important;
    border-radius: 6px !important;
    background: rgba(150, 150, 150, 0.15) !important;
    margin: 0px 0px 18px 0px !important;
}
.chat-link-typing {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    text-align: left !important;
    width: 100% !important;
    min-height: 32px !important;
    box-sizing: border-box !important;
    padding: 6px 12px !important;
    margin: 0px 0px 18px 0px !important;
    font-size: 14px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    color: inherit !important;
}
[data-testid="stSidebarUserContent"] {
    padding-bottom: 100px !important;
}
div[data-testid="stVerticalBlock"][class*="st-key-user_profile_container"] {
    position: fixed !important;
    z-index: 999999 !important;
    padding: 14px 1.5rem !important;
    border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-sizing: border-box !important;
    margin: 0 !important;
    min-width: 200px !important;
    opacity: 1 !important;
}
.user-profile-wrapper {
    position: relative;
    width: 100%;
}
.user-menu-details {
    position: static;
    width: 100%;
    display: block;
}
.user-profile-card {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 10px 12px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
    cursor: pointer !important;
    list-style: none !important;
    transition: background-color 0.2s ease, border-color 0.2s ease !important;
    width: 100% !important;
    box-sizing: border-box !important;
    pointer-events: auto !important;
}
.user-profile-card::-webkit-details-marker {
    display: none !important;
}
.user-profile-card:hover {
    background-color: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.3) !important; /* Brighter border on hover */
}
.user-avatar {
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    background-color: #D9534F !important;
    color: white !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    flex-shrink: 0 !important;
    letter-spacing: 0.5px !important;
}
.user-info {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    flex-grow: 1;
}
.user-name {
    color: #FAFAFA !important;
    font-size: 14.5px !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1.2 !important;
}
.user-role {
    color: rgba(255,255,255,0.6) !important;
    font-size: 13px !important;
    line-height: 1.2 !important;
    margin-top: 4px !important;
}
div[class*="st-key-user_menu_actions"] {
    position: absolute !important;
    bottom: calc(100% + 5px) !important;
    left: 0 !important;
    right: 0 !important;
    background-color: #1e1f22 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    box-shadow: 0 -4px 24px rgba(0,0,0,0.45) !important;
    padding: 6px !important;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s ease, transform 0.15s ease !important;
    transform: translateY(10px) !important;
    z-index: 999999 !important;
}
.user-menu-details[open] ~ div[class*="st-key-user_menu_actions"],
div[class*="st-key-user_profile_container"]:has(.user-menu-details[open]) div[class*="st-key-user_menu_actions"] {
    opacity: 1 !important;
    pointer-events: auto !important;
    transform: translateY(0) !important;
}
div[class*="st-key-user_menu_actions"] div[data-testid="stButton"] > button {
    width: 100% !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 10px !important;
    padding: 10px 12px !important;
    min-height: 0 !important;
    color: #E8EAED !important;
    font-size: 14px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    gap: 12px !important;
}
div[class*="st-key-user_menu_actions"] div[data-testid="stButton"] > button:hover {
    background-color: rgba(255,255,255,0.08) !important;
}
.user-menu-profile-row {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 8px !important;
    margin-bottom: 6px !important;
}
.user-menu-profile-row .user-info {
    flex-grow: 1;
    overflow: hidden;
}
.user-menu-profile-row .user-name {
    color: #FAFAFA !important;
    font-size: 14.5px !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
.user-menu-profile-row .user-role {
    color: rgba(255,255,255,0.6) !important;
    font-size: 12.5px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
.user-menu-divider {
    border-top: 1px solid rgba(255,255,255,0.08) !important;
    margin: 4px 0 6px 0 !important;
}
</style>
"""
