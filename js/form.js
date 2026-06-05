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
    
    // SEO Programático: Pre-selecionar cidade se informada
    if (window.PRESELECTED_CITY) {
      const citySelect = document.getElementById('citySelect');
      if (citySelect) {
        citySelect.value = window.PRESELECTED_CITY;
        state.data.city = window.PRESELECTED_CITY;
        const nextBtn = document.getElementById('next-2');
        if (nextBtn) nextBtn.disabled = false;
      }
    }
    
    // SEO Programático: Pre-selecionar serviço se informado
    if (window.PRESELECTED_SERVICE) {
      state.data.service = window.PRESELECTED_SERVICE;
      const nextBtn0 = document.getElementById('next-0');
      if (nextBtn0) nextBtn0.disabled = false;
      const card = document.querySelector(`.service-select-card[data-value="${window.PRESELECTED_SERVICE}"]`);
      if (card) card.classList.add('selected');
    }
    
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

  /* ── Show Success Screen ──────────────────────────────────── */
  function showResults() {
    const loadingPhase = document.getElementById('resultsLoadingPhase');
    const resultsPhase = document.getElementById('resultsPhase');

    if (loadingPhase) loadingPhase.style.display = 'none';
    if (!resultsPhase) return;

    // Preencher resumo do pedido
    const serviceLabels = {
      'portaria':       'Portaria & Recepção',
      'controle-acesso':'Controle de Acesso',
      'seguranca':      'Segurança Patrimonial',
      'limpeza':        'Limpeza & Conservação',
      'manutencao':     'Manutenção Predial',
      'mao-de-obra':    'Mão de Obra Especializada'
    };
    const quotesLabels = { '3': '3 cotações', '5': '5 cotações', '10': '10+ cotações' };

    const summaryService = document.getElementById('summaryService');
    const summaryCity    = document.getElementById('summaryCity');
    const summaryQuotes  = document.getElementById('summaryQuotes');
    const summaryContact = document.getElementById('summaryContact');

    if (summaryService) summaryService.textContent = serviceLabels[state.data.service] || state.data.service || '—';
    if (summaryCity)    summaryCity.textContent    = state.data.city || '—';
    if (summaryQuotes)  summaryQuotes.textContent  = quotesLabels[state.data.quotes] || state.data.quotes || '—';
    if (summaryContact) summaryContact.textContent = state.data.name ? `${state.data.name} · ${state.data.phone}` : '—';

    resultsPhase.style.display = 'block';

    // Animar checkmark SVG
    const checkPath = resultsPhase.querySelector('.success-check-path');
    if (checkPath && typeof gsap !== 'undefined') {
      const len = checkPath.getTotalLength ? checkPath.getTotalLength() : 60;
      gsap.set(checkPath, { strokeDasharray: len, strokeDashoffset: len });
      gsap.to(checkPath, { strokeDashoffset: 0, duration: 0.6, ease: 'power2.out', delay: 0.2 });
    }

    // Animar elementos em cascata
    if (typeof gsap !== 'undefined') {
      gsap.from('.success-icon-wrap', { scale: 0.5, opacity: 0, duration: 0.5, ease: 'back.out(1.7)' });
      gsap.from('.success-header',   { y: 20, opacity: 0, duration: 0.5, ease: 'power2.out', delay: 0.3 });
      gsap.from('.success-summary',  { y: 16, opacity: 0, duration: 0.45, ease: 'power2.out', delay: 0.5 });
      gsap.from('.success-badges',   { y: 12, opacity: 0, duration: 0.4, ease: 'power2.out', delay: 0.7 });
      gsap.from('.btn-new-quote',    { scale: 0.9, opacity: 0, duration: 0.5, ease: 'elastic.out(1,0.5)', delay: 0.9 });
    }

    // Enviar email com os dados do lead
    sendLeadEmail();

    console.log('Lead capturado:', state.data);
  }

  /* ── Envio de email via Web3Forms ─────────────────────────── */
  function sendLeadEmail() {
    const WEB3FORMS_KEY = 'COLE_SUA_CHAVE_AQUI'; // ← substitua pela sua chave

    const serviceLabels = {
      'portaria':       'Portaria & Recepção',
      'controle-acesso':'Controle de Acesso',
      'seguranca':      'Segurança Patrimonial',
      'limpeza':        'Limpeza & Conservação',
      'manutencao':     'Manutenção Predial',
      'mao-de-obra':    'Mão de Obra Especializada'
    };

    const payload = {
      access_key: WEB3FORMS_KEY,
      subject:    `[Cota Facilities] Novo lead — ${serviceLabels[state.data.service] || state.data.service} em ${state.data.city}`,
      from_name:  'Cota Facilities',
      message: `
🎯 NOVO LEAD — COTA FACILITIES
================================

👤 Nome:     ${state.data.name}
📧 Email:    ${state.data.email}
📱 Telefone: ${state.data.phone}

🏢 Serviço:  ${serviceLabels[state.data.service] || state.data.service}
📍 Cidade:   ${state.data.city}
📋 Cotações: ${state.data.quotes} cotações solicitadas

================================
Recebido em: ${new Date().toLocaleString('pt-BR')}
      `.trim()
    };

    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) console.log('Email enviado com sucesso!');
      else console.warn('Web3Forms erro:', data);
    })
    .catch(err => console.error('Falha ao enviar email:', err));
  }

  /* ── Fetch and Render Results ─────────────────────────────── */
  function fetchAndRenderResults(container) {
    if (!container) return;

    const selectedCity = state.data.city;
    const qty = Math.min(parseInt(state.data.quotes) || 5, 5);
    // PS Proteção ocupa 1 vaga; as demais são dinâmicas
    const maxDynamic = qty - 1;

    // Detectar prefixo de caminho relativo baseado no CSS da página
    const cssLink = document.querySelector('link[href*="css/layout.css"]') || document.querySelector('link[href*="css/main.css"]');
    const pathPrefix = cssLink ? cssLink.getAttribute('href').split('css/')[0] : '';

    fetch(pathPrefix + 'js/companies-db.json')
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
            <div class="cr-featured-tag"><span class="cr-star-icon">⭐</span> Melhor opção regional</div>
            <div class="cr-body">
              <div class="cr-main-content">
                <div class="cr-avatar-wrap">
                  <img src="${pathPrefix}imagem.jpg" class="cr-logo-img" alt="PS Proteção">
                </div>
                <div class="cr-info">
                  <div class="cr-title-row">
                    <span class="cr-name">PS Proteção</span>
                    <span class="cr-badge-premium">Parceiro Verificado</span>
                  </div>
                  <div class="cr-rating-row">
                    <div class="cr-stars-visual">★★★★★</div>
                    <span class="cr-rating-number">4.8</span>
                  </div>
                  <div class="cr-address-row">
                    <svg class="cr-icon-location" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/></svg>
                    <span class="cr-address-text">Americana · São Paulo · Campinas (Matriz)</span>
                  </div>
                </div>
                <div class="cr-meta">
                  <span class="cr-status open"><span class="cr-pulse-dot"></span> Aberto agora</span>
                </div>
              </div>
            </div>
            <div class="cr-footer">
              <div class="cr-actions">
                <a href="https://maps.app.goo.gl/u9BRTrVCJtsNUCgB8" target="_blank" rel="noopener" class="btn-cr-action btn-cr-action--map">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  Ver no Mapa
                </a>
                <a href="https://protecaoevigilancia.com.br" target="_blank" rel="noopener" class="btn-cr-action btn-cr-action--website">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                  Acessar Site
                </a>
              </div>
              <div class="cr-sent-badge">
                <svg class="cr-icon-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Cotação Enviada</span>
              </div>
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

          htmlParts.push(`
            <div class="company-result">
              <div class="cr-body">
                <div class="cr-main-content">
                  <div class="cr-avatar-wrap">
                    ${logoHtml}
                  </div>
                  <div class="cr-info">
                    <div class="cr-title-row">
                      <span class="cr-name">${company.name}</span>
                    </div>
                    <div class="cr-rating-row">
                      <div class="cr-stars-visual">${stars}</div>
                      <span class="cr-rating-number">${(company.rating || 4).toFixed(1)}</span>
                    </div>
                    <div class="cr-address-row">
                      <svg class="cr-icon-location" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/></svg>
                      <span class="cr-address-text">${company.address || selectedCity + ', SP'}</span>
                    </div>
                  </div>
                  <div class="cr-meta">
                    <span class="cr-status open"><span class="cr-pulse-dot"></span> Disponível</span>
                  </div>
                </div>
              </div>
              <div class="cr-footer">
                <div class="cr-actions">
                  <span class="cr-not-filled">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                    Dados não preenchidos pela empresa
                  </span>
                </div>
                <div class="cr-sent-badge">
                  <svg class="cr-icon-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                  <span>Cotação Enviada</span>
                </div>
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
                <div class="cr-main-content">
                  <div class="cr-avatar-wrap">
                    <span class="cr-logo-fallback" style="background:${g.color}">${g.initials}</span>
                  </div>
                  <div class="cr-info">
                    <div class="cr-title-row">
                      <span class="cr-name">${g.name}</span>
                    </div>
                    <div class="cr-rating-row">
                      <div class="cr-stars-visual">★★★★☆</div>
                      <span class="cr-rating-number">4.3</span>
                    </div>
                    <div class="cr-address-row">
                      <svg class="cr-icon-location" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/></svg>
                      <span class="cr-address-text">${selectedCity}, SP</span>
                    </div>
                  </div>
                  <div class="cr-meta">
                    <span class="cr-status open"><span class="cr-pulse-dot"></span> Aberto agora</span>
                  </div>
                </div>
              </div>
              <div class="cr-footer">
                <div class="cr-actions">
                  <span class="cr-not-filled">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                    Dados não preenchidos pela empresa
                  </span>
                </div>
                <div class="cr-sent-badge">
                  <svg class="cr-icon-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                  <span>Cotação Enviada</span>
                </div>
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
