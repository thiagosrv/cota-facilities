#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publica N páginas SEO da fila (seo-queue.json)
Uso: python publish_pages.py --count 10
Chamado pelo GitHub Actions diariamente.
"""
import os, json, argparse
from datetime import date

BASE_URL = "https://cotafacilities.com.br"

# ── FAQ para intenção "como-contratar" ────────────────────────
FAQ_COMO_CONTRATAR = [
    ("Quais documentos exigir de uma empresa de {s} em {c}?",
     "Ao contratar {s} em {c}, exija: CNPJ ativo, Certidão Negativa de Débitos (CND Federal e Estadual), Certificado de Regularidade do FGTS (CRF), certidão trabalhista e, para segurança privada, autorização da Polícia Federal. Empresas cadastradas na Cota Facilities já passaram por essa validação."),
    ("Como funciona o processo de contratação de {s} em {c}?",
     "O processo de contratação de {s} em {c} envolve: (1) definir o escopo do serviço, (2) solicitar cotações de múltiplos fornecedores em {c}, (3) comparar propostas técnicas e financeiras, (4) verificar documentação da empresa escolhida e (5) formalizar em contrato com SLA definido. A Cota Facilities facilita as etapas 2 e 3."),
    ("O que deve constar no contrato de {s} em {c}?",
     "Um contrato sólido de {s} em {c} deve incluir: descrição detalhada dos serviços, número de profissionais e carga horária, política de substituição em faltas e férias, prazo de vigência, cláusula de reajuste (INPC/IPCA), responsabilidades trabalhistas e multas por descumprimento. Solicite sempre que a empresa de {c} apresente minuta antes de assinar."),
    ("Como verificar se uma empresa de {s} em {c} é idônea?",
     "Para verificar a idoneidade de um fornecedor de {s} em {c}: consulte o CNPJ na Receita Federal, verifique reclamações no Procon e Reclame Aqui, peça referências de outros clientes em {c}, confira se a empresa possui CNAE compatível com o serviço e, no caso de segurança, consulte o cadastro na Polícia Federal."),
    ("Qual o prazo médio de contrato para {s} em {c}?",
     "Contratos de {s} em {c} geralmente têm prazo mínimo de 12 meses, com renovação automática. Algumas empresas de {c} aceitam contratos de 6 meses para novos clientes. Contratos mais longos (24-36 meses) costumam ter desconto no valor mensal. Negocie sempre com mais de um fornecedor em {c} para conseguir melhores condições."),
    ("Quais cuidados ter ao renovar o contrato de {s} em {c}?",
     "Na renovação do contrato de {s} em {c}, verifique: o índice de reajuste aplicado (compare com INPC/IPCA do período), se houve mudança no quadro de profissionais, atualizações na convenção coletiva da categoria em {c} e se o nível de serviço (SLA) continua adequado às suas necessidades. Solicitar novas cotações em {c} antes de renovar garante poder de negociação."),
]

def gerar_faq_html(s, c):
    itens = []
    for q_t, a_t in FAQ_COMO_CONTRATAR:
        q = q_t.format(s=s, c=c)
        a = a_t.format(s=s, c=c)
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

def gerar_faq_schema(s, c):
    items = [{"@type":"Question","name":q_t.format(s=s,c=c),
              "acceptedAnswer":{"@type":"Answer","text":a_t.format(s=s,c=c)}}
             for q_t, a_t in FAQ_COMO_CONTRATAR]
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage",
                       "mainEntity":items}, ensure_ascii=False, indent=2)

def gerar_breadcrumb_schema(intent_slug, intent_label, s_nome, s_slug, cidade, c_slug):
    return json.dumps({
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Início","item":BASE_URL},
            {"@type":"ListItem","position":2,"name":intent_label,
             "item":f"{BASE_URL}/{intent_slug}/"},
            {"@type":"ListItem","position":3,"name":s_nome,
             "item":f"{BASE_URL}/{intent_slug}/{s_slug}/"},
            {"@type":"ListItem","position":4,"name":cidade,
             "item":f"{BASE_URL}/{intent_slug}/{s_slug}/{c_slug}/"},
        ]
    }, ensure_ascii=False, indent=2)

def gerar_html(page):
    s     = page["servico"]
    s_sl  = page["servico_slug"]
    c     = page["cidade"]
    c_sl  = page["cidade_slug"]
    isl   = page["intent_slug"]

    h1    = page["intent_h1"].format(s=s, c=c)
    title = page["intent_title"].format(s=s, c=c)
    desc  = page["intent_desc"].format(s=s, c=c)
    intro = page["intent_intro"].format(s=s, c=c)

    faq_html = gerar_faq_html(s, c)
    faq_sch  = gerar_faq_schema(s, c)
    bc_sch   = gerar_breadcrumb_schema(isl, "Como Contratar", s, s_sl, c, c_sl)
    canon    = f"{BASE_URL}/{isl}/{s_sl}/{c_sl}/"
    root     = "../../../"
    year     = date.today().year

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canon}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:type" content="website">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
  <script type="application/ld+json">{faq_sch}</script>
  <script type="application/ld+json">{bc_sch}</script>
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#0F172A;color:#E2E8F0;font-family:'Outfit',sans-serif;line-height:1.6}}
    .seo-nav{{position:sticky;top:0;z-index:100;background:rgba(15,23,42,.92);backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,255,255,.07);padding:14px 24px;display:flex;align-items:center;justify-content:space-between}}
    .seo-nav img{{height:34px}}
    .seo-nav-cta{{background:linear-gradient(90deg,#7C3AED,#1B3A8C);color:#fff;font-weight:700;font-size:14px;padding:9px 20px;border-radius:999px;text-decoration:none}}
    .seo-hero{{max-width:820px;margin:0 auto;padding:72px 24px 56px;text-align:center}}
    .seo-breadcrumb{{font-size:12px;color:#64748B;margin-bottom:24px}}
    .seo-breadcrumb a{{color:#7B2FBE;text-decoration:none}}
    .seo-hero h1{{font-size:clamp(28px,4.5vw,52px);font-weight:700;line-height:1.15;color:#fff;letter-spacing:-.02em;margin-bottom:20px}}
    .seo-hero p{{font-size:clamp(15px,2vw,18px);color:#94A3B8;max-width:600px;margin:0 auto 36px;line-height:1.7}}
    .seo-hero p strong{{color:#fff}}
    .btn-seo-primary{{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(90deg,#84CC16,#65A30D);color:#0F172A;font-weight:700;font-size:16px;padding:15px 32px;border-radius:999px;text-decoration:none}}
    .seo-trust{{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;margin-top:20px}}
    .seo-trust-item{{display:flex;align-items:center;gap:6px;font-size:12px;color:#64748B}}
    .seo-trust-item svg{{color:#84CC16}}
    .seo-divider{{height:1px;background:linear-gradient(90deg,transparent,rgba(123,47,190,.3),transparent);margin:0 24px 64px}}
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
  </style>
</head>
<body>
  <nav class="seo-nav">
    <a href="{root}"><img src="{root}cota.png" alt="Cota Facilities"></a>
    <a href="{root}#cotacao" class="seo-nav-cta">Solicitar Cotação Gratuita →</a>
  </nav>

  <section class="seo-hero">
    <p class="seo-breadcrumb">
      <a href="{root}">Início</a> › <a href="{root}{isl}/">Como Contratar</a> › <a href="{root}{isl}/{s_sl}/">{s}</a> › {c}
    </p>
    <h1>{h1}</h1>
    <p>{intro}</p>
    <a href="{root}#cotacao" class="btn-seo-primary">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 9H16M16 9L11 4M16 9L11 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      Solicitar Cotação Gratuita
    </a>
    <div class="seo-trust">
      <span class="seo-trust-item"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1L9 5.2L13.7 5.85L10.35 9.12L11.13 13.77L7 11.62L2.87 13.77L3.63 9.12L0.27 5.85L4.94 5.2L7 1Z" fill="currentColor"/></svg>100% Gratuito</span>
      <span class="seo-trust-item"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1L11 3V7C11 9.76 9.32 12.34 7 13C4.68 12.34 3 9.76 3 7V3L7 1Z" fill="currentColor"/></svg>Empresas Verificadas</span>
      <span class="seo-trust-item"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="7" r="5.5" stroke="currentColor" stroke-width="1.5"/><path d="M7 4V7L9 8.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>Resposta em até 24h</span>
    </div>
  </section>

  <div class="seo-divider"></div>

  <section class="seo-faq-section">
    <h2>Guia: Como Contratar {s} em {c}</h2>
    {faq_html}
  </section>

  <footer class="seo-footer">
    <p>© {year} <a href="{root}">Cota Facilities</a> — Guia de contratação de {s} em {c}, SP.</p>
  </footer>
</body>
</html>"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()

    with open("seo-queue.json", encoding="utf-8") as f:
        queue = json.load(f)

    start = queue["next_index"]
    end   = min(start + args.count, queue["total"])

    if start >= queue["total"]:
        print("Fila concluida! Todas as paginas ja foram publicadas.")
        return

    publicadas = 0
    for i in range(start, end):
        page = queue["pages"][i]
        dirpath = os.path.join(page["intent_slug"], page["servico_slug"], page["cidade_slug"])
        os.makedirs(dirpath, exist_ok=True)

        html = gerar_html(page)
        with open(os.path.join(dirpath, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        publicadas += 1

    # Atualizar fila
    queue["next_index"] = end
    with open("seo-queue.json", "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

    restantes = queue["total"] - end
    print(f"Publicadas: {publicadas} paginas ({start+1} a {end})")
    print(f"Restantes : {restantes} de {queue['total']}")
    print(f"Progresso : {end}/{queue['total']} ({int(end/queue['total']*100)}%)")

if __name__ == "__main__":
    main()
