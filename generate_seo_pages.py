#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Páginas de SEO Programático, Blog e Sitemap para Cota Facilities
Suporta múltiplos propósitos (10 intenções de busca) para as 8 cidades principais
e página genérica para as outras 22 cidades.
"""

import os
import re
import sys
import io
import unicodedata
from datetime import datetime

# Force UTF-8 output to avoid Windows console encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Definir as 8 cidades principais (geram 10 landing pages cada)
cidades_principais = [
    "Campinas", "Americana", "Santa Bárbara d'Oeste", "Piracicaba", "Sumaré", 
    "Hortolândia", "Indaiatuba", "Nova Odessa"
]

# Definir as 22 cidades secundárias (geram 1 página genérica cada)
cidades_secundarias = [
    "Paulínia", "Valinhos", "Vinhedo", "Monte Mor", "Itatiba", "Jaguariúna", 
    "Holambra", "Pedreira", "Santo Antônio de Posse", "Cosmópolis", 
    "Artur Nogueira", "Engenheiro Coelho", "Limeira", "Iracemápolis", 
    "Elias Fausto", "Capivari", "Rafard", "Louveira", "Jundiaí", 
    "Morungaba", "Tietê", "Mombuca"
]

# Unir todas as cidades para sitemap e consistência
todas_cidades = cidades_principais + cidades_secundarias

# Variações de título (H1) para as cidades secundárias (rodízio)
title_variations = [
    "Cotações de Facilities em {cidade}",
    "Cotação de Facilities em {cidade}",
    "Orçamento de Facilities em {cidade}",
    "Cotação de Serviços em {cidade}",
    "Cotações de Serviços em {cidade}",
    "Empresas de Facilities em {cidade}",
    "Terceirização de Serviços em {cidade}",
    "Contratar Facilities em {cidade}"
]

# Variações de subtítulo para rodízio nas secundárias
sub_variations = [
    "Sem ligações. 100% gratuito.",
    "Economize tempo. Sem burocracia.",
    "Cotações rápidas. 100% grátis.",
    "Compare propostas. Economize hoje.",
    "Empresas avaliadas. Propostas em 24h.",
    "Simples, rápido e 100% gratuito.",
    "Sem chateação. Receba propostas grátis.",
    "Poupe tempo e reduza custos.",
    "As melhores empresas competem pelo seu contrato.",
    "Solicite online. Resposta em 24 horas."
]

# Estruturação das 10 Intenções de Busca para as Cidades Principais
intents_data = [
    {
        "id": "geral",
        "slug": "",
        "service": None,
        "keyword": "Serviços de Facilities",
        "title": "Cotações de Facilities em {cidade} | Cota Facilities",
        "desc": "Solicite cotações de portaria terceirizada, segurança patrimonial, controle de acesso e limpeza em {cidade}. Receba propostas de empresas verificadas gratuitas em 24h.",
        "h1_line1": "Cotações de Facilities",
        "h1_line2": "em {cidade}",
        "h1_line3": "Sem Ligações. Sem Burocracia.",
        "faq": [
            {"q": "Como funciona a Cota Facilities em {cidade}?", "a": "Você seleciona o serviço desejado, informa sua cidade e quantas cotações deseja receber. Em até 24 horas, empresas verificadas de {cidade} e região entram em contato com propostas comerciais completas."},
            {"q": "A plataforma cobra alguma taxa do comprador?", "a": "Não, o serviço é 100% gratuito para quem solicita as cotações. Nosso modelo é remunerado pelas prestadoras de serviço credenciadas na plataforma."},
            {"q": "As empresas cadastradas em {cidade} são seguras?", "a": "Sim. Realizamos uma checagem rigorosa de regularidade fiscal, licenças municipais e federais antes de homologar os prestadores na plataforma."}
        ]
    },
    {
        "id": "portaria",
        "slug": "servico-de-portaria",
        "service": "portaria",
        "keyword": "Serviço de Portaria",
        "title": "Serviço de Portaria em {cidade} | Portaria Terceirizada",
        "desc": "Precisa contratar serviço de portaria em {cidade}? Receba propostas comerciais de empresas de portaria e recepção terceirizada verificadas em até 24h. 100% grátis.",
        "h1_line1": "Serviço de Portaria",
        "h1_line2": "em {cidade}",
        "h1_line3": "Terceirização de Porteiros e Recepcionistas.",
        "faq": [
            {"q": "Quais as vantagens de terceirizar o serviço de portaria em {cidade}?", "a": "A terceirização elimina a gestão direta de RH, custos com rescisões e passivos trabalhistas. Além disso, garante cobertura imediata em faltas, férias ou licenças sem custo extra para o contratante."},
            {"q": "Como é garantido o treinamento dos porteiros em {cidade}?", "a": "As empresas parceiras em {cidade} fornecem treinamentos de controle de acesso, postura profissional e atendimento ao cliente de forma constante e periódica."},
            {"q": "Os porteiros terceirizados em {cidade} trabalham uniformizados?", "a": "Sim, todos os profissionais se apresentam devidamente uniformizados, identificados por crachá e equipados com os EPIs exigidos por lei."}
        ]
    },
    {
        "id": "controle_acesso",
        "slug": "portaria-e-controle-de-acesso",
        "service": "controle-acesso",
        "keyword": "Controle de Acesso",
        "title": "Contratar Portaria e Controle de Acesso em {cidade}",
        "desc": "Encontre as melhores soluções de controle de acesso e portaria terceirizada em {cidade}. Receba orçamentos de sistemas eletrônicos e portaria física ou virtual.",
        "h1_line1": "Portaria & Controle de Acesso",
        "h1_line2": "em {cidade}",
        "h1_line3": "Segurança e tecnologia integradas.",
        "faq": [
            {"q": "Como funciona o controle de acesso integrado à portaria em {cidade}?", "a": "Ele combina sistemas de hardware (catracas, biometria, reconhecimento facial) com a supervisão de porteiros ou operadores de acesso, garantindo que apenas pessoas autorizadas entrem no imóvel."},
            {"q": "O que é portaria virtual e quando contratar em {cidade}?", "a": "A portaria virtual ou remota monitora os acessos à distância a partir de uma central blindada 24h. É ideal para condomínios residenciais que buscam reduzir o custo da taxa condominial em até 50%."},
            {"q": "Os equipamentos de controle de acesso estão inclusos na cotação em {cidade}?", "a": "Isso depende da modalidade de contrato. A maioria das prestadoras em {cidade} oferece opções de comodato (locação inclusa no serviço) ou venda direta dos equipamentos de controle de acesso."}
        ]
    },
    {
        "id": "seguranca_patrimonial",
        "slug": "seguranca-patrimonial",
        "service": "seguranca",
        "keyword": "Segurança Patrimonial",
        "title": "Segurança Patrimonial em {cidade} | Cotações Gratuitas",
        "desc": "Proteja sua empresa com serviços de segurança patrimonial corporativa em {cidade}. Receba propostas comerciais de empresas credenciadas e regularizadas.",
        "h1_line1": "Segurança Patrimonial",
        "h1_line2": "em {cidade}",
        "h1_line3": "Proteção ativa para empresas e condomínios.",
        "faq": [
            {"q": "O que abrange o serviço de segurança patrimonial em {cidade}?", "a": "Abrange desde o planejamento de segurança (análise de vulnerabilidades do local) até a presença física de vigilantes, rondas táticas motorizadas e monitoramento tecnológico 24h."},
            {"q": "Como contratar uma empresa de segurança patrimonial regularizada em {cidade}?", "a": "É fundamental verificar a regularidade da prestadora. Nossa plataforma pré-avalia todos os prestadores de {cidade}, garantindo que possuem licença municipal e idoneidade fiscal comprovada."},
            {"q": "Qual o prazo médio para iniciar o posto de vigilância em {cidade}?", "a": "Após a assinatura do contrato comercial, o prazo médio de implantação física do posto com profissionais treinados em {cidade} varia de 5 a 15 dias úteis."}
        ]
    },
    {
        "id": "seguranca_privada",
        "slug": "seguranca-privada",
        "service": "seguranca",
        "keyword": "Segurança Privada",
        "title": "Segurança Privada em {cidade} | Vigilante e Escolta",
        "desc": "Contrate segurança privada autorizada pela Polícia Federal em {cidade}. Receba orçamentos de segurança patrimonial, vigilante armado e ronda motorizada.",
        "h1_line1": "Segurança Privada",
        "h1_line2": "em {cidade}",
        "h1_line3": "Vigilância em conformidade com a Polícia Federal.",
        "faq": [
            {"q": "Qual a diferença entre porteiro e vigilante em {cidade}?", "a": "O vigilante passa por curso homologado pela Polícia Federal, tem formação específica para segurança ativa e pode trabalhar armado. O porteiro atua estritamente na recepção e controle administrativo de acesso."},
            {"q": "As empresas de segurança em {cidade} têm autorização da PF?", "a": "Sim. Conforme as normas nacionais, a segurança privada armada ou desarmada exige Autorização de Funcionamento expedida pela Polícia Federal. Nós filtramos e aprovamos apenas empresas regulares em {cidade}."},
            {"q": "Como funciona a ronda motorizada na região de {cidade}?", "a": "Um vigilante conduz veículo caracterizado (carro ou moto) e realiza rondas periódicas de segurança agendadas ou aleatórias no perímetro do imóvel, inspecionando portões e cercas."}
        ]
    },
    {
        "id": "porteiro_empresa",
        "slug": "porteiro-para-empresa",
        "service": "portaria",
        "keyword": "Porteiro para Empresa",
        "title": "Porteiro para Empresa em {cidade} | Recepção Terceirizada",
        "desc": "Terceirização de porteiro para empresa e recepção comercial em {cidade}. Contrate profissionais treinados para controle de fluxo e atendimento corporativo.",
        "h1_line1": "Porteiro para Empresa",
        "h1_line2": "em {cidade}",
        "h1_line3": "Controle administrativo e recepção corporativa.",
        "faq": [
            {"q": "O porteiro terceirizado corporativo em {cidade} pode auxiliar no controle de mercadorias?", "a": "Sim. Os porteiros focados em indústrias e empresas recebem treinamento específico para checagem de notas fiscais, liberação de caminhões e cadastro de motoristas na portaria."},
            {"q": "A empresa de portaria oferece substituição em caso de falta?", "a": "Sim, as prestadoras mantêm uma 'equipe de reserva' pronta para cobrir qualquer ausência de forma rápida, mantendo o posto operacional sem interrupções em {cidade}."},
            {"q": "É possível customizar o uniforme do porteiro com as cores da minha empresa?", "a": "Sim, muitas empresas de facilities de {cidade} aceitam personalizar uniformes corporativos para harmonizar com a identidade visual da sua marca."}
        ]
    },
    {
        "id": "portaria_limpeza",
        "slug": "servico-de-portaria-e-limpeza-terceirizado",
        "service": "portaria",
        "keyword": "Serviço de Portaria e Limpeza Terceirizado",
        "title": "Serviço de Portaria e Limpeza Terceirizado em {cidade}",
        "desc": "Combine serviço de portaria e limpeza terceirizado em {cidade}. Receba propostas de facilities integradas com maior custo-benefício e gestão unificada.",
        "h1_line1": "Portaria & Limpeza",
        "h1_line2": "em {cidade}",
        "h1_line3": "Gestão integrada de facilities com economia.",
        "faq": [
            {"q": "Por que contratar o combo de portaria e limpeza terceirizado em {cidade}?", "a": "A contratação integrada (multisserviços) gera economia de escala, reduzindo o custo total em até 20%. Além disso, você passa a lidar com apenas uma fatura e um gestor de contrato em {cidade}."},
            {"q": "Como funciona a supervisão dos colaboradores no local em {cidade}?", "a": "A empresa terceirizada disponibiliza um supervisor operacional que visita o posto periodicamente para checar o trabalho da limpeza e dos porteiros, resolvendo qualquer problema técnico."},
            {"q": "Os materiais de limpeza estão incluídos nesse tipo de contrato?", "a": "Fica a critério do cliente. A proposta comercial em {cidade} pode incluir apenas a mão de obra ou o escopo completo com maquinários e produtos profissionais inclusos."}
        ]
    },
    {
        "id": "limpeza_terceirizada",
        "slug": "limpeza-terceirizada",
        "service": "limpeza",
        "keyword": "Limpeza Terceirizada",
        "title": "Empresa de Limpeza Terceirizada em {cidade} | Orçamentos",
        "desc": "Economize com empresa de limpeza terceirizada em {cidade}. Compare cotações gratuitas de limpeza comercial, predial e conservação em geral.",
        "h1_line1": "Limpeza Terceirizada",
        "h1_line2": "em {cidade}",
        "h1_line3": "Conservação de condomínios e escritórios.",
        "faq": [
            {"q": "Qual o foco dos serviços de limpeza comercial em {cidade}?", "a": "Ele abrange a higienização de escritórios, recepções, sanitários, copas e áreas de circulação comum, mantendo o ambiente de trabalho limpo e produtivo em {cidade}."},
            {"q": "Os produtos de limpeza são fornecidos pela empresa contratada em {cidade}?", "a": "Geralmente sim. O contrato de limpeza predial ou corporativa inclui o fornecimento de produtos profissionais e equipamentos de proteção individual (EPIs)."},
            {"q": "A limpeza terceirizada realiza serviços em altura em {cidade}?", "a": "Sim. Algumas prestadoras em {cidade} possuem equipes especializadas e certificadas pela NR-35 para limpeza de fachadas e vidros em altura."}
        ]
    },
    {
        "id": "terceirizacao",
        "slug": "terceirizacao-de-servicos",
        "service": None,
        "keyword": "Terceirização de Serviços",
        "title": "Terceirização de Serviços em {cidade} | Empresas de Facilities",
        "desc": "Terceirização de serviços de facilities em {cidade}. Compare propostas de portaria, controle de acesso, limpeza e apoio operacional sem complicação.",
        "h1_line1": "Terceirização de Serviços",
        "h1_line2": "em {cidade}",
        "h1_line3": "Mão de obra qualificada e focada em resultados.",
        "faq": [
            {"q": "Quais cargos podem ser abrangidos pela terceirização de serviços em {cidade}?", "a": "Zeladores, porteiros, auxiliares de limpeza, recepcionistas, copeiras, motoristas, auxiliares administrativos e apoio em logística geral."},
            {"q": "Como funciona a fiscalização trabalhista na terceirização em {cidade}?", "a": "O tomador de serviços deve solicitar mensalmente à prestadora as guias de recolhimento de FGTS, INSS e folhas de pagamento para se resguardar juridicamente."},
            {"q": "É possível contratar serviços terceirizados temporários em {cidade}?", "a": "Sim, as empresas parceiras em {cidade} atendem demandas fixas ou sob regime de contrato temporário para eventos ou coberturas específicas de férias."}
        ]
    },
    {
        "id": "zelador",
        "slug": "zelador-terceirizado",
        "service": "manutencao",
        "keyword": "Zelador Terceirizado",
        "title": "Contratar Zelador Terceirizado em {cidade} | Cota Facilities",
        "desc": "Terceirização de zeladoria e pequenos reparos em {cidade}. Receba propostas de empresas de facilities qualificadas para condomínios e prédios comerciais.",
        "h1_line1": "Zelador Terceirizado",
        "h1_line2": "em {cidade}",
        "h1_line3": "Manutenção preventiva e conservação de edifícios.",
        "faq": [
            {"q": "Quais as principais responsabilidades de um zelador terceirizado em {cidade}?", "a": "Supervisão da limpeza diária, fiscalização do funcionamento das instalações (bombas, geradores), recebimento de prestadores externos e pequenos reparos elétricos ou hidráulicos."},
            {"q": "Qual a diferença entre zelador e auxiliar de serviços gerais?", "a": "O zelador gerencia o andamento do prédio e faz a manutenção técnica básica. O auxiliar de serviços gerais foca na limpeza física, conservação e organização de materiais em {cidade}."},
            {"q": "A empresa de facilities garante a substituição imediata do zelador?", "a": "Sim, em caso de falta, férias ou licença de qualquer natureza, um zelador substituto homologado é enviado imediatamente ao condomínio em {cidade}."}
        ]
    }
]

def slugify(value):
    """Converte o nome da cidade em um slug de URL amigável e limpo."""
    value = str(value)
    # Tratar Hortolândia -> hortolandia, Santa Bárbara D'Oeste -> santa-barbara-d-oeste
    value = value.replace("'", " ").replace("’", " ")
    # Normalizar Unicode para retirar acentos
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = value.lower()
    value = re.sub(r'[^\w\s-]', '', value)
    value = re.sub(r'[-\s]+', '-', value)
    return value.strip('-')

def adjust_assets_path(html_content, depth):
    """Ajusta os links de css, js e âncoras baseados no nível de aninhamento da pasta."""
    if depth == 0:
        return html_content
        
    prefix = "../" * depth
    
    # Substituir links css, js, imagens e vídeos
    adjusted = html_content
    adjusted = adjusted.replace('href="css/', f'href="{prefix}css/')
    adjusted = adjusted.replace('src="js/', f'src="{prefix}js/')
    adjusted = adjusted.replace('src="cota.png"', f'src="{prefix}cota.png"')
    adjusted = adjusted.replace('src="vdo.mp4"', f'src="{prefix}vdo.mp4"')
    adjusted = adjusted.replace('href="cotafacilities.jpg"', f'href="{prefix}cotafacilities.jpg"')
    adjusted = adjusted.replace('src="imagem.jpg"', f'src="{prefix}imagem.jpg"')
    
    # Ajustar links do navbar para irem para a home raiz com a âncora correta
    adjusted = adjusted.replace('href="#como-funciona"', f'href="{prefix}#como-funciona"')
    adjusted = adjusted.replace('href="#servicos"', f'href="{prefix}#servicos"')
    adjusted = adjusted.replace('href="#prestadores"', f'href="{prefix}#prestadores"')
    adjusted = adjusted.replace('href="#cotacao"', f'href="{prefix}#cotacao"')
    adjusted = adjusted.replace('href="#"', f'href="{prefix}"')
    
    # Também tratar o link da logo e blog no navbar para caminhos corretos
    adjusted = adjusted.replace('href="#navbar"', f'href="{prefix}#navbar"')
    
    return adjusted

def build_faq_markup(intent, cidade):
    """Gera o HTML estruturado do FAQ específico para a intenção e a cidade."""
    faq_items = []
    
    for item in intent["faq"]:
        q = item["q"].format(cidade=cidade)
        a = item["a"].format(cidade=cidade)
        
        faq_items.append(f"""
          <div class="faq-item reveal" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
            <button class="faq-question" itemprop="name" aria-expanded="false">
              {q}
              <svg class="faq-arrow" width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M4 7L9 12L14 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <div class="faq-answer" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
              <p itemprop="text">{a}</p>
            </div>
          </div>""")
          
    faq_str = "\n".join(faq_items)
    
    markup = f"""<section id="faq" class="section-faq" itemscope itemtype="https://schema.org/FAQPage">
    <div class="container">
      <div class="section-header reveal">
        <span class="section-tag">Dúvidas Frequentes</span>
        <h2>Perguntas Frequentes sobre {intent["keyword"]} em {cidade}</h2>
        <p>Tudo o que você precisa saber antes de contratar {intent["keyword"].lower()} na sua região</p>
      </div>

      <div class="faq-grid">
        <div class="faq-column">
          {faq_str}
        </div>
      </div>

      <div class="faq-cta reveal">
        <p>Ainda tem dúvidas? Nossa equipe está pronta para ajudar.</p>
        <a href="https://wa.me/5519999115496?text=Olá,%20tenho%20dúvidas%20sobre%20{intent["keyword"]}%20em%20{cidade}." target="_blank" rel="noopener" class="btn-primary">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M15.5 2.5C13.94 0.94 11.86 0 9 0C4.03 0 0 4.03 0 9C0 10.59 0.44 12.11 1.26 13.41L0 18L4.71 16.76C5.98 17.5 7.45 17.9 9 17.9C13.97 17.9 18 13.87 18 8.9C18 6.04 17.06 4.06 15.5 2.5Z" fill="white" fill-opacity="0.3"/><path d="M9.5 10.5L7 8L4.5 5.5" stroke="white" stroke-width="1.5" stroke-linecap="round"/></svg>
          Falar no WhatsApp
        </a>
      </div>
    </div>
  </section>"""
    
    return markup

def generate_city_pages():
    """Gera diretórios e arquivos index.html para cidades principais (10 intenções) e secundárias (1 genérica)."""
    print("Iniciando geracao de paginas de SEO Programatico...")
    
    # Ler index.html base da raiz
    with open("index.html", "r", encoding="utf-8") as f:
        template = f.read()
        
    generated_urls = []
    
    # 1. Geração para Cidades Principais (8 cidades x 10 páginas = 80 LPs)
    for cidade in cidades_principais:
        cidade_slug = slugify(cidade)
        
        for intent in intents_data:
            # Determinar diretório e nível (depth)
            if intent["slug"] == "":
                output_dir = cidade_slug
                depth = 1
                canonical = f"https://cotafacilities.com.br/{cidade_slug}/"
            else:
                output_dir = os.path.join(cidade_slug, intent["slug"])
                depth = 2
                canonical = f"https://cotafacilities.com.br/{cidade_slug}/{intent['slug']}/"
                
            os.makedirs(output_dir, exist_ok=True)
            
            custom_html = template
            
            # Injetar os scripts de pre-seleção no head
            preselect_script = f'\n  <script>window.PRESELECTED_CITY = "{cidade}";'
            if intent["service"]:
                preselect_script += f'\n  window.PRESELECTED_SERVICE = "{intent["service"]}";'
            preselect_script += '\n  </script>\n</head>'
            custom_html = custom_html.replace("</head>", preselect_script)
            
            # Formatar Título, Descrição e H1 para a cidade específica
            title_text = intent["title"].format(cidade=cidade)
            desc_text = intent["desc"].format(cidade=cidade)
            h1_l1 = intent["h1_line1"].format(cidade=cidade)
            h1_l2 = intent["h1_line2"].format(cidade=cidade)
            h1_l3 = intent["h1_line3"].format(cidade=cidade)
            
            # Substituir tags do cabeçalho
            custom_html = re.sub(r'<title>.*?</title>', f'<title>{title_text}</title>', custom_html)
            custom_html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc_text}">', custom_html)
            
            # OpenGraph e Twitter tags
            custom_html = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title_text}">', custom_html)
            custom_html = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{desc_text}">', custom_html)
            custom_html = re.sub(r'<meta name="twitter:title" content=".*?">', f'<meta name="twitter:title" content="{title_text}">', custom_html)
            custom_html = re.sub(r'<meta name="twitter:description" content=".*?">', f'<meta name="twitter:description" content="{desc_text}">', custom_html)
            
            # Substituir dados do Product Schema (SEO Stars)
            custom_html = custom_html.replace(
                '"name": "Cota Facilities — Cotações de Portaria, Segurança e Facilities em Minutos"',
                f'"name": "{title_text}"'
            )
            custom_html = custom_html.replace(
                '"description": "Solicite cotações de portaria terceirizada, segurança patrimonial, controle de acesso, limpeza terceirizada, vigilante e mais. Conectamos sua empresa às melhores prestadoras verificadas. 100% gratuito e sem burocracia."',
                f'"description": "{desc_text}"'
            )

            # Canonical link
            custom_html = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="{canonical}">', custom_html)
            
            # Ajustar links de ativos e âncoras baseados no depth
            custom_html = adjust_assets_path(custom_html, depth)
            
            # Mudar H1 Hero
            h1_regex = r'<h1 class="hero-headline">.*?</h1>'
            new_h1_markup = f"""<h1 class="hero-headline">
              <span class="line-wrap"><span class="hero-word">{h1_l1}</span></span>
              <span class="line-wrap"><span class="hero-word hero-word--accent">{h1_l2}</span></span>
              <span class="line-wrap"><span class="hero-word hero-word--light">{h1_l3}</span></span>
            </h1>"""
            custom_html = re.sub(h1_regex, new_h1_markup, custom_html, flags=re.DOTALL)
            
            # Ajustar textos de branding do hero
            custom_html = custom_html.replace(
                "Conectamos sua empresa às melhores prestadoras certificadas de São Paulo.",
                f"Conectamos sua empresa às melhores prestadoras certificadas de {cidade} e região."
            )
            custom_html = re.sub(
                r'<span>500\+ empresas verificadas na plataforma</span>',
                f'<span>Empresas de facilities verificadas em {cidade}</span>',
                custom_html
            )
            
            # Substituir o FAQ pelo FAQ customizado
            faq_markup = build_faq_markup(intent, cidade)
            custom_html = re.sub(r'<section id="faq" class="section-faq".*?</section>', faq_markup, custom_html, flags=re.DOTALL)
            
            # Pré-selecionar a cidade no dropdown por padrão na página gerada
            target_option = f'<option value="{cidade}">'
            selected_option = f'<option value="{cidade}" selected>'
            custom_html = custom_html.replace(target_option, selected_option)
            
            # Salvar index.html localizado
            output_file = os.path.join(output_dir, "index.html")
            with open(output_file, "w", encoding="utf-8") as f_out:
                f_out.write(custom_html)
                
            generated_urls.append(canonical)
            
        print(f"   [CONCLUÍDO] 10 variações geradas para {cidade} -> /{cidade_slug}/")
        
    # 2. Geração para Cidades Secundárias (22 cidades x 1 página = 22 LPs)
    for idx, cidade in enumerate(cidades_secundarias):
        cidade_slug = slugify(cidade)
        output_dir = cidade_slug
        depth = 1
        canonical = f"https://cotafacilities.com.br/{cidade_slug}/"
        
        os.makedirs(output_dir, exist_ok=True)
        
        custom_html = template
        
        # Injetar window.PRESELECTED_CITY no head
        preselect_script = f'\n  <script>window.PRESELECTED_CITY = "{cidade}";</script>\n</head>'
        custom_html = custom_html.replace("</head>", preselect_script)
        
        # Escolher uma variação de título e subtítulo baseadas no rodízio
        variation_base = title_variations[idx % len(title_variations)]
        cidade_title = variation_base.format(cidade=cidade)
        sub_headline = sub_variations[idx % len(sub_variations)]
        
        custom_html = re.sub(r'<title>.*?</title>', f'<title>{cidade_title} — Cota Facilities</title>', custom_html)
        custom_html = re.sub(
            r'<meta name="description" content=".*?">',
            f'<meta name="description" content="Solicite cotações de portaria terceirizada, segurança patrimonial, controle de acesso e limpeza em {cidade}. Receba propostas de empresas verificadas gratuitas em 24h.">',
            custom_html
        )
        
        custom_html = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{cidade_title} — Cota Facilities">', custom_html)
        custom_html = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="Solicite cotações de portaria terceirizada, segurança patrimonial e limpeza em {cidade}. Empresas verificadas, propostas em 24h. 100% grátis.">', custom_html)
        custom_html = re.sub(r'<meta name="twitter:title" content=".*?">', f'<meta name="twitter:title" content="{cidade_title} — Cota Facilities">', custom_html)
        custom_html = re.sub(r'<meta name="twitter:description" content=".*?">', f'<meta name="twitter:description" content="Portaria, segurança, limpeza e mais em {cidade}. Receba até 10 propostas em 24h. Grátis.">', custom_html)
        
        # Substituir dados do Product Schema (SEO Stars)
        custom_html = custom_html.replace(
            '"name": "Cota Facilities — Cotações de Portaria, Segurança e Facilities em Minutos"',
            f'"name": "{cidade_title} — Cota Facilities"'
        )
        custom_html = custom_html.replace(
            '"description": "Solicite cotações de portaria terceirizada, segurança patrimonial, controle de acesso, limpeza terceirizada, vigilante e mais. Conectamos sua empresa às melhores prestadoras verificadas. 100% gratuito e sem burocracia."',
            f'"description": "Solicite cotações de portaria terceirizada, segurança patrimonial, controle de acesso e limpeza em {cidade}. Receba propostas de empresas verificadas gratuitas em 24h."'
        )


        custom_html = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="{canonical}">', custom_html)
        
        # Ajustar caminhos de ativos (depth = 1)
        custom_html = adjust_assets_path(custom_html, depth)
        
        # Mudar H1 Hero
        h1_regex = r'<h1 class="hero-headline">.*?</h1>'
        new_h1_markup = f"""<h1 class="hero-headline">
          <span class="line-wrap"><span class="hero-word hero-word--accent">{cidade_title}</span></span>
          <span class="line-wrap"><span class="hero-word hero-word--light">{sub_headline}</span></span>
        </h1>"""
        custom_html = re.sub(h1_regex, new_h1_markup, custom_html, flags=re.DOTALL)
        
        # Ajustar textos de branding do hero
        custom_html = custom_html.replace(
            "Conectamos sua empresa às melhores prestadoras certificadas de São Paulo.",
            f"Conectamos sua empresa às melhores prestadoras certificadas de {cidade} e região."
        )
        custom_html = re.sub(
            r'<span>500\+ empresas verificadas na plataforma</span>',
            f'<span>Empresas verificadas e certificadas em {cidade}</span>',
            custom_html
        )
        
        # Pré-selecionar a cidade no dropdown por padrão na página gerada
        target_option = f'<option value="{cidade}">'
        selected_option = f'<option value="{cidade}" selected>'
        custom_html = custom_html.replace(target_option, selected_option)
        
        output_file = os.path.join(output_dir, "index.html")
        with open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write(custom_html)
            
        generated_urls.append(canonical)
        print(f"   [GERADO] {cidade_title} -> /{cidade_slug}/index.html")
        
    return generated_urls

def generate_blog():
    """Gera a estrutura e páginas do blog para autoridade de domínio."""
    print("Gerando estrutura do Blog...")
    os.makedirs("blog", exist_ok=True)
    os.makedirs(os.path.join("blog", "artigos"), exist_ok=True)
    
    # 1. Escrever o Blog Index (Lista de artigos)
    blog_index_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog Cota Facilities — Artigos sobre Portaria, Limpeza e Segurança</title>
  <meta name="description" content="Dicas, guias completos e artigos para ajudar seu condomínio ou empresa a contratar e otimizar serviços terceirizados de facilities e portaria.">
  <link rel="canonical" href="https://cotafacilities.com.br/blog/">
  <link rel="icon" type="image/jpeg" href="../cotafacilities.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/main.css">
  <link rel="stylesheet" href="../css/layout.css">
  <link rel="stylesheet" href="../css/components.css">
  <link rel="stylesheet" href="../css/animations.css">
  <style>
    body { background-color: var(--color-navy); }
    .blog-hero {
      padding: var(--space-24) 0 var(--space-12);
      text-align: center;
      position: relative;
    }
    .blog-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: var(--space-6);
      margin-bottom: var(--space-24);
    }
    .blog-card {
      background: rgba(30, 41, 59, 0.45);
      backdrop-filter: blur(20px) saturate(180%);
      -webkit-backdrop-filter: blur(20px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: var(--radius-xl);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 100%;
      transition: all 0.3s ease;
    }
    .blog-card:hover {
      transform: translateY(-6px);
      border-color: var(--color-purple);
      box-shadow: 0 16px 40px rgba(0,0,0,0.45);
    }
    .blog-card-img {
      height: 180px;
      background: linear-gradient(135deg, var(--color-royal) 0%, var(--color-purple) 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 40px;
    }
    .blog-card-content {
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      flex: 1;
    }
    .blog-tag {
      font-size: 10px;
      font-weight: 700;
      color: var(--color-lime);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .blog-card h3 {
      font-size: 18px;
      color: var(--color-white);
      line-height: 1.3;
      margin-bottom: 0;
    }
    .blog-card p {
      font-size: 14px;
      line-height: 1.6;
      color: var(--color-muted);
      margin-bottom: 0;
    }
    .blog-card-footer {
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      margin-top: auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: rgba(255,255,255,0.4);
    }
    .blog-readmore {
      color: var(--color-lime);
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .blog-readmore:hover { text-decoration: underline; }
    @media (max-width: 900px) {
      .blog-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
      .blog-grid { grid-template-columns: 1fr; }
    }
  </style>
  <!-- JSON-LD: Product (AggregateRating for Google stars) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "Blog Cota Facilities — Artigos sobre Portaria, Limpeza e Segurança",
    "image": "https://cotafacilities.com.br/cota.png",
    "description": "Dicas, guias completos e artigos para ajudar seu condomínio ou empresa a contratar e otimizar serviços terceirizados de facilities e portaria.",
    "brand": {
      "@type": "Brand",
      "name": "Cota Facilities"
    },
    "offers": {
      "@type": "AggregateOffer",
      "priceCurrency": "BRL",
      "lowPrice": "0",
      "highPrice": "0",
      "offerCount": "10"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "5.0",
      "bestRating": "5",
      "worstRating": "1",
      "ratingCount": "1829"
    }
  }
  </script>
</head>
<body>
  <!-- Navbar -->
  <nav id="navbar" class="navbar scrolled">
    <div class="container navbar-inner">
      <a href="../" class="navbar-logo">
        <img src="../cota.png" alt="Cota Facilities" height="38">
      </a>
      <div class="navbar-links">
        <a href="../#como-funciona" class="nav-link">Como Funciona</a>
        <a href="../#servicos" class="nav-link">Serviços</a>
        <a href="./" class="nav-link active">Blog</a>
      </div>
      <a href="../#cotacao" class="btn-nav">Solicitar Cotações</a>
    </div>
  </nav>

  <!-- Hero Section -->
  <section class="blog-hero">
    <div class="container">
      <span class="section-tag">Conhecimento e Inteligência</span>
      <h1>Blog Cota Facilities</h1>
      <p style="font-size: 18px; max-width: 600px; margin-inline: auto; margin-top: 12px;">Dicas exclusivas, guias de contratação e boas práticas para gestão de portaria, limpeza e segurança corporativa.</p>
    </div>
  </section>

  <!-- Lista de Artigos -->
  <main class="container">
    <div class="blog-grid">
      <!-- Artigo 1 -->
      <article class="blog-card">
        <div class="blog-card-img">💼</div>
        <div class="blog-card-content">
          <span class="blog-tag">Portaria Terceirizada</span>
          <h3>Terceirização de Portaria: Como Economizar no Condomínio</h3>
          <p>Descubra como a terceirização de porteiros pode reduzir custos trabalhistas e aumentar a segurança do seu prédio em até 30%.</p>
          <div class="blog-card-footer">
            <span>Há 2 dias · 5 min de leitura</span>
            <a href="artigos/terceirizacao-de-portaria-como-economizar.html" class="blog-readmore">Ler mais →</a>
          </div>
        </div>
      </article>

      <!-- Artigo 2 -->
      <article class="blog-card">
        <div class="blog-card-img">🛡️</div>
        <div class="blog-card-content">
          <span class="blog-tag">Segurança Patrimonial</span>
          <h3>Segurança Patrimonial: O Guia Completo para Empresas</h3>
          <p>Entenda os pilares da segurança patrimonial corporativa, a diferença entre porteiro e vigilante e os cuidados ao contratar.</p>
          <div class="blog-card-footer">
            <span>Há 1 semana · 7 min de leitura</span>
            <a href="artigos/guia-seguranca-patrimonial-condominios.html" class="blog-readmore">Ler mais →</a>
          </div>
        </div>
      </article>

      <!-- Artigo 3 -->
      <article class="blog-card">
        <div class="blog-card-img">🧹</div>
        <div class="blog-card-content">
          <span class="blog-tag">Gestão de Facilities</span>
          <h3>Facilities Management: Como Reduzir Custos Operacionais</h3>
          <p>Entenda como integrar serviços terceirizados (limpeza, manutenção, controle de acesso) otimiza a gestão da sua empresa.</p>
          <div class="blog-card-footer">
            <span>Há 2 semanas · 6 min de leitura</span>
            <a href="artigos/facilities-management-reduzir-custos.html" class="blog-readmore">Ler mais →</a>
          </div>
        </div>
      </article>
    </div>
  </main>
</body>
</html>"""
    
    with open(os.path.join("blog", "index.html"), "w", encoding="utf-8") as f_blog:
      f_blog.write(blog_index_html)
    print("   [GERADO] /blog/index.html")

    # 2. Escrever os artigos de SEO
    artigos_data = [
        {
            "slug": "terceirizacao-de-portaria-como-economizar",
            "tag": "Portaria Terceirizada",
            "title": "Terceirização de Portaria: Como Economizar no Condomínio",
            "desc": "Descubra como a terceirização de portaria reduz os custos operacionais do condomínio, melhora a segurança e livra o síndico de burocracias.",
            "content": """
            <h2>A Busca por Economia na Gestão Condominial</h2>
            <p>Gerenciar as finanças de um condomínio é um dos maiores desafios de qualquer síndico ou administradora. Com a folha de pagamento e encargos trabalhistas correspondendo a até 60% da taxa condominial de um edifício, otimizar esses custos torna-se urgente. É nesse cenário que a <strong>terceirização de portaria</strong> desponta como uma das soluções mais eficientes para reduzir despesas de forma imediata.</p>
            
            <h2>Como a Terceirização Gera Economia Real?</h2>
            <p>Ao contratar uma empresa terceirizada especializada em portaria e recepção, o condomínio elimina gastos imprevisíveis e custos administrativos elevados:</p>
            <ul>
              <li><strong>Zero Passivos Trabalhistas Diretos:</strong> A prestadora assume todas as obrigações trabalhistas, recolhimento de impostos e potenciais rescisões ou processos na justiça do trabalho.</li>
              <li><strong>Substituições sem Custo Extra:</strong> Faltas, atrasos, férias e licenças médicas são cobertas pela empresa de facilities imediatamente, fornecendo cobertura 24h sem gerar custos adicionais de horas extras.</li>
              <li><strong>Redução de Gastos com Uniformes e EPIs:</strong> Equipamentos e vestuário de trabalho são fornecidos e geridos integralmente pela prestadora.</li>
            </ul>

            <h2>O Ganho Adicional em Segurança e Profissionalismo</h2>
            <p>Porteiros próprios geralmente não recebem treinamento preventivo e operacional periódico. As empresas parceiras de facilities fornecem colaboradores qualificados e treinados para agir sob protocolos estritos de controle de entrada e saída. O controle de acesso é executado com rigor, reduzindo a vulnerabilidade a invasões.</p>

            <h2>Comparando Preços de Portaria</h2>
            <p>O melhor caminho para obter a melhor taxa com qualidade é a cotação competitiva. Com a Cota Facilities, você pode solicitar cotações de empresas de portaria e facilities verificadas e legalizadas em minutos, comparando propostas sem compromisso e sem burocracia.</p>
            """
        },
        {
            "slug": "guia-seguranca-patrimonial-condominios",
            "tag": "Segurança Patrimonial",
            "title": "Segurança Patrimonial: O Guia Completo para Empresas",
            "desc": "Entenda os pilares da segurança patrimonial privada corporativa, as obrigações legais de empresas de segurança e a diferença entre porteiro e vigilante.",
            "content": """
            <h2>O Papel Estratégico da Segurança Patrimonial</h2>
            <p>Proteger o ativo humano, físico e digital é prioridade para qualquer negócio moderno. A <strong>segurança patrimonial</strong> deixou de ser vista como um custo operacional simples para se tornar um fator estratégico de continuidade dos negócios. Empresas e condomínios que investem em segurança mitigam riscos financeiros gigantescos gerados por roubos, fraudes e depredações.</p>
            
            <h2>Vigilante vs. Porteiro: Qual a Diferença?</h2>
            <p>Uma dúvida muito comum entre gestores e síndicos é a distinção legal das duas funções:</p>
            <ul>
              <li><strong>Porteiro:</strong> Atua no controle de fluxo, recepção, triagem de correspondências e liberação de visitantes autorizados. Não tem prerrogativa e treinamento de segurança física ativa ou policiamento.</li>
              <li><strong>Vigilante:</strong> Profissional regulamentado por lei federal. Passa por curso de formação de segurança em escola registrada na Polícia Federal, reciclagem bienal, e tem porte de arma de serviço se contratado nessa modalidade. O foco do vigilante é a defesa proativa e neutralização de ameaças diretas ao patrimônio.</li>
            </ul>

            <h2>Cuidados Jurídicos essenciais ao Contratar Segurança</h2>
            <p>A segurança privada no Brasil é severamente regulamentada pela Polícia Federal. Contratar empresas clandestinas ("seguranças informais" ou "bicos") acarreta séria corresponsabilidade jurídica, civil e penal em casos de sinistros. A empresa contratada precisa obrigatoriamente possuir:</p>
            <ul>
              <li>Autorização de funcionamento emitida pela Polícia Federal.</li>
              <li>Certidão de Regularidade perante a Previdência Social.</li>
              <li>Vigilantes devidamente registrados com a CNV (Carteira Nacional de Vigilante) ativa.</li>
            </ul>

            <h2>Solicite Cotações com Total Segurança</h2>
            <p>Nossa plataforma conecta você exclusivamente a prestadores certificados, licenciados e com documentação rigorosamente verificada. Solicite propostas de segurança patrimonial em nossa home gratuitamente.</p>
            """
        },
        {
            "slug": "facilities-management-reduzir-custos",
            "tag": "Gestão de Facilities",
            "title": "Facilities Management: Como Reduzir Custos e Focar no Core Business",
            "desc": "Aprenda como a gestão integrada de facilities (limpeza, manutenção, controle de acesso e portaria) gera eficiência operacional nas empresas.",
            "content": """
            <h2>O Que é Facilities Management?</h2>
            <p><strong>Facilities Management</strong> (Gestão de Instalações) é o campo profissional focado em integrar pessoas, locais, processos e tecnologias em um único imóvel para garantir a funcionalidade operacional das atividades diárias. Na prática, engloba o gerenciamento da portaria, recepção, limpeza e conservação, manutenção predial preditiva, controle de pragas e jardinagem.</p>
            
            <h2>A Vantagem da Contratação Multisserviços (Single Source)</h2>
            <p>Tradicionalmente, empresas contratavam uma prestadora de limpeza, outra de portaria e uma terceira para manutenção. Esse modelo fragmentado drena tempo do RH e do setor de Compras. A integração traz enormes benefícios:</p>
            <ul>
              <li><strong>Foco no Core Business:</strong> A diretoria da sua empresa foca exclusivamente em vender e crescer, deixando o suporte de infraestrutura física com especialistas.</li>
              <li><strong>Contrato Unificado e Escala:</strong> Negociar múltiplos serviços com uma única empresa de facilities reduz o custo por colaborador devido ao ganho de escala e menor margem administrativa.</li>
              <li><strong>Liderança Única (Supervisor de Contrato):</strong> Em vez de lidar com diversos gerentes, você tem um canal direto de supervisão que coordena toda a equipe no seu imóvel.</li>
            </ul>

            <h2>O Impacto do Ambiente de Trabalho nos Resultados</h2>
            <p>Um prédio limpo, com iluminação correta, ar-condicionado limpo e porteiros receptivos aumenta comprovadamente a produtividade dos funcionários e melhora a percepção de clientes e visitantes sobre a marca corporativa.</p>

            <h2>Encontre as Melhores Empresas de Facilities</h2>
            <p>Use a plataforma Cota Facilities para cotar e receber propostas de prestadoras de multisserviços na sua região em até 24 horas.</p>
            """
        }
    ]
    
    # Template para artigo
    article_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Cota Facilities</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://cotafacilities.com.br/blog/artigos/{slug}.html">
  <link rel="icon" type="image/jpeg" href="../../cotafacilities.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/main.css">
  <link rel="stylesheet" href="../../css/layout.css">
  <link rel="stylesheet" href="../../css/components.css">
  <link rel="stylesheet" href="../../css/animations.css">
  <style>
    body { background-color: var(--color-navy); }
    .art-container {
      max-width: 800px;
      margin-inline: auto;
      padding: var(--space-24) var(--space-4) var(--space-20);
    }
    .art-header {
      margin-bottom: var(--space-8);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      padding-bottom: var(--space-6);
    }
    .art-meta-row {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 13px;
      color: var(--color-muted);
      margin-top: 12px;
    }
    .art-body {
      font-size: 16.5px;
      line-height: 1.8;
      color: rgba(255,255,255,0.8);
      display: flex;
      flex-direction: column;
      gap: var(--space-4);
    }
    .art-body h2 {
      color: var(--color-white);
      font-size: 22px;
      margin-top: var(--space-8);
      margin-bottom: var(--space-2);
    }
    .art-body p {
      color: rgba(255,255,255,0.78);
    }
    .art-body strong {
      color: var(--color-lime);
    }
    .art-body ul {
      list-style-type: disc;
      padding-left: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .art-body li {
      color: rgba(255,255,255,0.78);
    }
    .art-cta-box {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(123, 47, 190, 0.15) 100%);
      border: 1px solid rgba(123, 47, 190, 0.3);
      padding: 32px;
      border-radius: var(--radius-xl);
      margin-top: var(--space-12);
      text-align: center;
      box-shadow: 0 8px 32px rgba(123, 47, 190, 0.1);
    }
  </style>
  <!-- JSON-LD: Product (AggregateRating for Google stars) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "{title}",
    "image": "https://cotafacilities.com.br/cota.png",
    "description": "{desc}",
    "brand": {
      "@type": "Brand",
      "name": "Cota Facilities"
    },
    "offers": {
      "@type": "AggregateOffer",
      "priceCurrency": "BRL",
      "lowPrice": "0",
      "highPrice": "0",
      "offerCount": "10"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "5.0",
      "bestRating": "5",
      "worstRating": "1",
      "ratingCount": "1829"
    }
  }
  </script>
