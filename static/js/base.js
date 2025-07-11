document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('theme-toggle');
  if (!toggle) return;
  const saved = localStorage.getItem('theme') || 'light';
  applyTheme(saved);

  toggle.addEventListener('click', () => {
    const isDark = document.documentElement.classList.contains('theme-dark');
    applyTheme(isDark ? 'light' : 'dark');
  });
});

function applyTheme(theme) {
  if (theme === 'dark') {
    document.documentElement.classList.add('theme-dark');
  } else {
    document.documentElement.classList.remove('theme-dark');
  }
  localStorage.setItem('theme', theme);
}
