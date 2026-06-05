#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Páginas SEO Programático — Cota Facilities
Gera 4.080 páginas HTML + sitemap.xml
Uso: python gerar_paginas_seo.py
"""

import os, re, json, unicodedata
from datetime import date

# ── Configuração ───────────────────────────────────────────────────────────────

BASE_URL = "https://cotafacilities.com.br"

CIDADES = [
    "Campinas","Americana","Santa Bárbara d'Oeste","Nova Odessa","Sumaré",
    "Hortolândia","Paulínia","Valinhos","Vinhedo","Indaiatuba","Monte Mor",
    "Itatiba","Jaguariúna","Holambra","Pedreira","Santo Antônio de Posse",
    "Cosmópolis","Artur Nogueira","Engenheiro Coelho","Limeira","Iracemápolis",
    "Piracicaba","Elias Fausto","Capivari","Rafard","Louveira","Jundiaí",
    "Morungaba","Tietê","Mombuca","Rio Claro","Cordeirópolis","Araras","Leme",
    "Mogi Mirim","Mogi Guaçu","Estiva Gerbi","Conchal","Charqueada",
    "Santa Gertrudes","Águas de São Pedro","São Pedro","Saltinho",
    "Santa Maria da Serra","Anhembi","Botucatu","Boituva","Porto Feliz","Itu",
    "Salto","Cabreúva","Itupeva","Várzea Paulista","Campo Limpo Paulista",
    "Atibaia","Bragança Paulista","Pinhalzinho","Amparo","Serra Negra","Socorro",
]

SERVICOS = [
    ("Portaria",                       "portaria"),
    ("Controle de Acesso",             "controle-de-acesso"),
    ("Portaria e Controle de Acesso",  "portaria-e-controle-de-acesso"),
    ("Limpeza",                        "limpeza"),
    ("Limpeza e Conservação",          "limpeza-e-conservacao"),
    ("Jardinagem",                     "jardinagem"),
    ("Zelador",                        "zelador"),
    ("Zeladoria",                      "zeladoria"),
    ("Recepcionista",                  "recepcionista"),
    ("Recepção",                       "recepcao"),
    ("Vigia",                          "vigia"),
    ("Guarda",                         "guarda"),
    ("Segurança",                      "seguranca"),
    ("Vigilante",                      "vigilante"),
    ("Rondas de Segurança",            "rondas-de-seguranca"),
    ("Portaria para Condomínio",       "portaria-para-condominio"),
    ("Segurança para Empresa",         "seguranca-para-empresa"),
]

INTENCOES = [
    {
        "slug":  "cotacao",
        "h1":    "Cotação de {s} em {c}",
        "title": "Cotação de {s} em {c} — Grátis e Rápido | Cota Facilities",
        "desc":  "Solicite cotação de {s} em {c} gratuitamente. Receba propostas de empresas verificadas em até 24h. Compare preços e escolha a melhor. 100% grátis.",
        "intro": "Precisa de cotação de <strong>{s}</strong> em <strong>{c}</strong>? A Cota Facilities conecta você com fornecedores credenciados de {c} e região — sem burocracia, sem ligações e 100% gratuito.",
    },
    {
        "slug":  "orcamento",
        "h1":    "Orçamento de {s} em {c}",
        "title": "Orçamento de {s} em {c} — Sem Compromisso | Cota Facilities",
        "desc":  "Peça orçamento de {s} em {c} sem custo. Empresas credenciadas enviam propostas em até 24h. Compare e feche o melhor negócio.",
        "intro": "Quer orçamento de <strong>{s}</strong> em <strong>{c}</strong> sem perder tempo com ligações? Preencha um formulário rápido e receba propostas de empresas verificadas que atendem {c}.",
    },
    {
        "slug":  "cotacoes-rapidas",
        "h1":    "5 Cotações Rápidas de {s} em {c}",
        "title": "5 Cotações de {s} em {c} — Rápido e Gratuito | Cota Facilities",
        "desc":  "Receba até 5 cotações de {s} em {c} em minutos. Compare fornecedores verificados em {c} e contrate o melhor. Gratuito e sem burocracia.",
        "intro": "Receba até <strong>5 cotações</strong> de <strong>{s}</strong> em <strong>{c}</strong> de uma só vez. Nossa plataforma notifica os melhores fornecedores de {c} automaticamente — você só compara e escolhe.",
    },
    {
        "slug":  "fornecedores",
        "h1":    "Melhores Fornecedores de {s} em {c}",
        "title": "Melhores Fornecedores de {s} em {c} | Cota Facilities",
        "desc":  "Encontre os melhores fornecedores de {s} em {c}. Empresas verificadas, avaliadas e credenciadas. Solicite cotação gratuita e compare propostas.",
        "intro": "Encontre os <strong>melhores fornecedores de {s}</strong> em <strong>{c}</strong>. A Cota Facilities reúne empresas verificadas, com documentação em dia e histórico de atendimento em {c} e região.",
    },
]

# ── FAQ personalizado por intenção ─────────────────────────────────────────────

FAQ_SETS = {
    "cotacao": [
        ("Quanto custa {s} em {c}?",
         "O custo de {s} em {c} varia conforme carga horária, quantidade de postos e perfil profissional exigido. Para obter valores precisos do mercado em {c}, solicite cotação gratuita na Cota Facilities e compare propostas de empresas verificadas."),
        ("Como solicitar cotação de {s} em {c}?",
         "Pelo site da Cota Facilities, preencha o formulário em menos de 2 minutos: informe o serviço ({s}), a cidade ({c}) e seus dados de contato. Em até 24h, fornecedores credenciados de {c} entrarão em contato com suas propostas."),
        ("Quais empresas de {s} atendem {c}?",
         "A Cota Facilities conta com uma rede de prestadoras verificadas que atendem {c} e região. Ao solicitar cotação de {s} em {c}, a plataforma notifica automaticamente os fornecedores disponíveis na sua área."),
        ("O processo de cotação de {s} em {c} é gratuito?",
         "Sim, 100% gratuito para quem contrata. A Cota Facilities não cobra nenhum valor para solicitar cotações de {s} em {c}. Você recebe as propostas, compara e decide sem compromisso."),
        ("Quanto tempo leva para receber cotações de {s} em {c}?",
         "Após preencher o formulário, você recebe as primeiras propostas de {s} em {c} em até 24 horas. Em cidades como {c}, com maior concentração de fornecedores, o retorno costuma ser ainda mais rápido."),
        ("Vale a pena terceirizar {s} em {c}?",
         "Sim. A terceirização de {s} em {c} elimina encargos trabalhistas, custos de recrutamento e gestão direta de pessoal. As empresas especializadas de {c} garantem cobertura de faltas, férias e substituições sem impactar sua operação."),
    ],
    "orcamento": [
        ("Como pedir orçamento de {s} em {c}?",
         "Para pedir orçamento de {s} em {c}, acesse a Cota Facilities, preencha o formulário com as informações do serviço e sua localização em {c}. Em até 24h, você recebe orçamentos detalhados de empresas credenciadas na sua região."),
        ("O orçamento de {s} em {c} tem custo?",
         "Não. Solicitar orçamento de {s} em {c} pela Cota Facilities é totalmente gratuito. A plataforma foi criada para facilitar a comparação de preços sem que o comprador precise ligar para diversas empresas."),
        ("O que influencia o orçamento de {s} em {c}?",
         "O orçamento de {s} em {c} depende de fatores como: número de profissionais necessários, carga horária (diurna, noturna ou 24h), especificações técnicas, localização dentro de {c} e o nível de experiência exigido. Solicite orçamentos múltiplos para comparar."),
        ("Posso negociar o orçamento de {s} em {c}?",
         "Sim. Ao receber os orçamentos de {s} em {c} pela Cota Facilities, você pode negociar diretamente com os fornecedores. Ter múltiplas propostas da mesma cidade ({c}) já é um ótimo ponto de partida para a negociação."),
        ("Em quanto tempo o orçamento de {s} em {c} é enviado?",
         "Os fornecedores de {s} cadastrados em {c} recebem sua solicitação imediatamente e têm até 24 horas para enviar o orçamento. O processo é automatizado para garantir agilidade, especialmente em {c} e municípios próximos."),
        ("Existe contrato mínimo para {s} em {c}?",
         "Depende do fornecedor. Ao solicitar orçamento de {s} em {c}, cada empresa apresenta suas condições contratuais. A Cota Facilities recomenda comparar pelo menos 3 propostas antes de assinar qualquer contrato em {c}."),
    ],
    "cotacoes-rapidas": [
        ("Como receber 5 cotações de {s} em {c} rapidamente?",
         "Preencha o formulário da Cota Facilities em menos de 2 minutos, selecione {s} e informe que está em {c}. Nossa plataforma notifica automaticamente até 5 fornecedores verificados de {c} e região — você recebe as propostas em até 24h."),
        ("Por que solicitar múltiplas cotações de {s} em {c}?",
         "Solicitar 5 cotações de {s} em {c} ao mesmo tempo permite comparar preços, condições de contrato e perfil das empresas. Empresas de {c} costumam ter variação de 15% a 40% entre si, tornando a comparação essencial para uma boa contratação."),
        ("As 5 cotações de {s} em {c} são de empresas diferentes?",
         "Sim. A Cota Facilities conecta você com fornecedores independentes de {s} em {c}. Cada empresa envia sua proposta de forma separada, garantindo diversidade de preços e condições para você escolher a melhor."),
        ("Qual o prazo para as 5 cotações de {s} em {c} chegarem?",
         "Em geral, as 5 cotações de {s} em {c} chegam em até 24 horas. Em cidades com maior concentração de fornecedores como {c}, muitas propostas chegam no mesmo dia da solicitação."),
        ("As empresas de {s} em {c} são verificadas?",
         "Sim. Todos os fornecedores de {s} cadastrados em {c} na Cota Facilities passam por validação de CNPJ, documentação fiscal, alvarás e licenças antes de acessar a plataforma. Você recebe apenas propostas de empresas regularizadas em {c}."),
        ("Posso escolher menos que 5 cotações de {s} em {c}?",
         "Sim. Na plataforma você escolhe receber 3, 5 ou mais cotações de {s} em {c}. Para contratos maiores ou mais complexos em {c}, recomendamos solicitar o máximo de propostas para ter mais poder de comparação."),
    ],
    "fornecedores": [
        ("Como encontrar bons fornecedores de {s} em {c}?",
         "A Cota Facilities reúne os melhores fornecedores de {s} em {c} — todos verificados e com documentação em dia. Solicite cotação gratuita e receba propostas de empresas com histórico comprovado de atendimento em {c}."),
        ("O que diferencia os melhores fornecedores de {s} em {c}?",
         "Os melhores fornecedores de {s} em {c} se destacam por: regularidade fiscal e trabalhista, tempo de mercado, avaliações de clientes, capacidade de cobertura na cidade de {c} e qualidade dos profissionais. A Cota Facilities verifica todos esses critérios."),
        ("Como avaliar fornecedores de {s} em {c}?",
         "Ao receber propostas de fornecedores de {s} em {c}, avalie: preço, prazo de início, política de substituição, experiência comprovada em {c} e referências de outros clientes na região. A Cota Facilities facilita essa comparação numa única plataforma."),
        ("Os fornecedores de {s} em {c} são regularizados?",
         "Sim. Todos os fornecedores de {s} listados em {c} na Cota Facilities passam por análise de CNPJ, certidões negativas, alvarás municipais e estaduais. Você não corre o risco de contratar empresas irregulares em {c}."),
        ("Quantos fornecedores de {s} atendem {c}?",
         "A Cota Facilities conta com uma rede crescente de fornecedores de {s} em {c} e municípios vizinhos. Ao solicitar cotação, você descobre quais estão disponíveis e com capacidade para atender sua demanda em {c} agora."),
        ("Como contratar um fornecedor de {s} em {c} com segurança?",
         "Para contratar {s} em {c} com segurança: solicite múltiplas cotações, verifique a documentação da empresa, peça referências de outros clientes em {c} e formalize tudo em contrato. A Cota Facilities fornece acesso apenas a empresas pré-verificadas."),
    ],
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def slugify(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "-", text.strip())
    return text

# ── Gerador de HTML ────────────────────────────────────────────────────────────

def gerar_faq_html(servico, cidade, intencao_slug):
    perguntas = FAQ_SETS[intencao_slug]
    itens = []
    for q_tpl, a_tpl in perguntas:
        q = q_tpl.format(s=servico, c=cidade)
        a = a_tpl.format(s=servico, c=cidade)
        itens.append(f"""
    <div class="seo-faq-item">
      <button class="seo-faq-q" onclick="this.parentElement.classList.toggle('open')">
        {q}
        <svg class="seo-faq-arrow" width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M5 8L10 13L15 8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <div class="seo-faq-a"><p>{a}</p></div>
    </div>""")
    return "\n".join(itens)

def gerar_faq_schema(servico, cidade, intencao_slug):
    perguntas = FAQ_SETS[intencao_slug]
    items = []
    for q_tpl, a_tpl in perguntas:
        q = q_tpl.format(s=servico, c=cidade)
        a = a_tpl.format(s=servico, c=cidade)
        items.append({"@type": "Question", "name": q,
                      "acceptedAnswer": {"@type": "Answer", "text": a}})
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": items}, ensure_ascii=False, indent=2)

def gerar_breadcrumb_schema(intencao, servico_nome, servico_slug, cidade, cidade_slug):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início",
             "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": intencao["h1"].split(" de ")[0],
             "item": f"{BASE_URL}/{intencao['slug']}/"},
            {"@type": "ListItem", "position": 3, "name": servico_nome,
             "item": f"{BASE_URL}/{intencao['slug']}/{servico_slug}/"},
            {"@type": "ListItem", "position": 4, "name": cidade,
             "item": f"{BASE_URL}/{intencao['slug']}/{servico_slug}/{cidade_slug}/"},
        ]
    }, ensure_ascii=False, indent=2)

def gerar_pagina(intencao, servico_nome, servico_slug, cidade, cidade_slug):
    h1    = intencao["h1"].format(s=servico_nome, c=cidade)
    title = intencao["title"].format(s=servico_nome, c=cidade)
    desc  = intencao["desc"].format(s=servico_nome, c=cidade)
    intro = intencao["intro"].format(s=servico_nome, c=cidade)
    faq_html   = gerar_faq_html(servico_nome, cidade, intencao["slug"])
    faq_schema = gerar_faq_schema(servico_nome, cidade, intencao["slug"])
    bc_schema  = gerar_breadcrumb_schema(intencao, servico_nome, servico_slug, cidade, cidade_slug)
    canonical  = f"{BASE_URL}/{intencao['slug']}/{servico_slug}/{cidade_slug}/"
    # Relative path back to root (always 3 levels deep)
    root = "../../../"

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}css/main.css">
  <link rel="stylesheet" href="{root}css/components.css">
  <script type="application/ld+json">{faq_schema}</script>
  <script type="application/ld+json">{bc_schema}</script>
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#0F172A;color:#E2E8F0;font-family:'Outfit',sans-serif;line-height:1.6}}
    .seo-nav{{position:sticky;top:0;z-index:100;background:rgba(15,23,42,.92);backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,255,255,.07);padding:14px 24px;display:flex;align-items:center;justify-content:space-between}}
    .seo-nav img{{height:34px}}
    .seo-nav-cta{{background:linear-gradient(90deg,#7C3AED,#1B3A8C);color:#fff;font-weight:700;font-size:14px;padding:9px 20px;border-radius:999px;text-decoration:none;transition:opacity .2s}}
    .seo-nav-cta:hover{{opacity:.85}}
    .seo-hero{{max-width:820px;margin:0 auto;padding:72px 24px 56px;text-align:center}}
    .seo-breadcrumb{{font-size:12px;color:#64748B;margin-bottom:24px}}
    .seo-breadcrumb a{{color:#7B2FBE;text-decoration:none}}
    .seo-breadcrumb a:hover{{text-decoration:underline}}
    .seo-hero h1{{font-size:clamp(28px,4.5vw,52px);font-weight:700;line-height:1.15;color:#fff;letter-spacing:-.02em;margin-bottom:20px}}
    .seo-hero p{{font-size:clamp(15px,2vw,18px);color:#94A3B8;max-width:600px;margin:0 auto 36px;line-height:1.7}}
    .seo-hero p strong{{color:#fff}}
    .seo-cta-wrap{{display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;margin-bottom:48px}}
    .btn-seo-primary{{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(90deg,#84CC16,#65A30D);color:#0F172A;font-weight:700;font-size:16px;padding:15px 32px;border-radius:999px;text-decoration:none;transition:transform .2s,box-shadow .2s}}
    .btn-seo-primary:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(132,204,22,.35)}}
    .seo-trust{{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap}}
    .seo-trust-item{{display:flex;align-items:center;gap:6px;font-size:12px;color:#64748B}}
    .seo-trust-item svg{{color:#84CC16}}
    .seo-faq-section{{max-width:780px;margin:0 auto;padding:0 24px 80px}}
    .seo-faq-section h2{{font-size:clamp(20px,3vw,28px);font-weight:700;color:#fff;margin-bottom:32px;text-align:center}}
    .seo-faq-item{{border:1px solid rgba(255,255,255,.07);border-radius:14px;margin-bottom:12px;overflow:hidden;transition:border-color .2s}}
    .seo-faq-item.open{{border-color:rgba(123,47,190,.5)}}
    .seo-faq-q{{width:100%;background:rgba(255,255,255,.03);border:none;color:#E2E8F0;font-family:'Outfit',sans-serif;font-size:15px;font-weight:600;padding:18px 20px;text-align:left;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:12px;transition:background .2s}}
    .seo-faq-q:hover{{background:rgba(255,255,255,.06)}}
    .seo-faq-arrow{{flex-shrink:0;transition:transform .3s;color:#7B2FBE}}
    .seo-faq-item.open .seo-faq-arrow{{transform:rotate(180deg)}}
    .seo-faq-a{{max-height:0;overflow:hidden;transition:max-height .4s ease,padding .3s}}
    .seo-faq-item.open .seo-faq-a{{max-height:300px;padding:0 20px 20px}}
    .seo-faq-a p{{font-size:14px;color:#94A3B8;line-height:1.7}}
    .seo-footer{{border-top:1px solid rgba(255,255,255,.06);padding:32px 24px;text-align:center;color:#475569;font-size:13px}}
    .seo-footer a{{color:#7B2FBE;text-decoration:none}}
    .seo-divider{{height:1px;background:linear-gradient(90deg,transparent,rgba(123,47,190,.3),transparent);margin:0 24px 64px}}
  </style>
</head>
<body>

  <!-- Navbar -->
  <nav class="seo-nav">
    <a href="{root}"><img src="{root}cota.png" alt="Cota Facilities"></a>
    <a href="{root}#cotacao" class="seo-nav-cta">Solicitar Cotação Gratuita →</a>
  </nav>

  <!-- Hero -->
  <section class="seo-hero">
    <p class="seo-breadcrumb">
      <a href="{root}">Início</a> › <a href="{root}{intencao['slug']}/">{intencao["h1"].split(" de ")[0]}</a> › <a href="{root}{intencao['slug']}/{servico_slug}/">{servico_nome}</a> › {cidade}
    </p>
    <h1>{h1}</h1>
    <p>{intro}</p>
    <div class="seo-cta-wrap">
      <a href="{root}#cotacao" class="btn-seo-primary">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 9H16M16 9L11 4M16 9L11 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Solicitar Cotação Gratuita
      </a>
    </div>
    <div class="seo-trust">
      <span class="seo-trust-item">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1L9 5.2L13.7 5.85L10.35 9.12L11.13 13.77L7 11.62L2.87 13.77L3.63 9.12L0.27 5.85L4.94 5.2L7 1Z" fill="currentColor"/></svg>
        100% Gratuito
      </span>
      <span class="seo-trust-item">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1L11 3V7C11 9.76 9.32 12.34 7 13C4.68 12.34 3 9.76 3 7V3L7 1Z" fill="currentColor"/></svg>
        Empresas Verificadas
      </span>
      <span class="seo-trust-item">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="7" r="5.5" stroke="currentColor" stroke-width="1.5"/><path d="M7 4V7L9 8.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
        Resposta em até 24h
      </span>
    </div>
  </section>

  <div class="seo-divider"></div>

  <!-- FAQ -->
  <section class="seo-faq-section">
    <h2>Perguntas Frequentes sobre {servico_nome} em {cidade}</h2>
    {faq_html}
  </section>

  <!-- Footer -->
  <footer class="seo-footer">
    <p>© {date.today().year} <a href="{root}">Cota Facilities</a> — Cotações de Facilities em {cidade} e região de São Paulo.</p>
  </footer>

</body>
</html>"""

