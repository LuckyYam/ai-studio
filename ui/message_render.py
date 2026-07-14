import base64

import streamlit as st
from google.genai.types import ContentOrDict

from core.models import IAttachment, ISource
from utils import get_copy_to_clipboard_iframe_html

from . import preview_attachment_dialog, show_sources_dialog


def needs_dialog_preview(att: IAttachment) -> bool:
    mime = att.get('mime_type', '')
    return bool(att.get('available', True) and att.get('data') and (mime.startswith('video/') or mime == 'application/pdf'))


def render_generating_indicator(label: str = 'Generating response') -> str:
    html_doc = f"""
  <!DOCTYPE html>
  <html>
  <head>
  <meta charset="UTF-8">
  <meta name="color-scheme" content="light dark">
  <style>
    :root {{ color-scheme: light dark; }}
    html, body {{
      margin: 0;
      padding: 0;
      background: transparent !important;
      overflow: hidden;
      font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .wrap {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 18px 4px 4px 4px;
    }}
    .stage {{
      position: relative;
      width: 64px;
      height: 56px;
      cursor: pointer;
      user-select: none;
      flex-shrink: 0;
      -webkit-tap-highlight-color: transparent;
    }}
    .dog-svg {{
      width: 64px;
      height: 56px;
      display: block;
      transform-origin: 50% 70%;
    }}
    .stage.asleep .dog-svg {{
      animation: breathe 2.6s ease-in-out infinite;
    }}
    .stage.awake .dog-svg {{
      animation: shake 0.35s ease-in-out 3;
    }}
    @keyframes breathe {{
      0%, 100% {{ transform: scaleY(1); }}
      50% {{ transform: scaleY(1.05); }}
    }}
    @keyframes shake {{
      0%, 100% {{ transform: rotate(0deg); }}
      25% {{ transform: rotate(-4deg); }}
      75% {{ transform: rotate(4deg); }}
    }}
    .tail {{
      transform-origin: 90% 75%;
      animation: wag 1.8s ease-in-out infinite;
    }}
    .stage.awake .tail {{
      animation: wag-fast 0.25s ease-in-out infinite;
    }}
    @keyframes wag {{
      0%, 100% {{ transform: rotate(0deg); }}
      50% {{ transform: rotate(10deg); }}
    }}
    @keyframes wag-fast {{
      0%, 100% {{ transform: rotate(-8deg); }}
      50% {{ transform: rotate(8deg); }}
    }}
    .eyes-closed, .eyes-open, .brows {{
      transition: opacity 0.15s ease;
    }}
    .stage.asleep .eyes-open, .stage.asleep .brows {{
      opacity: 0;
    }}
    .stage.awake .eyes-closed {{
      opacity: 0;
    }}
    .zzz {{
      position: absolute;
      top: -6px;
      right: -2px;
      font-size: 11px;
      font-weight: 700;
      color: rgba(150,150,150,0.85);
      opacity: 0;
    }}
    .stage.asleep .zzz {{
      animation: float-zzz 2.6s ease-in-out infinite;
    }}
    @keyframes float-zzz {{
      0% {{ transform: translateY(0px); opacity: 0; }}
      20% {{ opacity: 1; }}
      80% {{ opacity: 1; }}
      100% {{ transform: translateY(-10px); opacity: 0; }}
    }}
    .grr {{
      position: absolute;
      top: -14px;
      right: -6px;
      font-size: 13px;
      font-weight: 800;
      color: rgb(255, 90, 90);
      opacity: 0;
      transform: scale(0.6);
      transition: opacity 0.15s ease, transform 0.15s ease;
    }}
    .stage.awake .grr {{
      opacity: 1;
      transform: scale(1);
    }}
    .label {{
      font-size: 0.95rem;
      color: rgba(120,120,120,0.95);
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    @media (prefers-color-scheme: dark) {{
      .label {{ color: #a0a0a0; }}
    }}
    .gen-dots {{
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}
    .gen-dots span {{
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: #4F8BF9;
      display: inline-block;
      animation: gen-bounce 1.2s ease-in-out infinite;
    }}
    .gen-dots span:nth-child(1) {{ animation-delay: 0s; }}
    .gen-dots span:nth-child(2) {{ animation-delay: 0.15s; }}
    .gen-dots span:nth-child(3) {{ animation-delay: 0.3s; }}
    @keyframes gen-bounce {{
      0%, 80%, 100% {{ transform: scale(0.6); opacity: 0.4; }}
      40% {{ transform: scale(1); opacity: 1; }}
    }}
  </style>
  </head>
  <body>
    <div class="wrap">
      <div class="stage asleep" id="dogStage" title="Poke the dog">
        <div class="zzz">Z z z</div>
        <div class="grr">Hmph!</div>
        <svg class="dog-svg" viewBox="0 0 64 56" xmlns="http://www.w3.org/2000/svg">
          <ellipse class="tail" cx="52" cy="40" rx="10" ry="4" fill="#A47B4B"/>
          <ellipse cx="30" cy="40" rx="24" ry="13" fill="#C9A46B"/>
          <ellipse cx="15" cy="26" rx="13" ry="12" fill="#C9A46B"/>
          <path d="M 6 18 Q 0 8 8 6 Q 12 14 10 22 Z" fill="#A47B4B"/>
          <path d="M 22 16 Q 30 6 26 18 Q 22 22 22 16 Z" fill="#A47B4B"/>
          <ellipse cx="8" cy="30" rx="4" ry="3" fill="#3a2b1a"/>
          <g class="eyes-closed">
            <path d="M 12 22 Q 15 25 18 22" stroke="#3a2b1a" stroke-width="1.6" fill="none" stroke-linecap="round"/>
            <path d="M 20 21 Q 23 24 26 21" stroke="#3a2b1a" stroke-width="1.6" fill="none" stroke-linecap="round"/>
          </g>
          <g class="eyes-open">
            <circle cx="15" cy="23" r="2.4" fill="#1a1a1a"/>
            <circle cx="23" cy="22" r="2.4" fill="#1a1a1a"/>
          </g>
          <g class="brows">
            <path d="M 10 18 L 17 20" stroke="#3a2b1a" stroke-width="2" stroke-linecap="round"/>
            <path d="M 27 18 L 20 20" stroke="#3a2b1a" stroke-width="2" stroke-linecap="round"/>
          </g>
        </svg>
      </div>
      <div class="label">
        <span>{label}</span>
        <div class="gen-dots"><span></span><span></span><span></span></div>
      </div>
    </div>
    <script>
      let stage = document.getElementById('dogStage');
      let wakeTimer = null;
      stage.addEventListener('click', () => {{
        stage.classList.remove('asleep');
        stage.classList.add('awake');
        if (wakeTimer) {{ clearTimeout(wakeTimer); }}
        wakeTimer = setTimeout(function () {{
          stage.classList.remove('awake');
          stage.classList.add('asleep');
        }}, 2200);
      }});
    </script>
  </body>
  </html>
  """
    srcdoc = html_doc.replace('"', '&quot;').replace('\n', ' ')
    return (
        f'<iframe srcdoc="{srcdoc}" width="280" height="85" tabindex="-1" '
        'allowtransparency="true" style="border: none; outline: none; background: transparent; '
        'overflow: hidden; display: block; margin: -10px 0 0 -4px;" scrolling="no"></iframe>'
    )


