DOCK_ALIGN_JS = """
<script>
(function() {
  function getDoc() {
    try {
      if (window.parent && window.parent.document) return window.parent.document;
    } catch (e) {}
    return document;
  }
  function alignDock() {
    const doc = getDoc();
    const chatInput = doc.querySelector('[data-testid="stChatInput"]');
    const dock = doc.querySelector('[class*="st-key-model_dock"]');
    if (!chatInput || !dock) return;
    const inputRect = chatInput.getBoundingClientRect();
    const dockRect = dock.getBoundingClientRect();
    const left = inputRect.right - dockRect.width;
    const top = inputRect.top - dockRect.height - 10; // 10px gap above chat input
    dock.style.left = left + 'px';
    dock.style.top = top + 'px';
    dock.style.right = 'auto';
    dock.style.bottom = 'auto';
  }
  const doc = getDoc();
  const win = doc.defaultView || window;
  win.addEventListener('resize', alignDock);
  const observer = new MutationObserver(() => alignDock());
  observer.observe(doc.body, { childList: true, subtree: true });
  alignDock();
  setTimeout(alignDock, 100);
  setTimeout(alignDock, 400);
  setTimeout(alignDock, 1000);
})();
</script>
"""
