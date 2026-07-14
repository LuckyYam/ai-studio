AUTH_HTML = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
@import url("https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700&display=swap");
:root {
  --bg-main: #ffffff;
  --bg-panel: #f8f9fa;
  --text-primary: #2d3139;
  --text-secondary: #6c757d;
  --accent-color: rgba(45, 49, 57, 0.05);
  --accent-text: #2d3139;
  --auth-left-bg: var(--bg-panel);
  --auth-right-bg: var(--bg-main);
  --auth-curve-color: var(--bg-panel);
  --auth-input-bg: var(--bg-main);
  --auth-input-border: #dee2e6;
  --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg-main: #0f1115;
    --bg-panel: #1a1d24;
    --text-primary: #ffffff;
    --text-secondary: #a1a1aa;
    --accent-color: rgba(255, 255, 255, 0.05);
    --accent-text: #ffffff;
    --auth-left-bg: var(--bg-panel);
    --auth-right-bg: var(--bg-main);
    --auth-curve-color: var(--bg-panel);
    --auth-input-bg: var(--bg-main);
    --auth-input-border: #2a2d36;
    --card-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.25);
  }
}
html, body {
  background-color: var(--bg-main) !important;
  font-family: "Work Sans", Arial, Helvetica, sans-serif !important;
  color: var(--text-primary) !important;
}
.stApp, [data-testid="stAppViewContainer"], .main, .block-container, header[data-testid="stHeader"] {
  background: transparent !important;
  background-color: transparent !important;
}
header[data-testid="stHeader"], #MainMenu, footer { display: none !important; }
.block-container {
  max-width: 850px !important;
  padding-top: 5rem !important;
  padding-bottom: 3rem !important;
  position: relative;
  z-index: 10;
}
.curve-wrapper {
  position: fixed;
  left: 0;
  width: 100vw;
  overflow: hidden;
  line-height: 0;
  z-index: -999;
  pointer-events: none;
}
.top-curve-layout { top: 0; }
.bottom-curve-layout { bottom: 0; transform: rotate(180deg); }
.curve-wrapper svg {
  position: relative;
  display: block;
  width: calc(100% + 1.3px);
  height: 120px;
}
.shape-fill { fill: var(--auth-curve-color); transition: fill 0.3s ease; }
div[class*="st-key-auth_row"] {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
div[class*="st-key-auth_row"] div[data-testid="stHorizontalBlock"] {
  align-items: stretch !important;
  gap: 0 !important;
  border-radius: 12px !important;
  box-shadow: var(--card-shadow) !important;
  overflow: hidden !important;
  border: 1px solid var(--auth-input-border) !important;
  background-color: var(--bg-main) !important;
}
div[data-testid="InputInstructions"] {
  display: none !important;
}
div[class*="st-key-auth_row"] div[data-testid="column"] {
  width: 50% !important;
  flex: 1 1 50% !important;
  min-width: 50% !important;
  padding: 0 !important;
  margin: 0 !important;
}
div[class*="st-key-auth_left"],
div[class*="st-key-auth_right"] {
  width: 100% !important;
  height: 560px !important;
  min-height: 560px !important;
  max-height: 560px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  align-items: stretch;
  transition: background-color 0.3s ease;
  box-sizing: border-box !important;
}
div[class*="st-key-auth_left"] {
  background-color: var(--auth-left-bg);
  padding: 3rem 2.5rem;
}
div[class*="st-key-auth_left"] h1 {
  font-family: "Work Sans", sans-serif;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 24px;
  text-align: center;
  white-space: nowrap;
  font-size: 2.1rem;
}
div[class*="st-key-auth_right"] {
  background-color: var(--auth-right-bg);
  padding: 3rem 2.5rem;
}
div[class*="st-key-auth_right"] h1 {
  font-family: "Work Sans", sans-serif;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 12px;
  white-space: nowrap;
  font-size: 2.1rem;
}
div[class*="st-key-auth_right"] p.subtitle {
  font-family: "Work Sans", sans-serif;
  font-weight: 400;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.6;
  font-size: 1rem;
}
div[data-testid="stForm"] {
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stCheckbox"] label p {
  font-family: "Work Sans", sans-serif !important;
  font-weight: 500 !important;
  color: var(--text-secondary) !important;
  font-size: 0.9rem !important;
}
div[data-testid="stTextInput"] input {
  padding: 10px !important;
  background-color: var(--auth-input-bg) !important;
  border: 1px solid var(--auth-input-border) !important;
  border-radius: 8px !important;
  font-family: "Work Sans", sans-serif !important;
  color: var(--text-primary) !important;
  transition: all 0.2s ease;
}
div[data-testid="stTextInput"] input:focus {
  border-color: var(--text-secondary) !important;
  box-shadow: 0 0 0 2px rgba(161, 161, 170, 0.2) !important;
}
div[data-testid="stTextInput"] { margin-bottom: 0.8rem; }
div[data-testid="stFormSubmitButton"] button {
  background-color: transparent !important;
  border: 2px dashed var(--text-primary) !important;
  border-radius: 5px !important;
  font-family: "Work Sans", sans-serif !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  width: 100% !important;
  margin-top: 1rem !important;
  padding: 8px 16px !important;
  transition: all 0.2s ease-in-out;
}
div[data-testid="stFormSubmitButton"] button:hover {
  border: 2px double var(--text-primary) !important;
  background-color: var(--accent-color) !important;
}
div[data-testid="stFormSubmitButton"] button:focus:not(:active) {
    outline: none !important;
    border-color: var(--text-primary) !important;
}
div[class*="st-key-remember_row"] { margin-top: 0.2rem; }
div[class*="st-key-forgot_btn"] button,
div[class*="st-key-switch_mode_btn"] button {
  background: none !important;
  border: none !important;
  color: var(--text-primary) !important;
  font-family: "Work Sans", sans-serif !important;
  font-weight: 500 !important;
  padding: 0 !important;
  box-shadow: none !important;
  text-align: left !important;
  justify-content: flex-start !important;
  font-size: 0.95rem !important;
  transition: opacity 0.2s;
}
div[class*="st-key-forgot_btn"] button:hover,
div[class*="st-key-switch_mode_btn"] button:hover {
  text-decoration: underline;
  opacity: 0.8;
}
.auth-switch-line {
  color: var(--text-secondary);
  font-family: "Work Sans", sans-serif;
  font-weight: 500;
  margin-top: 1.8rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}
div[data-testid="stCheckbox"] {
    align-items: center;
}
@media only screen and (max-width: 640px) {
  div[class*="st-key-auth_row"] div[data-testid="stHorizontalBlock"] {
      flex-direction: column !important;
  }
  div[class*="st-key-auth_row"] div[data-testid="column"] {
      width: 100% !important;
      flex: 1 1 100% !important;
      min-width: 100% !important;
  }
  div[class*="st-key-auth_left"] {
    height: auto !important;
    min-height: 400px !important;
  }
  div[class*="st-key-auth_right"] {
    border-top: 1px solid var(--auth-input-border) !important;
    height: auto !important;
    min-height: 350px !important;
  }
}
</style>
<div class="curve-wrapper top-curve-layout">
  <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
    <path id="curve-top-1" d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" class="shape-fill" style="visibility: hidden;"></path>
    <path id="curve-top-2" d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" class="shape-fill"></path>
    <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" class="shape-fill"></path>
  </svg>
</div>
<div class="curve-wrapper bottom-curve-layout">
  <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
    <path id="curve-bottom-1" d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" class="shape-fill" style="visibility: hidden;"></path>
    <path id="curve-bottom-2" d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" class="shape-fill"></path>
    <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" class="shape-fill"></path>
  </svg>
</div>
"""
HIDE_SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"] {
    display: none;
}
[data-testid="collapsedControl"] {
    display: none;
}
</style>
"""