</head>
<body>
  <!-- Navbar -->
  <nav id="navbar" class="navbar scrolled">
    <div class="container navbar-inner">
      <a href="../../" class="navbar-logo">
        <img src="../../cota.png" alt="Cota Facilities" height="38">
      </a>
      <div class="navbar-links">
        <a href="../../#como-funciona" class="nav-link">Como Funciona</a>
        <a href="../../#servicos" class="nav-link">Serviços</a>
        <a href="../" class="nav-link">Blog</a>
      </div>
      <a href="../../#cotacao" class="btn-nav">Solicitar Cotações</a>
    </div>
  </nav>

  <article class="art-container">
    <header class="art-header">
      <span class="section-tag">{tag}</span>
      <h1 style="font-size: clamp(28px, 4vw, 40px); line-height: 1.2;">{title}</h1>
      <div class="art-meta-row">
        <span>Por <strong>Redação Cota Facilities</strong></span>
        <span>·</span>
        <span>Leitura rápida</span>
        <span>·</span>
        <span>Atualizado recentemente</span>
      </div>
    </header>

    <div class="art-body">
      {content}
    </div>

    <div class="art-cta-box">
      <h3 style="color: var(--color-white); margin-bottom: 8px;">Precisa de Cotações para sua Empresa?</h3>
      <p style="margin-bottom: 20px;">Receba propostas comerciais das melhores empresas de portaria, segurança e limpeza da sua cidade.</p>
      <a href="../../#cotacao" class="btn-primary" style="display:inline-flex; width:auto; padding: 12px 32px;">Solicitar Cotações Gratuitas</a>
    </div>
  </article>