def render_attachment_chip(att: IAttachment) -> str:
    mime = att.get('mime_type', '')
    if mime == 'application/pdf':
        icon, cls, label = 'fa-file-pdf', 'type-pdf', 'PDF'
    elif 'wordprocessing' in mime:
        icon, cls, label = 'fa-file-word', 'type-word', 'WORD'
    elif mime == 'text/csv':
        icon, cls, label = 'fa-file-csv', 'type-csv', 'CSV'
    elif mime.startswith('video/'):
        icon, cls, label = 'fa-file-video', 'type-video', 'VIDEO'
    else:
        icon, cls, label = ('fa-file', 'type-default', mime.split('/')[-1].upper() or 'FILE')
    unavailable = not att.get('available', True)
    name = f'{att["name"]} (unavailable)' if unavailable else att['name']
    opacity_style = ' style="opacity:0.55;"' if unavailable else ''
    return (
        f'<div class="user-att-card"{opacity_style}>'
        f'<div class="user-att-icon {cls}"><i class="fa-solid {icon}"></i></div>'
        f'<div class="user-att-info"><div class="user-att-name">{name}</div>'
        f'<div class="user-att-type">{label}</div></div></div>'
    )


def render_attachment(att: IAttachment) -> str:
    mime = att.get('mime_type', '')
    data = att.get('data')
    available = att.get('available', True)
    if available and data:
        if mime.startswith('image/'):
            return f'<img class="attachment-image" src="data:{mime};base64,{data}" alt="{att["name"]}" />'
        if mime.startswith('audio/'):
            return f'<div class="attachment-media"><audio controls src="data:{mime};base64,{data}"></audio><div class="attachment-caption">{att["name"]}</div></div>'
    return render_attachment_chip(att)


