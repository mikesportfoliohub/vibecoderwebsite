// static/js/register.js

document.addEventListener('DOMContentLoaded', () => {
  const form         = document.getElementById('registerForm');
  const usernameInput= document.getElementById('username');
  const emailInput   = document.getElementById('email');
  const passInput    = document.getElementById('password');
  const msgEl        = document.getElementById('registerResponse');
  const showBtn      = document.getElementById('showUsers');
  const usersList    = document.getElementById('usersList');
  const submitBtn    = form?.querySelector('button[type="submit"]');
  const REGISTER_URL = `${HOME_URL}auth/register_user`;
  const USERS_URL    = `${HOME_URL}auth/get_users`;

  if (!form || !usernameInput || !emailInput || !passInput || !msgEl || !submitBtn) {
    console.error('Register JS: Missing required elements');
    return;
  }

  form.addEventListener('submit', handleRegister);

  async function handleRegister(event) {
    event.preventDefault();
    clearMessage();

    const username = usernameInput.value.trim();
    const email    = emailInput.value.trim();
    const password = passInput.value;

    if (!username || !email || !password) {
      showError('All fields are required.');
      return;
    }

    setLoading(true);

    try {
      const res  = await fetch(REGISTER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || `Status ${res.status}`);
      }

      showSuccess(data.message);
      form.reset();
    } catch (err) {
      console.error('Registration error:', err);
      showError(err.message || 'Could not register user.');
    } finally {
      setLoading(false);
    }
  }

  function setLoading(isLoading) {
    submitBtn.disabled    = isLoading;
    submitBtn.textContent = isLoading ? 'Registering…' : 'Register';
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

  // Fetch and display registered users
  if (showBtn && usersList) {
    showBtn.addEventListener('click', async () => {
      usersList.innerHTML = '';
      try {
        const res   = await fetch(USERS_URL);
        const users = await res.json();

        if (!Array.isArray(users) || users.length === 0) {
          usersList.innerHTML = '<li>No registered users found.</li>';
          return;
        }

        users.forEach(user => {
          const li = document.createElement('li');
          li.textContent = `${user.username} (${user.email})`;
          usersList.appendChild(li);
        });
      } catch (err) {
        console.error('Error fetching users:', err);
        usersList.innerHTML = '<li class="error">Could not fetch users.</li>';
      }
    });
  }
});
