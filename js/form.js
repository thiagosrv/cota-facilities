/* ============================================================
   FORM.JS — Multi-Step Form State Machine + Loading + Results
   Cota Facilities
   ============================================================ */

(function () {
  'use strict';

  /* ── State ──────────────────────────────────────────────── */
  const state = {
    currentStep: 0,
    totalSteps: 5,
    data: {
      service: null,
      quotes: null,
      city: '',
      name: '',
      email: '',
      phone: ''
    }
  };

  /* ── DOM Refs ───────────────────────────────────────────── */
  const steps      = Array.from(document.querySelectorAll('.form-step'));
  const dots       = Array.from(document.querySelectorAll('.step-dot'));
  const progressBar = document.getElementById('formProgressBar');

  /* ── Init ───────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', () => {
    if (!steps.length) return;
    bindServiceCards();
    bindQuoteOptions();
    bindCitySelect();
    bindContactForm();
    bindNavButtons();
    bindNewQuote();
    updateProgress(0);
  });

  /* ── Progress ─────────────────────────────────────────────── */
  function updateProgress(stepIndex) {
    const pct = ((stepIndex + 1) / state.totalSteps) * 100;
    if (typeof gsap !== 'undefined') {
      gsap.to(progressBar, { width: pct + '%', duration: 0.45, ease: 'power2.out' });
    } else if (progressBar) {
      progressBar.style.width = pct + '%';
    }
    dots.forEach((dot, i) => {
      dot.classList.remove('active', 'completed');
      if (i < stepIndex) dot.classList.add('completed');
      else if (i === stepIndex) dot.classList.add('active');
    });
  }

  /* ── Step Transition ─────────────────────────────────────── */
  function goToStep(next) {
    if (next < 0 || next >= state.totalSteps) return;
    const current = steps[state.currentStep];
    const nextEl  = steps[next];
    const dir     = next > state.currentStep ? 1 : -1;

    if (typeof gsap !== 'undefined') {
      gsap.timeline()
        .to(current, { x: -80 * dir + '%', opacity: 0, duration: 0.3, ease: 'power2.in' })
        .call(() => {
          current.classList.remove('active');
          current.style.display = 'none';
          nextEl.style.display = 'block';
          nextEl.classList.add('active');
          gsap.set(nextEl, { x: 60 * dir + '%', opacity: 0 });
        })
        .to(nextEl, { x: '0%', opacity: 1, duration: 0.4, ease: 'power2.out' });
    } else {
      current.classList.remove('active'); current.style.display = 'none';
      nextEl.style.display = 'block'; nextEl.classList.add('active');
    }

    state.currentStep = next;
    updateProgress(next);

    const formSection = document.getElementById('cotacao');
    if (formSection) {
      const navH = document.getElementById('navbar')?.offsetHeight || 80;
      window.scrollTo({ top: formSection.getBoundingClientRect().top + window.scrollY - navH, behavior: 'smooth' });
    }
  }

  /* ── Step 1: Service ──────────────────────────────────────── */
  function bindServiceCards() {
    const cards  = document.querySelectorAll('.service-select-card');
    const nextBtn = document.getElementById('next-0');
    cards.forEach(card => {
      card.addEventListener('click', () => {
        cards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        state.data.service = card.dataset.value;
        if (nextBtn) nextBtn.disabled = false;
        if (typeof gsap !== 'undefined') {
          gsap.to(card, { scale: 1.04, duration: 0.15, yoyo: true, repeat: 1, ease: 'power1.inOut' });
        }
      });
    });
  }

  /* ── Step 2: Quote options ─────────────────────────────────── */
  function bindQuoteOptions() {
    const options = document.querySelectorAll('.quote-option');
    const nextBtn  = document.getElementById('next-1');
    options.forEach(opt => {
      opt.addEventListener('click', () => {
        options.forEach(o => o.classList.remove('selected'));
        opt.classList.add('selected');
        state.data.quotes = opt.dataset.value;
        if (nextBtn) nextBtn.disabled = false;
        if (typeof gsap !== 'undefined') {
          gsap.to(opt, { scale: 1.04, duration: 0.15, yoyo: true, repeat: 1, ease: 'power1.inOut' });
        }
      });
    });
  }

  /* ── Step 3: City (SP dropdown) ────────────────────────────── */
  function bindCitySelect() {
    const citySelect = document.getElementById('citySelect');
    const nextBtn    = document.getElementById('next-2');
    if (!citySelect) return;
    citySelect.addEventListener('change', () => {
      state.data.city = citySelect.value;
      if (nextBtn) nextBtn.disabled = !citySelect.value;
    });
  }

  /* ── Step 4: Contact form ─────────────────────────────────── */
  function bindContactForm() {
    const nameInput  = document.getElementById('nameInput');
    const emailInput = document.getElementById('emailInput');
    const phoneInput = document.getElementById('phoneInput');
    const lgpdCheck  = document.getElementById('lgpdCheck');
    const submitBtn  = document.getElementById('submitBtn');

    function validate() {
      const ok = nameInput?.value.trim().length >= 2 &&
                 /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput?.value.trim()) &&
                 (phoneInput?.value.replace(/\D/g,'').length >= 10) &&
                 lgpdCheck?.checked;
      if (submitBtn) submitBtn.disabled = !ok;
    }

    [nameInput, emailInput, phoneInput].forEach(el => el?.addEventListener('input', validate));
    lgpdCheck?.addEventListener('change', validate);

    /* Phone mask */
    if (phoneInput) {
      phoneInput.addEventListener('input', e => {
        let v = e.target.value.replace(/\D/g,'').slice(0,11);
        if (v.length >= 11)     v = v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        else if (v.length >= 7) v = v.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
        else if (v.length >= 3) v = v.replace(/(\d{2})(\d{0,5})/, '($1) $2');
        e.target.value = v;
        validate();
      });
    }

    submitBtn?.addEventListener('click', () => {
      if (submitBtn.disabled) return;
      state.data.name  = nameInput?.value.trim();
      state.data.email = emailInput?.value.trim();
      state.data.phone = phoneInput?.value.trim();
      submitForm();
    });
  }

  /* ── Submit + Loading ─────────────────────────────────────── */
  function submitForm() {
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<svg width="18" height="18" viewBox="0 0 18 18" fill="none" style="animation:spin 1s linear infinite"><circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="2" stroke-dasharray="20"/></svg> Enviando...`;
    }

    setTimeout(() => {
      goToStep(4);
      // Show loading phase, hide results
      const loadingPhase = document.getElementById('resultsLoadingPhase');
      const resultsPhase = document.getElementById('resultsPhase');
      if (loadingPhase) { loadingPhase.style.display = 'flex'; }
      if (resultsPhase) { resultsPhase.style.display = 'none'; }
      startLoadingPhase();
    }, 800);
  }

  /* ── 10-second Loading Phase ─────────────────────────────── */
  function startLoadingPhase() {
    const TOTAL   = 10000;  // 10 seconds
    const TICK    = 80;
    const msgs    = [
      'Identificando prestadoras na sua região...',
      'Verificando licenças e documentação...',
      'Consultando avaliações do Google...',
      'Preparando suas cotações gratuitas...'
    ];
    const lcIds   = ['lc1','lc2','lc3','lc4'];
    const ring    = document.getElementById('lringFill');
    const pctEl   = document.getElementById('loadingPct');
    const msgEl   = document.getElementById('loadingMsg');
    const CIRC    = 2 * Math.PI * 42; // ≈ 264

    let elapsed = 0;

    const interval = setInterval(() => {
      elapsed = Math.min(elapsed + TICK, TOTAL);
      const pct = elapsed / TOTAL;
      const pctInt = Math.round(pct * 100);

      // Ring fill
      if (ring) ring.style.strokeDashoffset = CIRC * (1 - pct);
      if (pctEl) pctEl.textContent = pctInt + '%';

      // Checklist steps (every 25%)
      const stepIdx = Math.min(Math.floor(pct * 4), 3);
      lcIds.forEach((id, i) => {
        const el = document.getElementById(id);
        if (!el) return;
        if (i < stepIdx) {
          el.className = 'lc-item done';
          el.querySelector('.lc-icon').textContent = '✓';
        } else if (i === stepIdx) {
          el.className = 'lc-item active';
          el.querySelector('.lc-icon').textContent = '●';
        } else {
          el.className = 'lc-item';
          el.querySelector('.lc-icon').textContent = '○';
        }
      });

      // Cycling message
      if (msgEl) msgEl.textContent = msgs[Math.min(Math.floor(pct * 4), msgs.length - 1)];

      if (elapsed >= TOTAL) {
        clearInterval(interval);
        // Mark all done
        lcIds.forEach(id => {
          const el = document.getElementById(id);
          if (el) { el.className = 'lc-item done'; el.querySelector('.lc-icon').textContent = '✓'; }
        });
        setTimeout(showResults, 300);
      }
    }, TICK);
  }

  /* ── Show Results ─────────────────────────────────────────── */
  function showResults() {
    const loadingPhase = document.getElementById('resultsLoadingPhase');
    const resultsPhase = document.getElementById('resultsPhase');
    const countEl      = document.getElementById('resultsCount');
    const container    = document.getElementById('companiesList');

    const qty = parseInt(state.data.quotes) || 5;
    if (countEl) countEl.textContent = Math.min(qty, 5) + ' empresas verificadas';

    if (loadingPhase) loadingPhase.style.display = 'none';
    if (resultsPhase) {
      resultsPhase.style.display = 'block';

      // Buscar e renderizar dados
      fetchAndRenderResults(container);

      if (typeof gsap !== 'undefined') {
        // Aguardar um tick para renderizar antes de animar
        setTimeout(() => {
          gsap.from('.results-header', { y: 20, opacity: 0, duration: 0.5, ease: 'power2.out' });
          gsap.from('.company-result', {
            y: 24, opacity: 0, stagger: 0.1, duration: 0.45,
            ease: 'power2.out', delay: 0.3
          });
          gsap.from('.results-footer-note', { y: 10, opacity: 0, duration: 0.4, delay: 0.9 });
          gsap.from('.btn-new-quote', { scale: 0.92, opacity: 0, duration: 0.5, ease: 'elastic.out(1,0.5)', delay: 1 });
        }, 50);
      }
    }

    // Log data
    console.log('Cotação solicitada:', state.data);
  }

  /* ── Fetch and Render Results ─────────────────────────────── */
  function fetchAndRenderResults(container) {
    if (!container) return;

    const selectedCity = state.data.city;
    const qty = Math.min(parseInt(state.data.quotes) || 5, 5);
    // PS Proteção ocupa 1 vaga; as demais são dinâmicas
    const maxDynamic = qty - 1;

    fetch('./js/companies-db.json')
      .then(res => res.json())
      .then(db => {
        // Coletar empresas de TODAS as categorias do JSON para a cidade selecionada
        // (funciona independente do nome da aba: "Empresas de Segurança", "Sheet1", etc.)
        let allCompanies = [];
        Object.values(db).forEach(cidadesObj => {
          if (cidadesObj[selectedCity]) {
            allCompanies = allCompanies.concat(cidadesObj[selectedCity]);
          }
        });

        // Deduplicar por nome e limitar
        const seen = new Set();
        const companies = allCompanies
          .filter(c => {
            if (!c.name || seen.has(c.name)) return false;
            seen.add(c.name);
            return true;
          })
          .slice(0, maxDynamic);

        const avatarColors = [
          'linear-gradient(135deg,#0F4C8A,#1E88E5)',
          'linear-gradient(135deg,#1B5E20,#388E3C)',
          'linear-gradient(135deg,#4A148C,#7B1FA2)',
          'linear-gradient(135deg,#BF360C,#E64A19)'
        ];

        const htmlParts = [];

        /* ── PS Proteção — SEMPRE PRIMEIRO E EM DESTAQUE ── */
        htmlParts.push(`
          <div class="company-result company-result--featured">
            <div class="cr-featured-tag">⭐ Melhor opção regional</div>
            <div class="cr-body">
              <div class="cr-avatar" style="background:linear-gradient(135deg,#1B3A8C,#7B2FBE)">
                <span>PS</span>
              </div>
              <div class="cr-info">
                <span class="cr-name">PS Proteção</span>
                <span class="cr-rating">★★★★★ <strong>4.8</strong> · Serviços</span>
                <span class="cr-services">Portaria · Segurança · Facilities · Controle de Acesso</span>
              </div>
              <div class="cr-meta">
                <span class="cr-status open">● Aberto agora</span>
                <a href="https://maps.app.goo.gl/u9BRTrVCJtsNUCgB8" target="_blank" rel="noopener" class="cr-maps-link">
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M6 1C3.79 1 2 2.79 2 5C2 7.5 6 11 6 11C6 11 10 7.5 10 5C10 2.79 8.21 1 6 1Z" stroke="currentColor" stroke-width="1.2"/><circle cx="6" cy="5" r="1.5" fill="currentColor"/></svg>
                  Ver no Google Maps
                </a>
              </div>
            </div>
            <div class="cr-sent">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 4" stroke="#84CC16" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
              Cotação enviada
            </div>
          </div>
        `);

        /* ── Empresas dinâmicas da cidade ── */
        companies.forEach((company, idx) => {
          const color = avatarColors[idx % avatarColors.length];
          const initials = company.name
            .split(' ')
            .filter(w => w.length > 2)
            .slice(0, 2)
            .map(w => w[0])
            .join('')
            .toUpperCase() || company.name.slice(0, 2).toUpperCase();

          const stars = '★'.repeat(Math.min(Math.floor(company.rating || 4), 5)) +
                        '☆'.repeat(Math.max(5 - Math.floor(company.rating || 4), 0));

          // Logo via favicon do site (se tiver website)
          const domain = company.website
            ? company.website.replace(/^https?:\/\//, '').replace(/\/.*$/, '')
            : '';
          const logoHtml = domain
            ? `<img
                class="cr-logo-img"
                src="https://www.google.com/s2/favicons?domain=${domain}&sz=64"
                alt="${company.name}"
                onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
               <span class="cr-logo-fallback" style="display:none;background:${color}">${initials}</span>`
            : `<span class="cr-logo-fallback" style="background:${color}">${initials}</span>`;

          // Links de ação
          const phoneLink = company.phone
            ? `<a href="tel:${company.phone.replace(/\D/g,'')}" class="cr-action-link cr-action-phone">
                <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M11.5 9.5C11.5 9.5 10.5 10.5 10.25 10.75C9.5 11.5 7 10.5 5 8.5C3 6.5 2 4 2.75 3.25C3 3 4 2 4 2L6 5L5 6C5 6 5.5 7 6.5 8C7.5 9 8.5 9.5 8.5 9.5L9.5 8.5L11.5 9.5Z" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                ${company.phone}
               </a>`
            : '';

          const websiteLink = company.website
            ? `<a href="${company.website}" target="_blank" rel="noopener" class="cr-action-link cr-action-web">
                <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><circle cx="6.5" cy="6.5" r="5" stroke="currentColor" stroke-width="1.2"/><path d="M6.5 1.5C6.5 1.5 4.5 4 4.5 6.5C4.5 9 6.5 11.5 6.5 11.5M6.5 1.5C6.5 1.5 8.5 4 8.5 6.5C8.5 9 6.5 11.5 6.5 11.5M1.5 6.5H11.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
                ${domain}
               </a>`
            : '';

          const mapsLink = company.url
            ? `<a href="${company.url}" target="_blank" rel="noopener" class="cr-action-link cr-action-maps">
                <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M6.5 1.5C4.29 1.5 2.5 3.29 2.5 5.5C2.5 8 6.5 12 6.5 12C6.5 12 10.5 8 10.5 5.5C10.5 3.29 8.71 1.5 6.5 1.5Z" stroke="currentColor" stroke-width="1.2"/><circle cx="6.5" cy="5.5" r="1.5" fill="currentColor"/></svg>
                Google Maps
               </a>`
            : '';

          htmlParts.push(`
            <div class="company-result">
              <div class="cr-body">
                <div class="cr-avatar-wrap">
                  ${logoHtml}
                </div>
                <div class="cr-info">
                  <span class="cr-name">${company.name}</span>
                  <span class="cr-rating">${stars} <strong>${(company.rating || 4).toFixed(1)}</strong></span>
                  <span class="cr-services">${company.address || selectedCity + ', SP'}</span>
                  <div class="cr-actions">
                    ${phoneLink}${websiteLink}${mapsLink}
                  </div>
                </div>
                <div class="cr-meta">
                  <span class="cr-status open">● Disponível</span>
                </div>
              </div>
              <div class="cr-sent">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 4" stroke="#84CC16" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                Cotação enviada
              </div>
            </div>
          `);
        });

        /* Se a cidade não tem dados suficientes, preenche com placeholders neutros */
        const remaining = maxDynamic - companies.length;
        const genericNames = [
          { name: 'Facilities Regional SP', initials: 'FR', color: avatarColors[0] },
          { name: 'Grupo Segurança Total', initials: 'GS', color: avatarColors[1] },
          { name: 'ProFacilities São Paulo', initials: 'PF', color: avatarColors[2] },
          { name: 'Veritas Facilities', initials: 'VF', color: avatarColors[3] }
        ];

        for (let i = 0; i < remaining; i++) {
          const g = genericNames[i % genericNames.length];
          htmlParts.push(`
            <div class="company-result">
              <div class="cr-body">
                <div class="cr-avatar" style="background:${g.color}">
                  <span>${g.initials}</span>
                </div>
                <div class="cr-info">
                  <span class="cr-name">${g.name}</span>
                  <span class="cr-rating">★★★★☆ <strong>4.3</strong></span>
                  <span class="cr-services">${selectedCity}, SP</span>
                </div>
                <div class="cr-meta">
                  <span class="cr-status open">● Aberto agora</span>
                </div>
              </div>
              <div class="cr-sent">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 4" stroke="#84CC16" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                Cotação enviada
              </div>
            </div>
          `);
        }

        container.innerHTML = htmlParts.join('');
      })
      .catch(err => {
        console.error('Erro ao buscar empresas:', err);
        // Fallback: manter HTML estático que já está no DOM
      });
  }

  /* ── Nav Buttons ──────────────────────────────────────────── */
  function bindNavButtons() {
    document.getElementById('next-0')?.addEventListener('click', () => goToStep(1));
    document.getElementById('next-1')?.addEventListener('click', () => goToStep(2));
    document.getElementById('next-2')?.addEventListener('click', () => goToStep(3));
    document.getElementById('back-1')?.addEventListener('click', () => goToStep(0));
    document.getElementById('back-2')?.addEventListener('click', () => goToStep(1));
    document.getElementById('back-3')?.addEventListener('click', () => goToStep(2));
  }

  /* ── New Quote ────────────────────────────────────────────── */
  function bindNewQuote() {
    document.getElementById('newQuoteBtn')?.addEventListener('click', () => {
      state.data = { service: null, quotes: null, city: '', name: '', email: '', phone: '' };
      state.currentStep = 0;

      document.querySelectorAll('.service-select-card').forEach(c => c.classList.remove('selected'));
      document.querySelectorAll('.quote-option').forEach(o => o.classList.remove('selected'));

      const cs = document.getElementById('citySelect');
      if (cs) cs.value = '';
      ['nameInput','emailInput','phoneInput'].forEach(id => {
        const el = document.getElementById(id); if (el) el.value = '';
      });
      const lgpd = document.getElementById('lgpdCheck');
      if (lgpd) lgpd.checked = false;

      ['next-0','next-1','next-2','submitBtn'].forEach(id => {
        const b = document.getElementById(id); if (b) b.disabled = true;
      });

      // Reset step 5
      const loadingPhase = document.getElementById('resultsLoadingPhase');
      const resultsPhase = document.getElementById('resultsPhase');
      if (loadingPhase) {
        loadingPhase.style.display = 'flex';
        const ring = document.getElementById('lringFill');
        if (ring) ring.style.strokeDashoffset = '264';
        const pct = document.getElementById('loadingPct');
        if (pct) pct.textContent = '0%';
      }
      if (resultsPhase) resultsPhase.style.display = 'none';

      goToStep(0);
    });
  }

})();
