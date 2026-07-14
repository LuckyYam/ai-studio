DURATION_LIVE_JS = """
<script>
(function () {{
    var startEpoch = {start_epoch_ms};
    function pad(n) {{ return String(n).padStart(2, '0'); }}
    function formatDuration(diffSeconds) {{
        if (diffSeconds < 0) diffSeconds = 0;
        var days = Math.floor(diffSeconds / 86400);
        var hours = Math.floor((diffSeconds % 86400) / 3600);
        var minutes = Math.floor((diffSeconds % 3600) / 60);
        var seconds = Math.floor(diffSeconds % 60);
        if (days >= 1) {{
            return pad(days) + ':' + pad(hours) + ':' + pad(minutes) + ':' + pad(seconds);
        }}
        return pad(hours) + ':' + pad(minutes) + ':' + pad(seconds);
    }}
    function tick() {{
        var el = document.querySelector('div[class*="st-key-duration_metric_card"] [data-testid="stMetricValue"]');
        if (!el) return;
        var diff = (Date.now() - startEpoch) / 1000;
        el.textContent = formatDuration(diff);
    }}
    if (window.__durationTickInterval) {{
        clearInterval(window.__durationTickInterval);
    }}
    tick();
    window.__durationTickInterval = setInterval(tick, 1000);
}})();
</script>
"""
