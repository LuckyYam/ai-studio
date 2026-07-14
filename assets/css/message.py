MESSAGE_CSS = """
<style>
.msg-wrap {
  width: 100%;
}
.msg-user-row {
  display: flex;
  justify-content: flex-end;
  margin: 4px 0 4px 0;
}
.msg-wrap .msg-user-row:last-child {
  margin-bottom: 18px;
}
.msg-user-bubble {
  background: rgba(128,128,128,0.16);
  color: inherit;
  padding: 10px 18px;
  border-radius: 22px;
  max-width: 70%;
  word-wrap: break-word;
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 15px;
}
.msg-ai-copy-overlay {
  position: absolute;
  bottom: 0px;
  right: -10px;
  width: 32px;
  height: 32px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s ease;
  z-index: 5;
}
[class*="st-key-ai_msg_"]:has(div[data-testid="stButton"]) .msg-ai-copy-overlay {
  bottom: -16px;
}
[class*="st-key-ai_msg_"]:hover .msg-ai-copy-overlay,
[class*="st-key-ai_card_stream"]:hover .msg-ai-copy-overlay {
  opacity: 1;
  pointer-events: auto;
}
.msg-ai-copy-overlay iframe {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
}
[class*="st-key-ai_msg_"],
[class*="st-key-ai_card_stream"] {
  position: relative;
  border: 1px solid rgba(128,128,128,0.3);
  border-radius: 16px;
  padding: 14px 18px 16px 18px !important;
  margin: 4px 0 28px 0;
  box-sizing: border-box;
  overflow: visible !important;
}
[class*="st-key-ai_msg_"] p,
[class*="st-key-ai_card_stream"] p {
  line-height: 1.5;
  margin: 0 0 14px 0;
}
[class*="st-key-ai_msg_"] p:last-child,
[class*="st-key-ai_card_stream"] p:last-child {
  margin-bottom: 0;
}
[class*="st-key-ai_msg_"] ul,
[class*="st-key-ai_msg_"] ol,
[class*="st-key-ai_card_stream"] ul,
[class*="st-key-ai_card_stream"] ol {
  margin: 6px 0 14px 0;
  padding-left: 24px;
}
[class*="st-key-ai_msg_"] li,
[class*="st-key-ai_card_stream"] li {
  margin-bottom: 6px;
}
[class*="st-key-ai_msg_"] div[data-testid="element-container"]:has(.msg-ai-copy-overlay),
[class*="st-key-ai_msg_"] div[data-testid="element-container"]:has(.msg-ai-copy-overlay),
[class*="st-key-ai_msg_"] div[data-testid="element-container"]:has(div[data-testid="stButton"]) {
  position: static !important;
  height: 0px !important;
  min-height: 0px !important;
  width: 0px !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: visible !important;
}
[class*="st-key-ai_msg_"][class*="st-key-ai_msg_"] div[data-testid="stButton"] {
  position: absolute !important;
  bottom: 16px !important;
  right: 45px !important;
  left: auto !important;
  width: 32px !important;
  height: 32px !important;
  margin: 0 !important;
  padding: 0 !important;
  opacity: 0;
  transition: opacity 0.15s ease;
  z-index: 5;
}
[class*="st-key-ai_msg_"]:hover div[data-testid="stButton"] {
  opacity: 1;
}
[class*="st-key-ai_msg_"] div[data-testid="stButton"] button {
  width: 32px !important;
  height: 32px !important;
  min-width: 32px !important;
  min-height: 32px !important;
  border-radius: 50% !important;
  padding: 0 !important;
  box-sizing: border-box !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background-color: transparent !important;
  border: 1px solid currentColor !important;
  color: var(--text-color) !important;
  box-shadow: none !important;
  transition: border-color 0.2s, color 0.2s, background-color 0.2s;
}
[class*="st-key-ai_msg_"] div[data-testid="stButton"] button:hover {
  border-color: rgb(255, 75, 75) !important;
  color: rgb(255, 75, 75) !important;
  background-color: rgba(255, 75, 75, 0.1) !important;
}
[class*="st-key-ai_msg_"] div[data-testid="stButton"] button:active {
  background-color: rgb(255, 75, 75) !important;
  color: rgb(255, 255, 255) !important;
  border-color: rgb(255, 75, 75) !important;
  box-shadow: none !important;
}
[class*="st-key-ai_msg_"] div[data-testid="stButton"] button:focus:not(:active) {
  box-shadow: none !important;
  border-color: currentColor !important;
}
[class*="st-key-ai_msg_"] div[data-testid="stButton"] button p,
[class*="st-key-ai_msg_"] div[data-testid="stButton"] button span[data-testid="stIconMaterial"] {
  margin: 0 !important;
  font-size: 15px !important;
  line-height: 1 !important;
}
[class*="st-key-ai_card_stream"] div[data-testid="stButton"] {
  display: none !important;
}
[class*="st-key-ai_msg_"] > div[data-testid="stVerticalBlock"],
[class*="st-key-ai_card_stream"] > div[data-testid="stVerticalBlock"] {
  gap: 0 !important;
}
.attachment-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(128,128,128,0.12);
  border: 1px solid rgba(128,128,128,0.3);
  border-radius: 12px;
  padding: 6px 12px;
  font-size: 13px;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--text-color);
}
.attachment-chip i {
  color: rgba(128,128,128,0.8);
}
.attachment-chip.unavailable {
  opacity: 0.55;
  text-decoration: line-through;
  background: rgba(128,128,128,0.08);
  border-color: rgba(128,128,128,0.2);
}
.attachment-chip.unavailable i {
  color: inherit;
}
.attachment-image {
  max-width: 260px;
  max-height: 260px;
  border-radius: 14px;
  display: block;
  object-fit: cover;
}
.attachment-media {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}
.attachment-media audio {
  width: 280px;
  height: 40px;
}
.attachment-caption {
  font-size: 12px;
  color: rgba(128,128,128,0.9);
  background: rgba(128,128,128,0.12);
  border: 1px solid rgba(128,128,128,0.3);
  border-radius: 10px;
  padding: 3px 10px;
  max-width: 320px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
[class*="st-key-ai_msg_"] div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]) {
  position: static !important;
  width: auto !important;
  height: auto !important;
}
</style>
"""
ATTACHMENT_BUTTON_CSS = """
<style>
div[class*="st-key-attcard_"][data-testid="stVerticalBlock"] {
    position: relative !important;
    display: inline-block !important;
    width: auto !important;
    height: auto !important;
    margin-left: auto !important;
    margin-bottom: -17px !important;
}
div[class*="st-key-attcard_"][data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:not([class*="attcard_click_"]),
div[class*="st-key-attcard_"][data-testid="stVerticalBlock"] div[data-testid="stMarkdown"],
div[class*="st-key-attcard_"][data-testid="stVerticalBlock"] div[data-testid="stMarkdownContainer"] {
    position: static !important;
    display: block !important;
    height: auto !important;
    width: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
}
div[class*="st-key-attcard_"][data-testid="stVerticalBlock"] div[data-testid="stMarkdown"] {
    pointer-events: none !important;
}
div[class*="st-key-attcard_click_"] {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    z-index: 10 !important;
    margin: 0 !important;
    padding: 0 !important;
}
div[class*="st-key-attcard_click_"] div[data-testid="stButton"],
div[class*="st-key-attcard_click_"] button {
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
    border-radius: 12px !important;
}
div[class*="st-key-attcard_click_"] button:disabled {
    cursor: not-allowed !important;
    pointer-events: none !important;
}
</style>
"""
USER_ATTACHMENT_CARD_CSS = """
<style>
.user-att-card {
    display: flex;
    align-items: center;
    gap: 12px;
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 12px;
    padding: 10px 16px;
    background: rgba(128,128,128,0.05);
    max-width: 320px;
    position: relative;
}
.user-att-icon {
    width: 36px;
    height: 36px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: #fff;
    font-size: 16px;
}
.user-att-icon.type-pdf   { background: #e3242b; }
.user-att-icon.type-word  { background: #2b579a; }
.user-att-icon.type-csv   { background: #21a366; }
.user-att-icon.type-video { background: #e0459a; }
.user-att-icon.type-default { background: #808080; }
.user-att-info {
    display: flex;
    flex-direction: column;
    overflow: hidden;
}
.user-att-name {
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.user-att-type {
    font-size: 12px;
    opacity: 0.6;
    text-transform: uppercase;
}
</style>
"""
SOURCES_BUTTON_CSS = """
<style>
div[class*="st-key-src_btn_"][data-testid="stVerticalBlock"] {
  display: flex !important;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  margin: 0 0 -10px 0;
  gap: 0 !important;
}
div[class*="st-key-src_btn_"] button {
  background: rgba(13, 148, 136, 0.1) !important;
  border: 1px solid rgba(13, 148, 136, 0.35) !important;
  border-radius: 12px !important;
  padding: 5px 12px !important;
  font-size: 12.5px !important;
  color: inherit !important;
  box-shadow: none !important;
  white-space: nowrap !important;
}
div[class*="st-key-src_btn_"] button:hover {
  background: rgba(13, 148, 136, 0.2) !important;
  border-color: rgba(13, 148, 136, 0.6) !important;
}
div[class*="st-key-src_btn_"] button span[data-testid="stIconMaterial"] {
  color: #0d9488 !important;
}
.source-item {
  display: block;
  padding: 10px 0;
  border-bottom: 1px solid rgba(128,128,128,0.2);
}
.source-item:last-child {
  border-bottom: none;
}
.source-title {
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  color: inherit;
}
.source-host {
  font-size: 12px;
  opacity: 0.6;
  margin-top: 2px;
}
</style>
"""
DOCUMENT_CARD_CSS = """
<style>
div[class*="st-key-doc_card_"] {
  border: 1px solid rgba(128,128,128,0.25);
  border-radius: 12px;
  padding: 16px;
  margin: 10px 0 6px 0;
  background: rgba(128,128,128,0.05);
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}
.doc-card-name {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  word-break: break-word;
}
.doc-card-name i {
  font-size: 18px;
}
.icon-pdf { color: #e3242b; }
.icon-word { color: #2b579a; }
.icon-csv { color: #21a366; }
.icon-default { color: #808080; }

div[class*="st-key-doc_card_"] div[data-testid="stButton"] button,
div[class*="st-key-doc_card_"] div[data-testid="stDownloadButton"] button {
  width: 100% !important;
  background: rgba(128,128,128,0.08) !important;
  border: 1px solid rgba(128,128,128,0.25) !important;
  color: inherit !important;
  box-shadow: none !important;
  border-radius: 8px !important;
}
div[class*="st-key-doc_card_"] div[data-testid="stDownloadButton"] button:hover {
  background: rgba(128,128,128,0.15) !important;
  border-color: rgba(128,128,128,0.4) !important;
}
</style>
"""