# ── Gerador do Sitemap ─────────────────────────────────────────────────────────

def gerar_sitemap(urls):
    hoje = date.today().isoformat()
    itens = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{hoje}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>"
        for u in urls
    )
    # Adicionar index com prioridade maior
    index = f"  <url><loc>{BASE_URL}/</loc><lastmod>{hoje}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{index}
{itens}
</urlset>"""

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    total = 0
    urls  = []

    for intencao in INTENCOES:
        for servico_nome, servico_slug in SERVICOS:
            for cidade in CIDADES:
                cidade_slug = slugify(cidade)

                # Caminho: /intent/servico/cidade/index.html
                dirpath = os.path.join(intencao["slug"], servico_slug, cidade_slug)
                os.makedirs(dirpath, exist_ok=True)

                html = gerar_pagina(intencao, servico_nome, servico_slug, cidade, cidade_slug)
                filepath = os.path.join(dirpath, "index.html")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(html)

                urls.append(f"{BASE_URL}/{intencao['slug']}/{servico_slug}/{cidade_slug}/")
                total += 1

                if total % 100 == 0:
                    print(f"  {total} páginas geradas...")

    # Sitemap
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(gerar_sitemap(urls))

    print(f"\nConcluido!")
    print(f"  Paginas geradas : {total}")
    print(f"  Sitemap         : sitemap.xml ({len(urls)+1} URLs)")
    print(f"  Estrutura       : /{INTENCOES[0]['slug']}/{SERVICOS[0][1]}/{slugify(CIDADES[0])}/")

if __name__ == "__main__":
    main()
