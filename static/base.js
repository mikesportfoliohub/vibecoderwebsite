document.addEventListener('DOMContentLoaded', () => {
  const pathSegments = window.location.pathname.split('/').filter(Boolean);
  let breadcrumbHTML = `<li><a href="${HOME_URL}">Home</a></li>`;
  let currentPath = '';

  pathSegments.forEach((segment, index) => {
    currentPath += '/' + segment;
    const displayName = segment.charAt(0).toUpperCase() + segment.slice(1);
    // Render last element as plain text; others as links.
    if (index === pathSegments.length - 1) {
      breadcrumbHTML += `<li>${displayName}</li>`;
    } else {
      breadcrumbHTML += `<li><a href="${currentPath}">${displayName}</a></li>`;
    }
  });

  document.getElementById('breadcrumb').innerHTML = breadcrumbHTML;
});
