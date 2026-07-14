KUTE_INJECTION = """
<script>
(function () {
  try {
    var parentWin = window.parent;
    var parentDoc = parentWin.document;
    function animateCurves() {
      var KUTE = parentWin.KUTE;
      if (KUTE && parentDoc.querySelector('#curve-top-2')) {
        KUTE.fromTo(
          parentDoc.querySelector('#curve-top-2'),
          { path: '#curve-top-1' },
          { path: '#curve-top-2' },
          { repeat: 999, duration: 2600, yoyo: true }
        ).start();

        KUTE.fromTo(
          parentDoc.querySelector('#curve-bottom-2'),
          { path: '#curve-bottom-1' },
          { path: '#curve-bottom-2' },
          { repeat: 999, duration: 2600, yoyo: true }
        ).start();
      }
    }
    if (!parentWin.kuteInjected) {
      parentWin.kuteInjected = true;
      if (!parentDoc.getElementById('kute-cdn-script')) {
        var script = parentDoc.createElement('script');
        script.id = 'kute-cdn-script';
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/kute.js/2.1.2/kute.min.js';
        script.onload = function () {
          setTimeout(animateCurves, 100);
        };
        parentDoc.head.appendChild(script);
      } else {
        setTimeout(animateCurves, 100);
      }
    } else {
      setTimeout(animateCurves, 100);
    }
  } catch (e) {
    console.warn('KUTE injection skipped:', e);
  }
})();
</script>
"""
AUTH_VALIDATION_JS = """
<script>
(function () {
  try {
    var parentWin = window.parent;
    var parentDoc = parentWin.document;
    var EMAIL_REGEX = /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/;
    var MIN_PASSWORD_LENGTH = 8;
    function ensureErrorEl(input, className) {
      var wrapper = input.closest('[data-testid="stTextInput"]');
      if (!wrapper) return null;
      var err = wrapper.querySelector('.' + className);
      if (!err) {
        err = parentDoc.createElement('div');
        err.className = className;
        wrapper.appendChild(err);
      }
      return err;
    }
    function setError(err, message) {
      if (!err) return;
      err.textContent = message || '';
      err.style.display = message ? 'block' : 'none';
    }
    function isConfirmField(input) {
      return (input.getAttribute('aria-label') || '').toLowerCase().indexOf('confirm') !== -1;
    }
    function isPasswordField(input) {
      var label = (input.getAttribute('aria-label') || '').toLowerCase();
      return label.indexOf('password') !== -1 && label.indexOf('confirm') === -1;
    }
    function validateEmail(input) {
      var value = input.value.trim();
      var err = ensureErrorEl(input, 'field-live-error');
      if (!value) {
        input.classList.remove('field-live-invalid');
        setError(err, '');
        return;
      }
      var valid = EMAIL_REGEX.test(value);
      input.classList.toggle('field-live-invalid', !valid);
      setError(err, valid ? '' : 'Enter a valid email address.');
    }
    function findConfirmPasswordInput(passwordInput) {
      var form = passwordInput.closest('[data-testid="stForm"]');
      if (!form) return null;
      var candidates = form.querySelectorAll('input[type="password"]');
      for (var i = 0; i < candidates.length; i++)
        if (isConfirmField(candidates[i])) return candidates[i];
      return null;
    }
    function findPasswordInput(confirmInput) {
      var form = confirmInput.closest('[data-testid="stForm"]');
      if (!form) return null;
      var candidates = form.querySelectorAll('input[type="password"]');
      for (var i = 0; i < candidates.length; i++)
        if (isPasswordField(candidates[i])) return candidates[i];
      return null;
    }
    function validatePassword(input) {
      var value = input.value;
      var err = ensureErrorEl(input, 'field-live-error');
      var messages = [];
      if (value && value.length < MIN_PASSWORD_LENGTH)
        messages.push('Password must be at least ' + MIN_PASSWORD_LENGTH + ' characters.');
      input.classList.toggle('field-live-invalid', messages.length > 0);
      setError(err, messages[0] || '');
      var confirmInput = findConfirmPasswordInput(input);
      if (confirmInput) validateConfirmPassword(confirmInput);
    }
    function validateConfirmPassword(input) {
      var value = input.value;
      var err = ensureErrorEl(input, 'field-live-error');
      var messages = [];
      if (value && value.length < MIN_PASSWORD_LENGTH) {
        messages.push('Password must be at least ' + MIN_PASSWORD_LENGTH + ' characters.');
      }
      var passwordInput = findPasswordInput(input);
      if (value && passwordInput && passwordInput.value && value !== passwordInput.value) {
        messages.push('Passwords do not match.');
      }
      input.classList.toggle('field-live-invalid', messages.length > 0);
      setError(err, messages[0] || '');
    }
    function attach() {
      parentDoc.querySelectorAll('input[aria-label="Email"]').forEach(function (input) {
        if (input.dataset.liveValidationBound) return;
        input.dataset.liveValidationBound = 'true';
        input.addEventListener('input', function () { validateEmail(input); });
        input.addEventListener('blur', function () { validateEmail(input); });
        validateEmail(input);
      });
      parentDoc.querySelectorAll('input[type="password"]').forEach(function (input) {
        if (input.dataset.liveValidationBound) return;
        input.dataset.liveValidationBound = 'true';
        if (isConfirmField(input)) {
          input.addEventListener('input', function () { validateConfirmPassword(input); });
          input.addEventListener('blur', function () { validateConfirmPassword(input); });
        } else {
          input.addEventListener('input', function () { validatePassword(input); });
          input.addEventListener('blur', function () { validatePassword(input); });
        }
      });
    }
    function injectStyle() {
      if (parentDoc.getElementById('field-live-validation-style')) return;
      var style = parentDoc.createElement('style');
      style.id = 'field-live-validation-style';
      style.textContent =
        'input.field-live-invalid { border-color: #e5484d !important; ' +
        'box-shadow: 0 0 0 2px rgba(229, 72, 77, 0.15) !important; }' +
        '.field-live-error { display: none; color: #e5484d; ' +
        'font-family: "Work Sans", sans-serif; font-size: 0.8rem; margin-top: 4px; }';
      parentDoc.head.appendChild(style);
    }
    injectStyle();
    attach();
    if (!parentWin.liveValidationObserverAttached) {
      parentWin.liveValidationObserverAttached = true;
      new MutationObserver(attach).observe(parentDoc.body, { childList: true, subtree: true });
    }
  } catch (e) {
    console.warn('Live validation injection skipped:', e);
  }
})();
</script>
"""
