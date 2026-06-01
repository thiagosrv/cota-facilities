/* ============================================================
   COUNTERS.JS — Animated Number Counters
   Cota Facilities
   ============================================================ */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', initCounters);

  function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    if (!counters.length) return;

    counters.forEach(el => {
      const target  = parseInt(el.dataset.target, 10);
      const suffix  = el.dataset.suffix || '';
      const isLarge = target >= 1000;

      /* Initial display */
      el.textContent = '0' + suffix;

      /* Create an IntersectionObserver as fallback if GSAP not ready */
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            observer.unobserve(el);
            animateCounter(el, target, suffix, isLarge);
          }
        });
      }, { threshold: 0.3 });

      observer.observe(el);
    });
  }

  function animateCounter(el, target, suffix, isLarge) {
    if (typeof gsap !== 'undefined') {
      animateWithGSAP(el, target, suffix, isLarge);
    } else {
      animateWithRAF(el, target, suffix);
    }
  }

  /* ── GSAP version ────────────────────────────────────────── */
  function animateWithGSAP(el, target, suffix, isLarge) {
    const obj = { val: 0 };
    const duration = target > 5000 ? 2.5 : 2;

    gsap.to(obj, {
      val: target,
      duration,
      ease: 'power1.out',
      onUpdate: () => {
        const v = Math.round(obj.val);
        el.textContent = formatNumber(v, isLarge) + suffix;
      },
      onComplete: () => {
        el.textContent = formatNumber(target, isLarge) + suffix;
      }
    });
  }

  /* ── RAF fallback ────────────────────────────────────────── */
  function animateWithRAF(el, target, suffix) {
    const duration = 2000;
    const start = performance.now();
    const isLarge = target >= 1000;

    function step(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOut(progress);
      const current = Math.round(eased * target);

      el.textContent = formatNumber(current, isLarge) + suffix;

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = formatNumber(target, isLarge) + suffix;
      }
    }

    requestAnimationFrame(step);
  }

  /* ── Helpers ─────────────────────────────────────────────── */
  function formatNumber(n, isLarge) {
    if (isLarge && n >= 1000) {
      /* Format as "12.000" Brazilian style */
      return n.toLocaleString('pt-BR');
    }
    return n.toString();
  }

  function easeOut(t) {
    return 1 - Math.pow(1 - t, 3);
  }

})();
