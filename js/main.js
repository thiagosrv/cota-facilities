/* ============================================================
   MAIN.JS v3.0 — Animations, Smooth Scroll, Micro-interactions
   Cota Facilities

   Stack:
   · Lenis          — scroll suave (substitui scroll-behavior: smooth)
   · GSAP 3         — hero, navbar, button springs, magnetic
   · ScrollTrigger  — scroll-driven: word reveals, batch cards, parallax
   · IntersectionObserver — fallback quando GSAP/ST não carregam

   Performance:
   · ScrollTrigger usado em batch (≤ 6 instâncias totais)
   · Lenis roda no RAF — zero main thread blocking
   · Magnetic buttons: somente em pointer: hover (desktop)
   · will-change removido após animações únicas
   ============================================================ */

(function () {
  'use strict';

  /* ── Bootstrap ──────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', () => {
    // Estas funções são independentes de GSAP:
    initMobileMenu();
    initFAQ();
    initServiceCards();

    // Smooth scroll: usa Lenis se disponível, senão nativo
    initSmoothScroll();
  });

  // Com defer, todos os <script defer> executam antes de DOMContentLoaded.
  // Portanto gsap, ScrollTrigger e Lenis estão disponíveis imediatamente.
  // O waitForGSAP continua como segurança para edge-cases de rede lenta.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', waitForGSAP);
  } else {
    waitForGSAP();
  }

  function waitForGSAP() {
    if (typeof gsap !== 'undefined') {
      initWithGSAP();
    } else {
      let attempts = 0;
      const iv = setInterval(() => {
        attempts++;
        if (typeof gsap !== 'undefined') {
          clearInterval(iv);
          initWithGSAP();
        } else if (attempts >= 20) {
          clearInterval(iv);
          // Fallback: IO para reveals básicos
          initScrollRevealsFallback();
          initStepRingsFallback();
        }
      }, 50);
    }
  }

  function initWithGSAP() {
    if (typeof ScrollTrigger !== 'undefined') {
      gsap.registerPlugin(ScrollTrigger);
    }

    initLenis();             // smooth scroll via Lenis + integração com ST
    initScrollProgress();    // barra de progresso no topo
    initNavbar();            // hide/show + entrance
    initHeroAnimation();     // timeline de entrada do hero
    initSubtitleRotation();  // rotação das frases do hero
    initButtonSprings();     // click feedback nos CTAs
    initMagneticButtons();   // magnetic hover (desktop only)
    initScrollAnimations();  // ST: word reveal, batch cards, parallax, FAQ
  }

  /* ────────────────────────────────────────────────────────
     LENIS — Scroll Suave
  ──────────────────────────────────────────────────────── */
  function initLenis() {
    if (typeof Lenis === 'undefined') return;

    const lenis = new Lenis({
      duration: 1.25,
      easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // expo ease out
      smoothWheel: true,
      smoothTouch: false,   // iOS tem inércia nativa — não sobrescrever
      touchMultiplier: 2,
      infinite: false,
    });

    // Integrar Lenis com ScrollTrigger
    if (typeof ScrollTrigger !== 'undefined') {
      lenis.on('scroll', ScrollTrigger.update);
      ScrollTrigger.normalizeScroll(true);
    }

    // Conectar ao GSAP ticker para sincronização perfeita
    gsap.ticker.add((time) => {
      lenis.raf(time * 1000);
    });
    gsap.ticker.lagSmoothing(0);

    // Expor globalmente para initSmoothScroll usar
    window._lenis = lenis;
  }

  /* ────────────────────────────────────────────────────────
     SCROLL PROGRESS BAR
  ──────────────────────────────────────────────────────── */
  function initScrollProgress() {
    const bar = document.getElementById('scrollProgress');
    if (!bar || typeof ScrollTrigger === 'undefined') return;

    gsap.to(bar, {
      scaleX: 1,
      ease: 'none',
      scrollTrigger: {
        trigger: document.documentElement,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 0.4,
      }
    });
  }

  /* ────────────────────────────────────────────────────────
     SCROLL ANIMATIONS (ScrollTrigger)
  ──────────────────────────────────────────────────────── */
  function initScrollAnimations() {
    if (typeof ScrollTrigger === 'undefined') {
      // Fallback IO se ST não carregou
      initScrollRevealsFallback();
      initStepRingsFallback();
      return;
    }

    // ── 1. Word reveal em H2 das section-headers ─────────
    // Quebra cada h2 em .word-wrap > .word e anima do clip
    const headings = document.querySelectorAll(
      '.section-header h2, .form-header h2, .providers-content h2'
    );
    headings.forEach(h2 => {
      if (h2.dataset.splitDone) return;
      splitIntoWords(h2);

      const words = h2.querySelectorAll('.word');
      gsap.set(words, { yPercent: 110 });

      ScrollTrigger.create({
        trigger: h2,
        start: 'top 88%',
        once: true,
        onEnter: () => {
          gsap.to(words, {
            yPercent: 0,
            duration: 0.72,
            stagger: 0.055,
            ease: 'power3.out',
          });
        }
      });
    });

    // ── 2. Section tags: spring pop ──────────────────────
    gsap.utils.toArray('.section-tag').forEach(tag => {
      gsap.set(tag, { scale: 0.6, opacity: 0 });
      ScrollTrigger.create({
        trigger: tag,
        start: 'top 92%',
        once: true,
        onEnter: () => {
          gsap.to(tag, {
            scale: 1,
            opacity: 1,
            duration: 0.55,
            ease: 'back.out(2.2)',
          });
        }
      });
    });

    // ── 3. Batch: service cards ───────────────────────────
    const serviceCards = gsap.utils.toArray('.service-card');
    if (serviceCards.length) {
      gsap.set(serviceCards, { y: 40, opacity: 0, scale: 0.97 });
      ScrollTrigger.batch(serviceCards, {
        onEnter: els => {
          gsap.to(els, {
            y: 0, opacity: 1, scale: 1,
            stagger: 0.09,
            duration: 0.62,
            ease: 'power3.out',
          });
        },
        start: 'top 88%',
        once: true,
      });
    }

    // ── 4. Batch: step cards ──────────────────────────────
    const stepCards = gsap.utils.toArray('.step-card');
    if (stepCards.length) {
      gsap.set(stepCards, { y: 55, opacity: 0 });
      ScrollTrigger.batch(stepCards, {
        onEnter: els => {
          gsap.to(els, {
            y: 0, opacity: 1,
            stagger: 0.14,
            duration: 0.72,
            ease: 'power3.out',
          });
        },
        start: 'top 85%',
        once: true,
      });
    }

    // ── 5. Batch: trust cards ─────────────────────────────
    const trustCards = gsap.utils.toArray('.trust-card');
    if (trustCards.length) {
      gsap.set(trustCards, { y: 36, opacity: 0, scale: 0.96 });
      ScrollTrigger.batch(trustCards, {
        onEnter: els => {
          gsap.to(els, {
            y: 0, opacity: 1, scale: 1,
            stagger: 0.10,
            duration: 0.60,
            ease: 'power3.out',
          });
        },
        start: 'top 88%',
        once: true,
      });
    }

    // ── 6. FAQ items: slide-in da esquerda ─────────────────
    const faqItems = gsap.utils.toArray('.faq-item');
    if (faqItems.length) {
      gsap.set(faqItems, { x: -28, opacity: 0 });
      ScrollTrigger.batch(faqItems, {
        onEnter: els => {
          gsap.to(els, {
            x: 0, opacity: 1,
            stagger: 0.07,
            duration: 0.52,
            ease: 'power2.out',
          });
        },
        start: 'top 88%',
        once: true,
      });
    }

    // ── 7. Stat items: rise + scale ───────────────────────
    const statItems = gsap.utils.toArray('.stat-item');
    if (statItems.length) {
      gsap.set(statItems, { y: 30, opacity: 0 });
      ScrollTrigger.batch(statItems, {
        onEnter: els => {
          gsap.to(els, {
            y: 0, opacity: 1,
            stagger: 0.15,
            duration: 0.65,
            ease: 'power3.out',
          });
        },
        start: 'top 75%',
        once: true,
      });
    }

    // ── 8. Hero parallax (scrub) ──────────────────────────
    // Conteúdo do hero sobe mais devagar que o scroll → efeito de profundidade
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
      gsap.to(heroContent, {
        y: -70,
        ease: 'none',
        scrollTrigger: {
          trigger: '.hero',
          start: 'top top',
          end: 'bottom top',
          scrub: 2,
        }
      });
    }

    // ── Providers inner: stagger ──────────────────────────
    const provInner = document.querySelector('.providers-inner');
    if (provInner) {
      const children = Array.from(provInner.children);
      gsap.set(children, { y: 40, opacity: 0 });
      ScrollTrigger.create({
        trigger: provInner,
        start: 'top 80%',
        once: true,
        onEnter: () => {
          gsap.to(children, {
            y: 0, opacity: 1,
            stagger: 0.15,
            duration: 0.65,
            ease: 'power3.out',
          });
        }
      });
    }

    // ── Review cards ──────────────────────────────────────
    const reviewCards = gsap.utils.toArray('.review-card');
    if (reviewCards.length) {
      gsap.set(reviewCards, { y: 32, opacity: 0 });
      ScrollTrigger.batch(reviewCards, {
        onEnter: els => {
          gsap.to(els, {
            y: 0, opacity: 1,
            stagger: 0.10,
            duration: 0.58,
            ease: 'power2.out',
          });
        },
        start: 'top 88%',
        once: true,
      });
    }
  }

  /* ────────────────────────────────────────────────────────
     WORD SPLIT — quebra h2 em .word-wrap > .word
  ──────────────────────────────────────────────────────── */
  function splitIntoWords(el) {
    el.dataset.splitDone = '1';
    const rawHTML = el.innerHTML;

    // Tokeniza por espaço, preserva tags HTML simples
    const parts = rawHTML.split(/(\s+)/);
    el.innerHTML = parts.map(part => {
      if (/^\s+$/.test(part)) return part; // espaços entre palavras
      return `<span class="word-wrap"><span class="word">${part}</span></span>`;
    }).join('');
  }

  /* ────────────────────────────────────────────────────────
     NAVBAR
  ──────────────────────────────────────────────────────── */
  function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    gsap.from(navbar, { y: -70, opacity: 0, duration: 0.7, ease: 'power3.out', delay: 0.1 });

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

  /* ────────────────────────────────────────────────────────
     HERO ANIMATION
  ──────────────────────────────────────────────────────── */
  function initHeroAnimation() {
    const words     = document.querySelectorAll('.hero-word');
    const heroSub   = document.querySelector('.hero-sub');
    const heroCtas  = document.querySelector('.hero-ctas');
    const heroTrust = document.querySelector('.hero-trust-row');
    const heroBadge = document.querySelector('.hero-badge');
    const heroMockup = document.getElementById('heroMockup');

    const toAnimate = [heroSub, heroCtas, heroTrust, heroBadge].filter(Boolean);
    gsap.set(words,     { yPercent: 110, opacity: 0 });
    gsap.set(toAnimate, { y: 24, opacity: 0 });
    if (heroMockup) gsap.set(heroMockup, { x: 50, opacity: 0, scale: 0.95 });

    gsap.timeline({ delay: 0.25 })
      .to(heroBadge,   { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' })
      .to(words,       { yPercent: 0, opacity: 1, stagger: 0.055, duration: 0.65, ease: 'power3.out' }, '-=0.15')
      .to(heroSub,     { y: 0, opacity: 1, duration: 0.50, ease: 'power2.out' }, '-=0.30')
      .to(heroCtas,    { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, '-=0.30')
      .to(heroTrust,   { y: 0, opacity: 1, duration: 0.40, ease: 'power2.out' }, '-=0.25')
      .to(heroMockup,  { x: 0, opacity: 1, scale: 1, duration: 0.7, ease: 'power3.out' }, '-=0.50');

    if (heroMockup) {
      gsap.to(heroMockup, { y: -14, duration: 2.6, ease: 'sine.inOut', yoyo: true, repeat: -1, delay: 1.2 });
    }
  }

  /* ────────────────────────────────────────────────────────
     SUBTITLE ROTATION
  ──────────────────────────────────────────────────────── */
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

  /* ────────────────────────────────────────────────────────
     MAGNETIC BUTTONS — CTAs seguem o cursor (desktop only)
  ──────────────────────────────────────────────────────── */
  function initMagneticButtons() {
    // Pular em dispositivos touch (hover: none = touchscreen)
    if (window.matchMedia('(hover: none)').matches) return;

    const sel = '.btn-primary, .btn-nav, .mm-cta-btn';
    document.querySelectorAll(sel).forEach(btn => {
      btn.addEventListener('mousemove', e => {
        const r = btn.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width  / 2) * 0.28;
        const y = (e.clientY - r.top  - r.height / 2) * 0.28;
        gsap.to(btn, { x, y, duration: 0.38, ease: 'power2.out', overwrite: 'auto' });
      });

      btn.addEventListener('mouseleave', () => {
        gsap.to(btn, { x: 0, y: 0, duration: 0.55, ease: 'elastic.out(1, 0.45)', overwrite: 'auto' });
      });
    });
  }

  /* ────────────────────────────────────────────────────────
     BUTTON SPRINGS — click feedback
  ──────────────────────────────────────────────────────── */
  function initButtonSprings() {
    const sel = '.btn-primary, .btn-nav, .btn-next, .btn-submit, .btn-provider-submit';
    document.querySelectorAll(sel).forEach(btn => {
      btn.addEventListener('pointerdown', () => {
        if (btn.disabled) return;
        gsap.to(btn, { scale: 0.95, duration: 0.09, ease: 'power1.out', overwrite: 'auto' });
      });
      btn.addEventListener('pointerup', () => {
        gsap.to(btn, { scale: 1, duration: 0.4, ease: 'elastic.out(1, 0.5)', overwrite: 'auto' });
      });
      btn.addEventListener('pointerleave', () => {
        gsap.to(btn, { scale: 1, duration: 0.25, ease: 'power2.out', overwrite: 'auto' });
      });
    });
  }

  /* ────────────────────────────────────────────────────────
     SERVICE CARDS — click → scroll + seleciona tipo
  ──────────────────────────────────────────────────────── */
  function initServiceCards() {
    document.querySelectorAll('.service-card').forEach(card => {
      card.addEventListener('click', () => {
        const service = card.dataset.service;
        const targetCard = document.querySelector(`.service-select-card[data-value="${service}"]`);
        if (targetCard) {
          const cotacao = document.getElementById('cotacao');
          if (cotacao) {
            if (window._lenis) {
              const navH = (document.getElementById('navbar')?.offsetHeight || 70) + 8;
              window._lenis.scrollTo(cotacao, { offset: -navH, duration: 1.2 });
            } else {
              cotacao.scrollIntoView({ behavior: 'smooth' });
            }
            setTimeout(() => targetCard.click(), 800);
          }
        }
      });
    });
  }

  /* ────────────────────────────────────────────────────────
     MOBILE MENU (premium overlay — irmão do <nav>)
  ──────────────────────────────────────────────────────── */
  function initMobileMenu() {
    const toggle   = document.getElementById('navToggle');
    const closeBtn = document.getElementById('menuClose');
    const menu     = document.getElementById('mobileMenu');
    if (!toggle || !menu) return;

    const mmLinks = menu.querySelectorAll('.mm-link');
    const mmFoot  = menu.querySelector('.mm-foot');
    let isOpen    = false;

    function openMenu() {
      if (isOpen) return;
      isOpen = true;

      toggle.setAttribute('aria-expanded', 'true');
      menu.setAttribute('aria-hidden', 'false');
      toggle.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      menu.classList.add('is-open');

      if (typeof gsap !== 'undefined') {
        gsap.set(mmLinks, { opacity: 0, x: 32 });
        gsap.set(mmFoot,  { opacity: 0, y: 20 });
        gsap.to(mmLinks, {
          opacity: 1, x: 0,
          stagger: 0.07, duration: 0.42, ease: 'power3.out', delay: 0.15
        });
        gsap.to(mmFoot, {
          opacity: 1, y: 0,
          duration: 0.40, ease: 'power2.out',
          delay: 0.15 + mmLinks.length * 0.07 + 0.08
        });
      }

      setTimeout(() => closeBtn?.focus(), 80);
    }

    function closeMenu() {
      if (!isOpen) return;
      isOpen = false;

      toggle.setAttribute('aria-expanded', 'false');
      menu.setAttribute('aria-hidden', 'true');
      toggle.classList.remove('is-open');
      document.body.style.overflow = '';

      if (typeof gsap !== 'undefined') {
        gsap.to([mmLinks, mmFoot], {
          opacity: 0, duration: 0.18, ease: 'power1.in',
          onComplete: () => menu.classList.remove('is-open')
        });
      } else {
        menu.classList.remove('is-open');
      }

      toggle.focus();
    }

    toggle.addEventListener('click', () => isOpen ? closeMenu() : openMenu());
    closeBtn?.addEventListener('click', closeMenu);
    mmLinks.forEach(l => l.addEventListener('click', closeMenu));
    menu.querySelector('.mm-cta-btn')?.addEventListener('click', closeMenu);
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && isOpen) closeMenu(); });
    menu.addEventListener('click', e => { if (e.target === menu) closeMenu(); });
  }

  /* ────────────────────────────────────────────────────────
     FAQ ACCORDION
  ──────────────────────────────────────────────────────── */
  function initFAQ() {
    document.querySelectorAll('.faq-item').forEach(item => {
      const btn    = item.querySelector('.faq-question');
      const answer = item.querySelector('.faq-answer');
      if (!btn || !answer) return;

      btn.addEventListener('click', () => {
        const wasOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(other => {
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

  /* ────────────────────────────────────────────────────────
     SMOOTH SCROLL — usa Lenis se disponível
  ──────────────────────────────────────────────────────── */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', e => {
        const href   = anchor.getAttribute('href');
        if (!href || href === '#') return;
        const target = document.querySelector(href);
        if (!target) return;
        e.preventDefault();

        const navH = (document.getElementById('navbar')?.offsetHeight || 72) + 8;

        if (window._lenis) {
          window._lenis.scrollTo(target, { offset: -navH, duration: 1.4 });
        } else {
          window.scrollTo({
            top: target.getBoundingClientRect().top + window.scrollY - navH,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  /* ────────────────────────────────────────────────────────
     FALLBACKS — IntersectionObserver quando GSAP não carrega
  ──────────────────────────────────────────────────────── */
  function initScrollRevealsFallback() {
    const reveals = document.querySelectorAll('.reveal');
    if (!reveals.length) return;

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
    }, { threshold: 0.10, rootMargin: '0px 0px -48px 0px' });

    reveals.forEach(el => io.observe(el));

    const provInner = document.querySelector('.providers-inner');
    if (provInner) {
      Array.from(provInner.children).forEach((child, i) => {
        child.classList.add('reveal');
        child.style.setProperty('--reveal-delay', i * 120 + 'ms');
        io.observe(child);
      });
    }
  }

  function initStepRingsFallback() {
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

})();