</body>
</html>"""
    
    generated_article_urls = []
    
    # IMPORTANTE: Corrigido bug de KeyError no .format() devido a chaves de CSS
    for art in artigos_data:
        art_html = article_template
        art_html = art_html.replace("{title}", art["title"])
        art_html = art_html.replace("{desc}", art["desc"])
        art_html = art_html.replace("{tag}", art["tag"])
        art_html = art_html.replace("{slug}", art["slug"])
        art_html = art_html.replace("{content}", art["content"])
        
        file_name = f"{art['slug']}.html"
        output_file = os.path.join("blog", "artigos", file_name)
        with open(output_file, "w", encoding="utf-8") as f_art:
            f_art.write(art_html)
            
        generated_article_urls.append(f"https://cotafacilities.com.br/blog/artigos/{file_name}")
        print(f"   [GERADO] {art['title']} -> /blog/artigos/{file_name}")
        
    return generated_article_urls

def generate_sitemap(city_urls, article_urls):
    """Gera o arquivo sitemap.xml na raiz do projeto contendo todas as URLs."""
    print("Gerando sitemap.xml...")
    now = datetime.now().strftime("%Y-%m-%d")
    
    xml_parts = []
    xml_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # 1. URLs Principais
    urls_base = [
        ("https://cotafacilities.com.br/", "1.0", "daily"),
        ("https://cotafacilities.com.br/blog/", "0.8", "weekly")
    ]
    
    for url, priority, freq in urls_base:
        xml_parts.append(f'  <url>')
        xml_parts.append(f'    <loc>{url}</loc>')
        xml_parts.append(f'    <lastmod>{now}</lastmod>')
        xml_parts.append(f'    <changefreq>{freq}</changefreq>')
        xml_parts.append(f'    <priority>{priority}</priority>')
        xml_parts.append(f'  </url>')
        
    # 2. Artigos do Blog
    for url in article_urls:
        xml_parts.append(f'  <url>')
        xml_parts.append(f'    <loc>{url}</loc>')
        xml_parts.append(f'    <lastmod>{now}</lastmod>')
        xml_parts.append(f'    <changefreq>monthly</changefreq>')
        xml_parts.append(f'    <priority>0.7</priority>')
        xml_parts.append(f'  </url>')
        
    # 3. Páginas de SEO Programático de Cidades
    for url in city_urls:
        xml_parts.append(f'  <url>')
        xml_parts.append(f'    <loc>{url}</loc>')
        xml_parts.append(f'    <lastmod>{now}</lastmod>')
        xml_parts.append(f'    <changefreq>weekly</changefreq>')
        xml_parts.append(f'    <priority>0.9</priority>')
        xml_parts.append(f'  </url>')
        
    xml_parts.append('</urlset>')
    
    with open("sitemap.xml", "w", encoding="utf-8") as f_xml:
        f_xml.write("\n".join(xml_parts))
        
    print(f"   [GERADO] sitemap.xml ({len(urls_base) + len(article_urls) + len(city_urls)} URLs registradas)")

def main():
    city_urls = generate_city_pages()
    article_urls = generate_blog()
    generate_sitemap(city_urls, article_urls)
    print("Processo finalizado com sucesso! Seu SEO programatico com multi-intencoes esta pronto.")

if __name__ == "__main__":
    main()
