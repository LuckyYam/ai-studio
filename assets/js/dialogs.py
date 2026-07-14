RENAME_LIVE_WATCHER_JS = """
<script>
(function () {
    function attach() {
        const dialog = document.querySelector('div[data-testid="stDialog"]');
        if (!dialog) return;
        const input = dialog.querySelector('input[type="text"]');
        if (!input || input.__renameWatcherAttached) return;
        input.__renameWatcherAttached = true;
        let timer = null;
        input.addEventListener('input', function () {
            clearTimeout(timer);
            timer = setTimeout(function () {
                const pos = input.selectionStart;
                input.blur();
                input.focus();
                input.setSelectionRange(pos, pos);
            }, 100);
        });
    }
    const observer = new MutationObserver(attach);
    observer.observe(document.body, { childList: true, subtree: true });
    attach();
})();
</script>
"""
