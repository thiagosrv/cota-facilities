/* ============================================================
   MAIN.JS — GSAP Animations, ScrollTrigger, Micro-interactions
   Cota Facilities
   ============================================================ */

(function () {
  'use strict';

  /* ── Wait for GSAP ─────────────────────────────────────── */
  function waitForGSAP(cb) {
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
      cb();
    } else {
      setTimeout(() => waitForGSAP(cb), 50);
    }
  }

  waitForGSAP(init);

  function init() {
    gsap.registerPlugin(ScrollTrigger);

    createParticles();
    initNavbar();
    initHeroAnimation();
    initScrollReveals();
    initStepRings();
    initServiceCards();
    initButtonSprings();
    initMobileMenu();
    initSmoothScroll();
    initFAQ();
  }

  /* ── Particles ──────────────────────────────────────────── */
  function createParticles() {
    const container = document.getElementById('particles');
    if (!container) return;

    const colors = ['#7B2FBE', '#1B3A8C', '#84CC16', '#5B21B6'];
    const count = window.innerWidth < 600 ? 8 : 16;

    for (let i = 0; i < count; i++) {
      const p = document.createElement('div');
      p.className = 'particle';

      const size = Math.random() * 200 + 80;
      const color = colors[Math.floor(Math.random() * colors.length)];
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      const dur = (Math.random() * 10 + 6).toFixed(1) + 's';
      const delay = (Math.random() * 6).toFixed(1) + 's';

      p.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${x}%;
        top: ${y}%;
        background: radial-gradient(circle, ${color}, transparent 70%);
        opacity: 0.07;
        --dur: ${dur};
        --delay: ${delay};
        animation-duration: ${dur};
        animation-delay: ${delay};
      `;

      container.appendChild(p);
    }
  }

  /* ── Navbar ─────────────────────────────────────────────── */
  function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    /* Entrance animation */
    gsap.from(navbar, {
      y: -80,
      opacity: 0,
      duration: 0.8,
      ease: 'power3.out',
      delay: 0.1
    });

    /* Scroll behavior */
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;

      if (scrollY > 60) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }

      /* Hide on scroll down, show on scroll up */
      if (scrollY > lastScroll && scrollY > 200) {
        gsap.to(navbar, { y: -100, duration: 0.3, ease: 'power2.in' });
      } else {
        gsap.to(navbar, { y: 0, duration: 0.3, ease: 'power2.out' });
      }

      lastScroll = scrollY;
    }, { passive: true });
  }

  /* ── Hero Animation ─────────────────────────────────────── */
  function initHeroAnimation() {
    const words = document.querySelectorAll('.hero-word');
    const heroSub = document.querySelector('.hero-sub');
    const heroCtas = document.querySelector('.hero-ctas');
    const heroTrust = document.querySelector('.hero-trust-row');
    const heroBadge = document.querySelector('.hero-badge');
    const heroMockup = document.getElementById('heroMockup');

    /* Set initial states */
    gsap.set(words, { yPercent: 110, opacity: 0 });
    gsap.set([heroSub, heroCtas, heroTrust, heroBadge], { y: 30, opacity: 0 });
    if (heroMockup) gsap.set(heroMockup, { x: 60, opacity: 0, scale: 0.9 });

    const tl = gsap.timeline({ delay: 0.3 });

    tl
      /* Badge first */
      .to(heroBadge, {
        y: 0,
        opacity: 1,
        duration: 0.5,
        ease: 'power2.out'
      })
      /* Words stagger reveal */
      .to(words, {
        yPercent: 0,
        opacity: 1,
        stagger: 0.06,
        duration: 0.65,
        ease: 'power3.out'
      }, '-=0.2')
      /* Subheadline */
      .to(heroSub, {
        y: 0,
        opacity: 1,
        duration: 0.55,
        ease: 'power2.out'
      }, '-=0.3')
      /* CTAs */
      .to(heroCtas, {
        y: 0,
        opacity: 1,
        duration: 0.5,
        ease: 'power2.out'
      }, '-=0.35')
      /* Trust badges */
      .to(heroTrust, {
        y: 0,
        opacity: 1,
        duration: 0.5,
        ease: 'power2.out'
      }, '-=0.3')
      /* Mockup card slides in */
      .to(heroMockup, {
        x: 0,
        opacity: 1,
        scale: 1,
        duration: 0.8,
        ease: 'power3.out'
      }, '-=0.6');

    /* Floating mockup loop */
    if (heroMockup) {
      gsap.to(heroMockup, {
        y: -16,
        duration: 2.8,
        ease: 'sine.inOut',
        yoyo: true,
        repeat: -1,
        delay: 1.5
      });
    }
  }

  /* ── Scroll Reveals ─────────────────────────────────────── */
  function initScrollReveals() {
    const reveals = document.querySelectorAll('.reveal');

    reveals.forEach((el, i) => {
      gsap.to(el, {
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          once: true
        },
        y: 0,
        opacity: 1,
        duration: 0.7,
        delay: (i % 4) * 0.05, /* slight cascade within same row */
        ease: 'power2.out'
      });
    });

    /* Service cards — stagger by column position */
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach((card, i) => {
      card.style.transitionDelay = (i % 3) * 0.08 + 's';
    });

    /* Step cards — stagger by index */
    const stepCards = document.querySelectorAll('.step-card');
    stepCards.forEach((card, i) => {
      card.style.transitionDelay = i * 0.12 + 's';
    });

    /* Providers section */
    const providersInner = document.querySelector('.providers-inner');
    if (providersInner) {
      gsap.from(providersInner.children, {
        scrollTrigger: {
          trigger: providersInner,
          start: 'top 85%',
          once: true
        },
        y: 40,
        opacity: 0,
        stagger: 0.2,
        duration: 0.7,
        ease: 'power2.out'
      });
    }
  }

  /* ── Step Rings Animation ────────────────────────────────── */
  function initStepRings() {
    const stepCards = document.querySelectorAll('.step-card');

    stepCards.forEach(card => {
      ScrollTrigger.create({
        trigger: card,
        start: 'top 80%',
        once: true,
        onEnter: () => {
          card.classList.add('animated');
        }
      });
    });
  }

  /* ── Service Cards Hover ─────────────────────────────────── */
  function initServiceCards() {
    const cards = document.querySelectorAll('.service-card');

    cards.forEach(card => {
      card.addEventListener('mouseenter', () => {
        gsap.to(card.querySelector('.service-icon-wrap'), {
          scale: 1.1,
          rotation: 5,
          duration: 0.2,
          ease: 'power1.out'
        });
      });

      card.addEventListener('mouseleave', () => {
        gsap.to(card.querySelector('.service-icon-wrap'), {
          scale: 1,
          rotation: 0,
          duration: 0.3,
          ease: 'power2.out'
        });
      });

      /* Click — scroll to form and pre-select */
      card.addEventListener('click', () => {
        const service = card.dataset.service;
        const targetCard = document.querySelector(`.service-select-card[data-value="${service}"]`);
        if (targetCard) {
          document.getElementById('cotacao').scrollIntoView({ behavior: 'smooth' });
          setTimeout(() => {
            targetCard.click();
          }, 800);
        }
      });
    });
  }

  /* ── Button Springs ─────────────────────────────────────── */
  function initButtonSprings() {
    const buttons = document.querySelectorAll(
      '.btn-primary, .btn-nav, .btn-next, .btn-submit, .btn-provider-submit, .mockup-btn'
    );

    buttons.forEach(btn => {
      btn.addEventListener('mousedown', () => {
        if (btn.disabled) return;
        gsap.to(btn, { scale: 0.95, duration: 0.1, ease: 'power1.out' });
      });

      btn.addEventListener('mouseup', () => {
        gsap.to(btn, { scale: 1, duration: 0.4, ease: 'elastic.out(1, 0.5)' });
      });

      btn.addEventListener('mouseleave', () => {
        gsap.to(btn, { scale: 1, duration: 0.3, ease: 'power2.out' });
      });
    });
  }

  /* ── Mobile Menu ─────────────────────────────────────────── */
  function initMobileMenu() {
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');
    if (!toggle || !links) return;

    let isOpen = false;

    toggle.addEventListener('click', () => {
      isOpen = !isOpen;

      if (isOpen) {
        links.classList.add('open');
        gsap.from(links.querySelectorAll('.nav-link'), {
          y: 20,
          opacity: 0,
          stagger: 0.08,
          duration: 0.4,
          ease: 'power2.out'
        });
        /* Animate hamburger to X */
        const spans = toggle.querySelectorAll('span');
        gsap.to(spans[0], { rotation: 45, y: 7, duration: 0.3 });
        gsap.to(spans[1], { opacity: 0, duration: 0.2 });
        gsap.to(spans[2], { rotation: -45, y: -7, duration: 0.3 });
      } else {
        links.classList.remove('open');
        const spans = toggle.querySelectorAll('span');
        gsap.to(spans[0], { rotation: 0, y: 0, duration: 0.3 });
        gsap.to(spans[1], { opacity: 1, duration: 0.2, delay: 0.1 });
        gsap.to(spans[2], { rotation: 0, y: 0, duration: 0.3 });
      }
    });

    /* Close on link click */
    links.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        isOpen = false;
        links.classList.remove('open');
        const spans = toggle.querySelectorAll('span');
        gsap.to(spans[0], { rotation: 0, y: 0, duration: 0.3 });
        gsap.to(spans[1], { opacity: 1, duration: 0.2, delay: 0.1 });
        gsap.to(spans[2], { rotation: 0, y: 0, duration: 0.3 });
      });
    });
  }

  /* ── FAQ Accordion ───────────────────────────────────────── */
  function initFAQ() {
    const items = document.querySelectorAll('.faq-item');

    items.forEach(item => {
      const btn = item.querySelector('.faq-question');
      const answer = item.querySelector('.faq-answer');
      if (!btn || !answer) return;

      btn.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');

        /* Close all others */
        items.forEach(other => {
          other.classList.remove('open');
          other.querySelector('.faq-question')?.setAttribute('aria-expanded', 'false');
        });

        /* Toggle current */
        if (!isOpen) {
          item.classList.add('open');
          btn.setAttribute('aria-expanded', 'true');

          if (typeof gsap !== 'undefined') {
            gsap.from(answer.querySelector('p'), {
              y: 10,
              opacity: 0,
              duration: 0.3,
              ease: 'power2.out'
            });
          }
        }
      });
    });
  }

  /* ── Smooth Scroll ───────────────────────────────────────── */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', e => {
        const target = document.querySelector(anchor.getAttribute('href'));
        if (!target) return;
        e.preventDefault();

        const navH = document.getElementById('navbar')?.offsetHeight || 80;
        const top = target.getBoundingClientRect().top + window.scrollY - navH;

        window.scrollTo({ top, behavior: 'smooth' });
      });
    });
  }

})();
