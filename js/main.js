/* ============================================================
   MAIN.JS v2.0 — Animations, Micro-interactions
   Cota Facilities

   Performance: ScrollTrigger removido → IntersectionObserver nativo
   (zero bloqueio de main thread para scroll animations).
   GSAP usado apenas para: hero entrance, navbar hide/show,
   form step transitions e mobile menu.
   ============================================================ */

(function () {
  'use strict';

  /* ── Inicialização ──────────────────────────────────────── */
  // Scroll reveals e step rings não dependem de GSAP — iniciar imediatamente
  document.addEventListener('DOMContentLoaded', () => {
    initScrollReveals();   // IntersectionObserver — nativo, sem GSAP
    initStepRings();       // IntersectionObserver — nativo, sem GSAP
    initMobileMenu();      // usa GSAP se disponível, CSS fallback
    initSmoothScroll();
    initFAQ();
    initServiceCards();    // apenas click handler, sem hover GSAP
  });

  // Hero + interações visuais dependem de GSAP — aguardar carregamento
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', waitForGSAP);
  } else {
    waitForGSAP();
  }

  function waitForGSAP() {
    if (typeof gsap !== 'undefined') {
      initWithGSAP();
    } else {
      // Polling mínimo: max 20 tentativas (1 segundo total)
      let attempts = 0;
      const interval = setInterval(() => {
        attempts++;
        if (typeof gsap !== 'undefined') {
          clearInterval(interval);
          initWithGSAP();
        } else if (attempts >= 20) {
          clearInterval(interval); // desiste, animações CSS fazem o trabalho
        }
      }, 50);
    }
  }

  function initWithGSAP() {
    // NÃO registrar ScrollTrigger — removido completamente
    initNavbar();
    initHeroAnimation();
    initSubtitleRotation();
    initButtonSprings();
  }

  /* ── Scroll Reveals — IntersectionObserver nativo ────────
     Zero bloqueio de main thread. CSS transition em .reveal
     faz a animação; JS apenas adiciona .is-visible.
  ──────────────────────────────────────────────────────── */
  function initScrollReveals() {
    const reveals = document.querySelectorAll('.reveal');
    if (!reveals.length) return;

    // Stagger via CSS custom property por linha (group de 4)
    reveals.forEach((el, i) => {
      el.style.setProperty('--reveal-delay', (i % 4) * 60 + 'ms');
    });

    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.10,
      rootMargin: '0px 0px -48px 0px'
    });

    reveals.forEach(el => io.observe(el));

    // Providers section: adiciona reveal class programaticamente
    const providersInner = document.querySelector('.providers-inner');
    if (providersInner) {
      Array.from(providersInner.children).forEach((child, i) => {
        child.classList.add('reveal');
        child.style.setProperty('--reveal-delay', i * 120 + 'ms');
        io.observe(child);
      });
    }
  }

  /* ── Step Rings — IntersectionObserver nativo ───────────── */
  function initStepRings() {
    const stepCards = document.querySelectorAll('.step-card');
    if (!stepCards.length) return;

    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.20 });

    stepCards.forEach(card => io.observe(card));
  }

  /* ── Navbar ─────────────────────────────────────────────── */
  function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    // Entrance animation
    gsap.from(navbar, { y: -70, opacity: 0, duration: 0.7, ease: 'power3.out', delay: 0.1 });

    // Hide on scroll down / show on scroll up
    let lastScroll = 0;
    let ticking = false;

    window.addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const scrollY = window.scrollY;
        navbar.classList.toggle('scrolled', scrollY > 60);

        if (scrollY > lastScroll && scrollY > 200) {
          gsap.to(navbar, { y: -100, duration: 0.3, ease: 'power2.in', overwrite: 'auto' });
        } else {
          gsap.to(navbar, { y: 0, duration: 0.3, ease: 'power2.out', overwrite: 'auto' });
        }
        lastScroll = scrollY;
        ticking = false;
      });
    }, { passive: true });
  }

  /* ── Hero Animation ─────────────────────────────────────── */
  function initHeroAnimation() {
    const words    = document.querySelectorAll('.hero-word');
    const heroSub  = document.querySelector('.hero-sub');
    const heroCtas = document.querySelector('.hero-ctas');
    const heroTrust = document.querySelector('.hero-trust-row');
    const heroBadge = document.querySelector('.hero-badge');
    const heroMockup = document.getElementById('heroMockup');

    // Batch inicial — uma única operação de estilo
    const toAnimate = [heroSub, heroCtas, heroTrust, heroBadge].filter(Boolean);
    gsap.set(words,     { yPercent: 110, opacity: 0 });
    gsap.set(toAnimate, { y: 24, opacity: 0 });
    if (heroMockup) gsap.set(heroMockup, { x: 50, opacity: 0, scale: 0.95 });

    gsap.timeline({ delay: 0.25 })
      .to(heroBadge,  { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' })
      .to(words,      { yPercent: 0, opacity: 1, stagger: 0.055, duration: 0.6, ease: 'power3.out' }, '-=0.15')
      .to(heroSub,    { y: 0, opacity: 1, duration: 0.5, ease: 'power2.out' }, '-=0.25')
      .to(heroCtas,   { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, '-=0.3')
      .to(heroTrust,  { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, '-=0.25')
      .to(heroMockup, { x: 0, opacity: 1, scale: 1, duration: 0.7, ease: 'power3.out' }, '-=0.5');

    // Float loop apenas no mockup
    if (heroMockup) {
      gsap.to(heroMockup, { y: -14, duration: 2.6, ease: 'sine.inOut', yoyo: true, repeat: -1, delay: 1.2 });
    }
  }

  /* ── Subtitle Rotation ───────────────────────────────────── */
  function initSubtitleRotation() {
    const el = document.getElementById('hero-subtitle-rotating');
    if (!el) return;

    const phrases = [
      'Sem Ligações. Sem Burocracia.',
      'Economize tempo. Sem burocracia.',
      'Cotações rápidas. 100% grátis.',
      'Compare propostas. Economize hoje.',
      'Empresas avaliadas. Propostas em 24h.',
      'Simples, rápido e 100% gratuito.',
      'As melhores empresas competem pelo seu contrato.',
      'Solicite online. Resposta em 24 horas.'
    ];

    let idx = 0;
    setInterval(() => {
      idx = (idx + 1) % phrases.length;
      gsap.to(el, {
        opacity: 0, y: -8, duration: 0.35,
        onComplete: () => {
          el.textContent = phrases[idx];
          gsap.fromTo(el, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.35 });
        }
      });
    }, 4000);
  }

  /* ── Service Cards ───────────────────────────────────────── */
  function initServiceCards() {
    document.querySelectorAll('.service-card').forEach(card => {
      card.addEventListener('click', () => {
        const service = card.dataset.service;
        const targetCard = document.querySelector(`.service-select-card[data-value="${service}"]`);
        if (targetCard) {
          document.getElementById('cotacao')?.scrollIntoView({ behavior: 'smooth' });
          setTimeout(() => targetCard.click(), 750);
        }
      });
    });
  }

  /* ── Button Springs (click feedback) ────────────────────── */
  function initButtonSprings() {
    const sel = '.btn-primary, .btn-nav, .btn-next, .btn-submit, .btn-provider-submit';
    document.querySelectorAll(sel).forEach(btn => {
      btn.addEventListener('pointerdown', () => {
        if (btn.disabled) return;
        gsap.to(btn, { scale: 0.95, duration: 0.09, ease: 'power1.out', overwrite: 'auto' });
      });
      btn.addEventListener('pointerup', () => {
        gsap.to(btn, { scale: 1, duration: 0.4, ease: 'elastic.out(1,0.5)', overwrite: 'auto' });
      });
      btn.addEventListener('pointerleave', () => {
        gsap.to(btn, { scale: 1, duration: 0.25, ease: 'power2.out', overwrite: 'auto' });
      });
    });
  }

  /* ── Mobile Menu ─────────────────────────────────────────── */
  function initMobileMenu() {
    const toggle = document.getElementById('navToggle');
    const links  = document.getElementById('navLinks');
    if (!toggle || !links) return;

    let isOpen = false;

    function openMenu() {
      isOpen = true;
      links.classList.add('open');
      toggle.classList.add('menu-open');
      document.body.style.overflow = 'hidden';

      if (typeof gsap !== 'undefined') {
        const navLinks = links.querySelectorAll('.nav-link');
        gsap.fromTo(navLinks,
          { y: 20, opacity: 0 },
          { y: 0, opacity: 1, stagger: 0.07, duration: 0.35, ease: 'power2.out' }
        );
        const spans = toggle.querySelectorAll('span');
        gsap.to(spans[0], { rotation: 45,  y: 7,  duration: 0.28 });
        gsap.to(spans[1], { opacity: 0,           duration: 0.18 });
        gsap.to(spans[2], { rotation: -45, y: -7, duration: 0.28 });
      }
    }

    function closeMenu() {
      isOpen = false;
      links.classList.remove('open');
      toggle.classList.remove('menu-open');
      document.body.style.overflow = '';

      if (typeof gsap !== 'undefined') {
        const spans = toggle.querySelectorAll('span');
        gsap.to(spans[0], { rotation: 0, y: 0, duration: 0.28 });
        gsap.to(spans[1], { opacity: 1, duration: 0.18, delay: 0.08 });
        gsap.to(spans[2], { rotation: 0, y: 0, duration: 0.28 });
      }
    }

    toggle.addEventListener('click', () => isOpen ? closeMenu() : openMenu());
    links.querySelectorAll('.nav-link').forEach(l => l.addEventListener('click', closeMenu));
  }

  /* ── FAQ Accordion ───────────────────────────────────────── */
  function initFAQ() {
    const items = document.querySelectorAll('.faq-item');

    items.forEach(item => {
      const btn    = item.querySelector('.faq-question');
      const answer = item.querySelector('.faq-answer');
      if (!btn || !answer) return;

      btn.addEventListener('click', () => {
        const wasOpen = item.classList.contains('open');

        items.forEach(other => {
          other.classList.remove('open');
          other.querySelector('.faq-question')?.setAttribute('aria-expanded', 'false');
        });

        if (!wasOpen) {
          item.classList.add('open');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }

  /* ── Smooth Scroll ───────────────────────────────────────── */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', e => {
        const href   = anchor.getAttribute('href');
        const target = document.querySelector(href);
        if (!target) return;
        e.preventDefault();
        const navH = (document.getElementById('navbar')?.offsetHeight || 72) + 8;
        window.scrollTo({
          top: target.getBoundingClientRect().top + window.scrollY - navH,
          behavior: 'smooth'
        });
      });
    });
  }

})();
