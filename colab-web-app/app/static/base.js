// static/js/base.js

document.addEventListener('DOMContentLoaded', () => {
  const breadcrumbEl = document.getElementById('breadcrumb');
  if (!breadcrumbEl) return;

  const overrides = {
    auth: 'Login',
    register_page: 'Register',
    dashboard: 'Dashboard',
    admin: 'Admin'
  };

  const segments = window.location.pathname
    .split('/')
    .filter(Boolean);

  const fragment = document.createDocumentFragment();

  // Home link
  const liHome = document.createElement('li');
  liHome.innerHTML = `<a href="${HOME_URL}">Home</a>`;
  fragment.appendChild(liHome);

  let accumulatedPath = '';
  segments.forEach((seg, idx) => {
    accumulatedPath += `/${seg}`;

    // Derive display name
    let name = overrides[seg] 
      || decodeURIComponent(seg)
          .replace(/-/g, ' ')
          .replace(/\b\w/g, ch => ch.toUpperCase());

    const li = document.createElement('li');
    if (idx === segments.length - 1) {
      li.textContent = name;
    } else {
      const a = document.createElement('a');
      a.href = accumulatedPath;
      a.textContent = name;
      li.appendChild(a);
    }
    fragment.appendChild(li);
  });

  breadcrumbEl.replaceChildren(fragment);
});
