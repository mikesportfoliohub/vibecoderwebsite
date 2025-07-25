// static/js/login.js

document.addEventListener('DOMContentLoaded', () => {
  const form        = document.getElementById('loginForm');
  const emailInput  = document.getElementById('loginEmail');
  const passInput   = document.getElementById('loginPassword');
  const msgEl       = document.getElementById('loginResponse');
  const submitBtn   = form?.querySelector('button[type="submit"]');

  // The template must set this before loading login.js:
  // <script>window.nextPage = "{{ next_page }}";</script>
  const NEXT_PAGE       = window.nextPage || '';
  const LOGIN_URL_BASE  = `${HOME_URL}auth/login`;
  const DEFAULT_TARGET  = `${HOME_URL}dashboard`;

  if (!form || !emailInput || !passInput || !msgEl || !submitBtn) {
    console.error('Login JS: missing required DOM elements');
    return;
  }

  form.addEventListener('submit', handleLogin);

  async function handleLogin(evt) {
    evt.preventDefault();
    clearMessage();

    const email    = emailInput.value.trim();
    const password = passInput.value;

    if (!email || !password) {
      showError('Email and password are required.');
      return;
    }

    setLoading(true);

    try {
      // Build the POST URL with ?next= if needed
      const url = NEXT_PAGE
        ? `${LOGIN_URL_BASE}?next=${encodeURIComponent(NEXT_PAGE)}`
        : LOGIN_URL_BASE;

      const res  = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || `Login failed (status ${res.status})`);
      }

      showSuccess(data.message);
      console.log('Login successful:', data);

      // After a brief pause, redirect to:
      // 1) data.next (returned by server)
      // 2) fallback to NEXT_PAGE (template param)
      // 3) otherwise to /dashboard
      setTimeout(() => {
        const target = data.next || NEXT_PAGE || DEFAULT_TARGET;
        window.location.href = target;
      }, 800);

    } catch (err) {
      console.error('Login error:', err);
      showError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  }

  function setLoading(flag) {
    submitBtn.disabled    = flag;
    submitBtn.textContent = flag ? 'Logging in…' : 'Login';
  }

  function clearMessage() {
    msgEl.textContent           = '';
    msgEl.classList.remove('error', 'success');
  }

  function showError(text) {
    msgEl.textContent       = text;
    msgEl.classList.add('error');
  }

  function showSuccess(text) {
    msgEl.textContent       = text;
    msgEl.classList.add('success');
  }
});
