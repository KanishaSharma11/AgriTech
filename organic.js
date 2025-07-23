document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('main section');
  const nav = document.getElementById('steps-nav');

  sections.forEach((sec, i) => {
    const btn = document.createElement('button');
    btn.textContent = `Step ${i+1}`;
    btn.addEventListener('click', () => {
      sec.scrollIntoView({ behavior: 'smooth' });
    });
    nav.appendChild(btn);
  });

  window.addEventListener('scroll', () => {
    let idx = sections.length - 1;
    sections.forEach((sec, i) => {
      const rect = sec.getBoundingClientRect();
      if (rect.top < window.innerHeight / 2) idx = i;
    });
    nav.querySelectorAll('button').forEach((b,i) => {
      b.classList.toggle('active', i === idx);
    });
  });
});
