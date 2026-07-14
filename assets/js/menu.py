MENU_CLOSE_JS = """
<script>
(function () {
    var doc = window.parent.document;
    var win = window.parent;
    function closeAllExcept(except_) {
        doc.querySelectorAll('details.chat-menu-details[open]').forEach(function (d) {
            if (d !== except_) d.removeAttribute('open');
        });
    }
    function positionChatMenu(details) {
        var menuWrap = details.closest('div[class*="st-key-menu_btn_"]');
        if (!menuWrap) return;
        var actions = menuWrap.querySelector('div[class*="st-key-menu_actions_"]');
        if (!actions) return;
        var summary = details.querySelector('summary');
        var anchorRect = (summary || details).getBoundingClientRect();
        var menuHeight = actions.offsetHeight || 190;
        var buffer = 12;
        var profileCard = doc.querySelector('div[data-testid="stVerticalBlock"][class*="st-key-user_profile_container"]');
        var floor = win.innerHeight;
        if (profileCard) {
            var cardRect = profileCard.getBoundingClientRect();
            if (cardRect.height > 0) floor = cardRect.top;
        }
        var spaceBelow = floor - anchorRect.bottom;
        if (spaceBelow < menuHeight + buffer) {
            actions.classList.add('open-upwards');
        } else {
            actions.classList.remove('open-upwards');
        }
    }
    if (!win.__chatMenuOutsideClickBound) {
        win.__chatMenuOutsideClickBound = true;
        doc.addEventListener('click', function (e) {
            doc.querySelectorAll('details.chat-menu-details[open]').forEach(function (d) {
                if (!d.contains(e.target)) d.removeAttribute('open');
            });
            doc.querySelectorAll('details.user-menu-details[open]').forEach(function (d) {
                if (!d.contains(e.target)) d.removeAttribute('open');
            });
        });
    }
    if (!win.__chatMenuToggleBound) {
        win.__chatMenuToggleBound = true;
        doc.addEventListener('toggle', function (e) {
            var target = e.target;
            if (target.matches && target.matches('details.chat-menu-details')) {
                if (target.open) {
                    closeAllExcept(target);
                    win.requestAnimationFrame(function () {
                        positionChatMenu(target);
                    });
                }
            }
        }, true);
    }
    if (!win.__chatMenuRepositionBound) {
        win.__chatMenuRepositionBound = true;
        var reposition = function () {
            var openDetails = doc.querySelector('details.chat-menu-details[open]');
            if (openDetails) positionChatMenu(openDetails);
        };
        win.addEventListener('scroll', reposition, true);
        win.addEventListener('resize', reposition);
    }
})();
</script>
"""
