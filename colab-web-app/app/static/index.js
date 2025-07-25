// static/js/index.js

document.addEventListener('DOMContentLoaded', () => {
  const form       = document.getElementById('userForm');
  const input      = document.getElementById('userInput');
  const responseEl = document.getElementById('responseText');
  const submitBtn  = form?.querySelector('button[type="submit"]');

  if (!form || !input || !responseEl || !submitBtn) {
    console.error('Missing required DOM elements for index.js');
    return;
  }

  form.addEventListener('submit', handleSubmit);

  async function handleSubmit(event) {
    event.preventDefault();

    const value = input.value.trim();
    clearResponse();

    if (!value) {
      showError('Please enter a command or link.');
      return;
    }

    setLoading(true);

    try {
      const res = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ user_input: value })
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || `Server returned ${res.status}`);
      }

      showSuccess(data.message);
      console.log('Server responded:', data);

    } catch (err) {
      console.error('Request failed:', err);
      showError(err.message || 'An unexpected error occurred.');

    } finally {
      setLoading(false);
    }
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.textContent = isLoading ? 'Sending…' : 'Submit';
  }

  function clearResponse() {
    responseEl.textContent = '';
    responseEl.classList.remove('error', 'success');
  }

  function showError(msg) {
    responseEl.textContent = msg;
    responseEl.classList.add('error');
  }

  function showSuccess(msg) {
    responseEl.textContent = msg;
    responseEl.classList.add('success');
  }
});
