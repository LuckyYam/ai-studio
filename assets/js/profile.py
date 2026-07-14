PROFILE_CARD_FIX_JS = """
<script>
(function () {
    var doc = window.parent.document;
    function syncProfileCardPosition() {
        var sidebar = doc.querySelector('[data-testid="stSidebar"]');
        var card = doc.querySelector('div[data-testid="stVerticalBlock"][class*="st-key-user_profile_container"]');
        if (!sidebar || !card) return;
        var rect = sidebar.getBoundingClientRect();
        if (rect.width < 50) return;
        var scrollbarWidth = Math.max(0, sidebar.offsetWidth - sidebar.clientWidth);
        var safeWidth = Math.max(rect.width - scrollbarWidth, 150);
        card.style.left = rect.left + 'px';
        card.style.width = safeWidth + 'px';
        card.style.bottom = (window.parent.innerHeight - rect.bottom) + 'px';
        var sidebarBg = window.parent.getComputedStyle(sidebar).backgroundColor;
        if (sidebarBg && sidebarBg !== 'rgba(0, 0, 0, 0)' && sidebarBg !== 'transparent') {
            card.style.backgroundColor = sidebarBg;
        }
    }
    if (!window.parent.__profileCardSyncBound) {
        window.parent.__profileCardSyncBound = true;
        window.parent.addEventListener('resize', syncProfileCardPosition);
        var sidebarEl = doc.querySelector('[data-testid="stSidebar"]');
        if (sidebarEl && window.parent.ResizeObserver) {
            new window.parent.ResizeObserver(syncProfileCardPosition).observe(sidebarEl);
        }
        new MutationObserver(syncProfileCardPosition).observe(doc.body, { childList: true, subtree: true });
        window.parent.setInterval(syncProfileCardPosition, 400);
    }
    syncProfileCardPosition();
})();
</script>
"""
