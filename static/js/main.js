const body = document.body;
const isTouch = matchMedia('(hover: none), (max-width: 900px)').matches;

// Preloader
const finishLoad = () => setTimeout(() => body.classList.add('loaded'), 350);
if (document.readyState === 'complete') finishLoad(); else window.addEventListener('load', finishLoad);
setTimeout(() => body.classList.add('loaded'), 2500); // safety net

// Menu
document.getElementById('menuBtn').addEventListener('click', () => body.classList.toggle('menu-open'));
document.querySelectorAll('.menu-item').forEach(a => a.addEventListener('click', () => body.classList.remove('menu-open')));
document.addEventListener('keydown', e => { if (e.key === 'Escape') body.classList.remove('menu-open'); });

// Header + progress + parallax on scroll
const topbar = document.querySelector('.topbar');
const progress = document.getElementById('progress');
const heroImg = document.querySelector('.hero-bg-img');
const parallax = document.querySelectorAll('.parallax');
let lastY = 0, ticking = false;
function onScroll() {
  const y = window.scrollY;
  topbar.classList.toggle('scrolled', y > 40);
  topbar.classList.toggle('hide', y > 300 && y > lastY && !body.classList.contains('menu-open'));
  lastY = y;
  const max = document.documentElement.scrollHeight - innerHeight;
  progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
  if (heroImg && y < innerHeight * 1.2) heroImg.style.transform = `translateY(${y * 0.3}px) scale(${1.05 + y * 0.0002})`;
  parallax.forEach(el => {
    const r = el.getBoundingClientRect();
    const off = Math.max(-60, Math.min(60, (r.top + r.height / 2 - innerHeight / 2) * -(+el.dataset.speed || 0.05)));
    el.style.transform = `translateY(${off}px) scale(1.18)`;
  });
  ticking = false;
}
window.addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
onScroll();

// Back to top
document.getElementById('toTop')?.addEventListener('click', () => scrollTo({ top: 0, behavior: 'smooth' }));

// Reveal on scroll + counters
const io = new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (!en.isIntersecting) return;
    en.target.classList.add('in');
    const num = en.target.querySelector('[data-count]');
    if (num) countUp(num);
    io.unobserve(en.target);
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

function countUp(el) {
  const target = +el.dataset.count, start = performance.now(), dur = 1800;
  const step = t => {
    const p = Math.min((t - start) / dur, 1);
    el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + (p === 1 ? '+' : '');
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// Custom cursor
const cursor = document.getElementById('cursor');
if (cursor && !isTouch) {
  let cx = innerWidth / 2, cy = innerHeight / 2, tx = cx, ty = cy;
  addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; cursor.classList.add('on'); });
  document.addEventListener('mouseleave', () => cursor.classList.remove('on'));
  (function loop() {
    cx += (tx - cx) * 0.2; cy += (ty - cy) * 0.2;
    cursor.style.transform = `translate(${cx}px, ${cy}px)`;
    requestAnimationFrame(loop);
  })();
  const label = cursor.querySelector('span');
  document.querySelectorAll('a, button, summary, input, textarea, select').forEach(el => {
    el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
    el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
  });
  document.querySelectorAll('.news-card, .exp-card, .case-card, .row-card').forEach(el => {
    el.addEventListener('mouseenter', () => { cursor.classList.add('view'); label.textContent = 'View'; });
    el.addEventListener('mouseleave', () => cursor.classList.remove('view'));
  });
} else if (cursor) cursor.remove();

// Magnetic buttons
if (!isTouch) document.querySelectorAll('.magnetic').forEach(el => {
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect();
    el.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.25}px, ${(e.clientY - r.top - r.height / 2) * 0.35}px)`;
  });
  el.addEventListener('mouseleave', () => el.style.transform = '');
});

// Testimonial slider
const slider = document.getElementById('slider');
if (slider) {
  const slides = slider.querySelectorAll('.slide'), dots = slider.querySelectorAll('.slider-dots button');
  let i = 0, timer;
  const go = n => {
    slides[i].classList.remove('active'); dots[i].classList.remove('active');
    i = (n + slides.length) % slides.length;
    slides[i].classList.add('active'); dots[i].classList.add('active');
    clearInterval(timer); timer = setInterval(() => go(i + 1), 6000);
  };
  dots.forEach(d => d.addEventListener('click', () => go(+d.dataset.i)));
  slider.querySelectorAll('.nav-btn').forEach(b => b.addEventListener('click', () => go(i + +b.dataset.dir)));
  timer = setInterval(() => go(i + 1), 6000);
}

// FAQ: only one open at a time
document.querySelectorAll('.faq-item').forEach(d => d.addEventListener('toggle', () => {
  if (d.open) document.querySelectorAll('.faq-item').forEach(o => { if (o !== d) o.open = false; });
}));

// Case study filters
const filters = document.getElementById('filters');
if (filters) {
  filters.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    filters.querySelectorAll('button').forEach(x => x.classList.toggle('active', x === b));
    document.querySelectorAll('.filter-item').forEach(it => {
      it.classList.toggle('hidden', b.dataset.f !== 'all' && it.dataset.cat !== b.dataset.f);
      it.querySelector('.reveal')?.classList.add('in');
    });
  });
}