def render_user_message(text: str, attachments: list[IAttachment] | None = None) -> str:
    html_atts = [a for a in (attachments or []) if not needs_dialog_preview(a)]
    rows = [f'<div class="msg-user-row">{render_attachment(a)}</div>' for a in html_atts]
    if text:
        rows.append(f'<div class="msg-user-row"><div class="msg-user-bubble">{text}</div></div>')
    return f'<div class="msg-wrap">{"".join(rows)}</div>'


def render_copy_overlay(text: str) -> str:
    copy_iframe_html = get_copy_to_clipboard_iframe_html(text)
    copy_iframe_srcdoc = copy_iframe_html.replace('"', '&quot;').replace('\n', ' ')
    return (
        f'<div class="msg-ai-copy-overlay"><iframe srcdoc="{copy_iframe_srcdoc}" width="32" height="32" '
        'tabindex="-1" allowtransparency="true" style="border: none; outline: none; background: transparent; '
        'overflow: hidden; display: block;"></iframe></div>'
    )


def render_document_card(container, att: IAttachment, uid: str) -> None:
    mime = att.get('mime_type', '')
    icon = (
        ':material/picture_as_pdf:' if mime == 'application/pdf' else ':material/description:' if 'wordprocessing' in mime else ':material/table_chart:' if mime == 'text/csv' else ':material/draft:'
    )
    fa_icon = (
        'fa-file-pdf icon-pdf' if mime == 'application/pdf' else 'fa-file-word icon-word' if 'wordprocessing' in mime else 'fa-file-csv icon-csv' if mime == 'text/csv' else 'fa-file icon-default'
    )
    card = container.container(key=f'doc_card_{uid}')
    card.markdown(f'<div class="doc-card-name"><i class="fa-solid {fa_icon}"></i>{att["name"]}</div>', unsafe_allow_html=True)
    if att.get('available', True) and att.get('data'):
        raw = base64.b64decode(att['data'])  # pyright: ignore[reportTypedDictNotRequiredAccess]
        card.download_button('Download', data=raw, file_name=att['name'], mime=mime, icon=icon, key=f'doc_dl_{uid}', width='stretch')
    else:
        card.info('This document is no longer available.')


def entry_role(item: ContentOrDict) -> str | None:
    if isinstance(item, dict):
        return item.get('role')
    return getattr(item, 'role', None)


def display_user_turn(uid: str, text: str, attachments: list[IAttachment], disabled: bool = False) -> None:
    dialog_atts = [a for a in attachments if needs_dialog_preview(a)]
    for j, att in enumerate(dialog_atts):
        card_container = st.container(key=f'attcard_{uid}_{j}')
        card_container.markdown(render_attachment_chip(att), unsafe_allow_html=True)
        card_container.button('', key=f'attcard_click_{uid}_{j}', disabled=disabled)
        if st.session_state.get(f'attcard_click_{uid}_{j}'):
            preview_attachment_dialog(att)
    st.markdown(render_user_message(text, attachments), unsafe_allow_html=True)


def render_sources_trigger(uid: str, sources: list[ISource]) -> None:
    if not sources:
        return
    btn_container = st.container(key=f'src_btn_{uid}')
    label = 'Source' if len(sources) == 1 else f'Sources  {len(sources)}'
    if btn_container.button(label, icon=':material/travel_explore:', key=f'src_btn_click_{uid}'):
        show_sources_dialog(sources)
