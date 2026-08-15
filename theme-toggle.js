document.addEventListener('click', function (e) {
  var btn = e.target.closest('[data-theme-toggle]');
  if (!btn) return;
  var current = document.documentElement.getAttribute('data-theme');
  var systemDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  var isDark = current ? current === 'dark' : systemDark;
  var next = isDark ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  try { localStorage.setItem('ful-theme', next); } catch (err) {}
});
