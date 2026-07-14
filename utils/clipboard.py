import json


def get_copy_to_clipboard_iframe_html(text_to_copy: str) -> str:
    escaped = json.dumps(text_to_copy)
    return f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="color-scheme" content="light dark">
            <meta http-equiv="Content-Security-Policy" content="frame-ancestors 'self' *">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <style>
                :root {{ color-scheme: light dark; }}
                html, body {{
                    margin: 0;
                    padding: 0;
                    background: transparent !important;
                    height: 100%;
                    overflow: hidden;
                }}
                #copyButton {{
                    box-sizing: border-box;
                    width: 32px;
                    height: 32px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    padding: 0;
                    border-radius: 50%;
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    background-color: transparent;
                    color: #31333F;
                    font-size: 14px;
                    cursor: pointer;
                    transition: border-color 0.2s, color 0.2s;
                }}
                @media (prefers-color-scheme: dark) {{
                    #copyButton {{
                        background-color: #262730;
                        color: #FAFAFA;
                        border: 1px solid rgba(250, 250, 250, 0.2);
                    }}
                }}
                #copyButton:hover {{
                    border-color: rgb(255, 75, 75);
                    color: rgb(255, 75, 75);
                }}
                #copyButton:active {{
                    background-color: rgb(255, 75, 75);
                    color: rgb(255, 255, 255);
                }}
            </style>
        </head>
        <body>
            <button id="copyButton" onclick="copyToClipboard()" title="Copy response">
                <i id="copyIcon" class="fa-regular fa-clipboard"></i>
            </button>
            <script>
                const copyIcon = document.getElementById('copyIcon');
                async function copyToClipboard() {{
                    try {{
                        await navigator.clipboard.writeText({escaped});
                    }} catch (e) {{
                        console.error('Copy failed', e);
                    }}
                    copyIcon.className = 'fa-solid fa-check';
                    setTimeout(function () {{
                        copyIcon.className = 'fa-regular fa-clipboard';
                    }}, 1000);
                }}
            </script>
        </body>
        </html>
        """


def get_menu_close_iframe_html() -> str:
    return """
        <html>
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="Content-Security-Policy" content="frame-ancestors 'self' *">
            <style>
                html, body {
                    margin: 0;
                    padding: 0;
                    background: transparent !important;
                    height: 100%;
                    overflow: hidden;
                }
            </style>
        </head>
        <body>
            <script>
                (() => {
                    try {
                        const doc = window.parent.document;
                        if (!doc.__chatMenuOutsideClickBound) {
                            doc.__chatMenuOutsideClickBound = true;
                            doc.addEventListener('click', (e) => {
                                doc.querySelectorAll('details.chat-menu-details[open]').forEach((d) => {
                                    if (!d.contains(e.target)) {
                                        d.removeAttribute('open');
                                    }
                                });
                            });
                        }
                        if (!doc.__chatMenuToggleBound) {
                            doc.__chatMenuToggleBound = true;
                            doc.addEventListener('toggle', (e) => {
                                const target = e.target;
                                if (target.matches && target.matches('details.chat-menu-details') && target.open) {
                                    doc.querySelectorAll('details.chat-menu-details[open]').forEach((d) => {
                                        if (d !== target) {
                                            d.removeAttribute('open');
                                        }
                                    });
                                }
                            }, true);
                        }
                    } catch (err) {
                        console.error('chat menu script error', err);
                    }
                })();
            </script>
        </body>
        </html>
    """
