(function() {
  function initScrollObservers() {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        entry.target.classList.toggle('appear', entry.isIntersecting);
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('.fade-section').forEach(el => observer.observe(el));
  }

  function manageNavbarTransparency() {
    const nav = document.querySelector('nav');
    const sentinel = document.getElementById('top-sentinel');
    if (!nav || !sentinel) return;
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        nav.classList.toggle('bg-opacity-90', !entry.isIntersecting);
        window.dispatchEvent(new CustomEvent('sentinel-change', {
          detail: { atTop: entry.isIntersecting }
        }));
      });
    });
    observer.observe(sentinel);
  }

  function getPreferredTheme() {
    return localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  document.addEventListener('DOMContentLoaded', function() {
    initScrollObservers();
    manageNavbarTransparency();
    const current = getPreferredTheme();
    applyTheme(current);
    const btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.setAttribute('aria-pressed', current === 'dark');
      btn.addEventListener('click', () => {
        const next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        applyTheme(next);
        btn.setAttribute('aria-pressed', next === 'dark');
      });
    }
  });

  window.ui = { initScrollObservers, manageNavbarTransparency, getPreferredTheme, applyTheme };
})();
