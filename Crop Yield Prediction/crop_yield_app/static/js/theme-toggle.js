const toggle = document.getElementById('themeToggle');
const current = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', current);
toggle.textContent = current === 'dark' ? '☀️' : '🌙';
toggle.onclick = () => {
  const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
  toggle.textContent = theme === 'dark' ? '☀️' : '🌙';
};
