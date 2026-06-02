#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de automação para publicação diária incremental de Landing Pages
baseado em um banco de dados hospedado no Google Sheets.
Gera exatamente 1 página por execução, atualiza o sitemap.xml e published_pages.json.
"""

import os
import re
import io
import csv
import sys
import json
import urllib.request
import unicodedata
from datetime import datetime

# URL pública da planilha exportada em formato CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1Fr8iJam3V42jElGtfHcNWEhiziPl3TzeI9Pj1U55krY/export?format=csv"
TEMPLATE_PATH = "index.html"
STATE_FILE = "published_pages.json"
SITEMAP_FILE = "sitemap.xml"

# Banco de dados de FAQs por intenção / serviço
FAQ_DATA = {
    "geral": [
        {"q": "Como funciona a Cota Facilities em {cidade}?", "a": "Você seleciona o serviço desejado, informa sua cidade e quantas cotações deseja receber. Em até 24 horas, empresas verificadas de {cidade} e região entram em contato com propostas comerciais completas."},
        {"q": "A plataforma cobra alguma taxa do comprador?", "a": "Não, o serviço é 100% gratuito para quem solicita as cotações. Nosso modelo é remunerado pelas prestadoras de serviço credenciadas na plataforma."},
        {"q": "As empresas cadastradas em {cidade} são seguras?", "a": "Sim. Realizamos uma checagem rigorosa de regularidade fiscal, licenças municipais e federais antes de homologar os prestadores na plataforma."}
    ],
    "portaria": [
        {"q": "Quais as vantagens de terceirizar o serviço de portaria em {cidade}?", "a": "A terceirização elimina a gestão direta de RH, custos com rescisões e passivos trabalhistas. Além disso, garante cobertura imediata em faltas, férias ou licenças sem custo extra para o contratante."},
        {"q": "Como é garantido o treinamento dos porteiros em {cidade}?", "a": "As empresas parceiras em {cidade} fornecem treinamentos de controle de acesso, postura profissional e atendimento ao cliente de forma constante e periódica."},
        {"q": "Os porteiros terceirizados em {cidade} trabalham uniformizados?", "a": "Sim, todos os profissionais se apresentam devidamente uniformizados, identificados por crachá e equipados com os EPIs exigidos por lei."}
    ],
    "controle_acesso": [
        {"q": "Como funciona o controle de acesso integrado à portaria em {cidade}?", "a": "Ele combina sistemas de hardware (catracas, biometria, reconhecimento facial) com a supervisão de porteiros ou operadores de acesso, gerando maior segurança física em {cidade}."},
        {"q": "O que é portaria virtual e quando contratar em {cidade}?", "a": "A portaria virtual ou remota monitora os acessos à distância a partir de uma central blindada 24h. É ideal para condomínios residenciais que buscam reduzir o custo da taxa condominial em até 50%."},
        {"q": "Os equipamentos de controle de acesso estão inclusos na cotação em {cidade}?", "a": "Isso depende da modalidade de contrato. A maioria das prestadoras em {cidade} oferece opções de comodato (locação inclusa no serviço) ou venda direta dos equipamentos de controle de acesso."}
    ],
    "seguranca_patrimonial": [
        {"q": "O que abrange o serviço de segurança patrimonial em {cidade}?", "a": "Abrange desde o planejamento de segurança (análise de vulnerabilidades do local) até a presença física de vigilantes, rondas táticas motorizadas e monitoramento tecnológico 24h."},
        {"q": "Como contratar uma empresa de segurança patrimonial regularizada em {cidade}?", "a": "É fundamental verificar a regularidade da prestadora. Nossa plataforma pré-avalia todos os prestadores de {cidade}, garantindo que possuem licença municipal e idoneidade fiscal comprovada."},
        {"q": "Qual o prazo médio para iniciar o posto de vigilância em {cidade}?", "a": "Após a assinatura do contrato comercial, o prazo médio de implantação física do posto com profissionais treinados em {cidade} varia de 5 a 15 dias úteis."}
    ],
    "seguranca_privada": [
        {"q": "Qual a diferença entre porteiro e vigilante em {cidade}?", "a": "O vigilante passa por curso homologado pela Polícia Federal, tem formação específica para segurança ativa e pode trabalhar armado. O porteiro atua estritamente na recepção e controle administrativo de acesso."},
        {"q": "As empresas de segurança em {cidade} têm autorização da PF?", "a": "Sim. Conforme as normas nacionais, a segurança privada armada ou desarmada exige Autorização de Funcionamento expedida pela Polícia Federal. Nós filtramos e aprovamos apenas empresas regulares em {cidade}."},
        {"q": "Como funciona a ronda motorizada na região de {cidade}?", "a": "Um vigilante conduz veículo caracterizado (carro ou moto) e realiza rondas periódicas de segurança agendadas ou aleatórias no perímetro do imóvel, inspecionando portões e cercas."}
    ],
    "limpeza_terceirizada": [
        {"q": "Qual o foco dos serviços de limpeza comercial em {cidade}?", "a": "Ele abrange a higienização de escritórios, recepções, sanitários, copas e áreas de circulação comum, mantendo o ambiente de trabalho limpo e produtivo em {cidade}."},
        {"q": "Os produtos de limpeza são fornecidos pela empresa contratada em {cidade}?", "a": "Geralmente sim. O contrato de limpeza predial ou corporativa inclui o fornecimento de produtos profissionais e equipamentos de proteção individual (EPIs)."},
        {"q": "A limpeza terceirizada realiza serviços em altura em {cidade}?", "a": "Sim. Algumas prestadoras em {cidade} possuem equipes especializadas e certficadas pela NR-35 para limpeza de fachadas e vidros em altura."}
    ],
    "zelador": [
        {"q": "Quais as principais responsabilidades de um zelador terceirizado em {cidade}?", "a": "Supervisão da limpeza diária, fiscalização do funcionamento das instalações (bombas, geradores), recebimento de prestadores externos e pequenos reparos elétricos ou hidráulicos."},
        {"q": "Qual a diferença entre zelador e auxiliar de serviços gerais?", "a": "O zelador gerencia o andamento do prédio e faz a manutenção técnica básica. O auxiliar de serviços gerais foca na limpeza física, conservação e organização de materiais em {cidade}."},
        {"q": "A empresa de facilities garante a substituição imediata do zelador?", "a": "Sim, em caso de falta, férias ou licença de qualquer natureza, um zelador substituto homologado é enviado imediatamente ao condomínio em {cidade}."}
    ],
    "jardinagem": [
        {"q": "Como funciona a terceirização de jardinagem e paisagismo em {cidade}?", "a": "A empresa parceira envia profissionais qualificados com equipamentos próprios (cortadores, roçadeiras, tesouras) para realizar a manutenção periódica ou projetos de novos jardins em {cidade}."},
        {"q": "Qual a frequência ideal para manutenção de áreas verdes em {cidade}?", "a": "Para áreas residenciais ou comerciais de {cidade}, recomenda-se visitas quinzenais ou mensais na primavera/verão, e espaçadas no outono/inverno, dependendo do crescimento da vegetação."},
        {"q": "Os insumos (adubos, sementes) estão inclusos no orçamento de jardinagem?", "a": "Fica a critério do contrato. A maioria das propostas em {cidade} separa a mão de obra e maquinário do fornecimento de mudas, terra tratada e insumos, cobrados sob demanda."}
    ],
    "recepcao": [
        {"q": "Quais as atribuições de uma recepcionista terceirizada em {cidade}?", "a": "Atendimento telefônico, triagem de correspondências, recepção de visitantes e clientes, controle de crachás e cadastro nos sistemas de controle de acesso da empresa em {cidade}."},
        {"q": "Como funciona o suporte bilíngue para recepção corporativa em {cidade}?", "a": "Nossas parceiras em {cidade} possuem banco de talentos com recepcionistas bilíngues (inglês/espanhol) qualificadas para atendimento de multinacionais ou hotéis."},
        {"q": "A recepcionista terceirizada pode exercer atividades administrativas?", "a": "Sim. É possível alinhar o escopo para atividades de apoio administrativo básico, como controle de fluxo de motoboys, agendamento de salas de reunião e arquivos."}
    ],
    "copeira": [
        {"q": "O que faz uma copeira terceirizada em {cidade}?", "a": "Prepara e serve cafés, chás, águas e lanches para a diretoria, colaboradores e visitantes. Também cuida da higienização de utensílios, organização da copa e controle de suprimentos em {cidade}."},
        {"q": "Como funciona o uniforme e higiene de uma copeira em {cidade}?", "a": "A apresentação pessoal é impecável: uniforme social ou padrão copa, cabelos totalmente presos (com touca se necessário), unhas limpas e uso de EPIs como luvas e sapatos antiderrapantes."},
        {"q": "Posso contratar copeira terceirizada para eventos pontuais em {cidade}?", "a": "Sim, as prestadoras atendem tanto contratos mensais contínuos quanto demandas temporárias de copeiras e garçons para feiras, congressos e eventos corporativos em {cidade}."}
    ]
}

def slugify(value):
    """Converte o nome da cidade ou título em um slug de URL amigável e limpo."""
    value = str(value)
    # Tratar Hortolândia -> hortolandia, Santa Bárbara D'Oeste -> santa-barbara-d-oeste
    value = value.replace("'", " ").replace("’", " ")
    # Normalizar Unicode para retirar acentos
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = value.lower()
    value = re.sub(r'[^\w\s-]', '', value)
    value = re.sub(r'[-\s]+', '-', value)
    return value.strip('-')

def normalize_city_name(city):
    """Normaliza o nome da cidade removendo apostrofes curvadas para casamento exato com o template."""
    return city.replace("’", "'").strip()

def get_clean_title_slug(titulo, cidade):
    """Retorna o slug do título limpo de menções à cidade."""
    city_suffix = f" em {cidade}"
    title_clean = titulo
    if title_clean.lower().endswith(city_suffix.lower()):
        title_clean = title_clean[:-len(city_suffix)]
    else:
        # Fallback caso a cidade não esteja no final da frase
        title_clean = re.sub(re.escape(cidade), '', title_clean, flags=re.IGNORECASE)
    
    # Substituir múltiplos espaços por um único
    title_clean = re.sub(r'\s+', ' ', title_clean).strip()
    return slugify(title_clean)

def get_service_from_title(title):
    """Retorna a chave do serviço baseado em termos de busca do título."""
    title_lower = title.lower()
    if any(k in title_lower for k in ["portaria", "recepcao", "recepcionista"]):
        return "portaria"
    elif any(k in title_lower for k in ["controlador de acesso", "controle de acesso"]):
        return "controle-acesso"
    elif any(k in title_lower for k in ["limpeza", "conservacao"]):
        return "limpeza"
    elif any(k in title_lower for k in ["zelador", "zeladoria", "manutencao"]):
        return "manutencao"
    elif any(k in title_lower for k in ["seguranca", "vigia", "ronda"]):
        return "seguranca"
    return None

def get_faq_for_title(title):
    """Escolhe a melhor lista de FAQs e palavra-chave associada com base no título."""
    title_lower = title.lower()
    if any(k in title_lower for k in ["portaria", "porteiro"]):
        return FAQ_DATA["portaria"], "Serviço de Portaria"
    elif any(k in title_lower for k in ["controlador de acesso", "controle de acesso"]):
        return FAQ_DATA["controle_acesso"], "Controle de Acesso"
    elif any(k in title_lower for k in ["limpeza", "conservacao"]):
        return FAQ_DATA["limpeza_terceirizada"], "Limpeza Terceirizada"
    elif any(k in title_lower for k in ["zelador", "zeladoria", "manutencao"]):
        return FAQ_DATA["zelador"], "Zelador Terceirizado"
    elif any(k in title_lower for k in ["jardinagem", "areas verdes"]):
        return FAQ_DATA["jardinagem"], "Jardinagem Terceirizada"
    elif any(k in title_lower for k in ["recepcao", "recepcionista"]):
        return FAQ_DATA["recepcao"], "Recepção Terceirizada"
    elif "copeira" in title_lower:
        return FAQ_DATA["copeira"], "Copeira Terceirizada"
    elif any(k in title_lower for k in ["seguranca", "vigia", "ronda"]):
        return FAQ_DATA["seguranca_patrimonial"], "Segurança Patrimonial"
    return FAQ_DATA["geral"], "Serviços de Facilities"

def build_faq_markup(faq_list, keyword, cidade):
    """Gera o HTML estruturado do FAQ específico para a intenção e a cidade."""
    faq_items = []
    
    for item in faq_list:
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
        <h2>Perguntas Frequentes sobre {keyword} em {cidade}</h2>
        <p>Tudo o que você precisa saber antes de contratar {keyword.lower()} na sua região</p>
      </div>

      <div class="faq-grid">
        <div class="faq-column">
          {faq_str}
        </div>
      </div>

      <div class="faq-cta reveal">
        <p>Ainda tem dúvidas? Nossa equipe está pronta para ajudar.</p>
        <a href="https://wa.me/5519999115496?text=Olá,%20tenho%20dúvidas%20sobre%20{keyword}%20em%20{cidade}." target="_blank" rel="noopener" class="btn-primary">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M15.5 2.5C13.94 0.94 11.86 0 9 0C4.03 0 0 4.03 0 9C0 10.59 0.44 12.11 1.26 13.41L0 18L4.71 16.76C5.98 17.5 7.45 17.9 9 17.9C13.97 17.9 18 13.87 18 8.9C18 6.04 17.06 4.06 15.5 2.5Z" fill="white" fill-opacity="0.3"/><path d="M9.5 10.5L7 8L4.5 5.5" stroke="white" stroke-width="1.5" stroke-linecap="round"/></svg>
          Falar no WhatsApp
        </a>
      </div>
    </div>
  </section>"""
    
    return markup

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
    
    # Ajustar links do navbar para irem para a home raiz com a âncora correta
    adjusted = adjusted.replace('href="#como-funciona"', f'href="{prefix}#como-funciona"')
    adjusted = adjusted.replace('href="#servicos"', f'href="{prefix}#servicos"')
    adjusted = adjusted.replace('href="#prestadores"', f'href="{prefix}#prestadores"')
    adjusted = adjusted.replace('href="#cotacao"', f'href="{prefix}#cotacao"')
    adjusted = adjusted.replace('href="#"', f'href="{prefix}"')
    
    # Também tratar o link da logo e blog no navbar para caminhos corretos
    adjusted = adjusted.replace('href="#navbar"', f'href="{prefix}#navbar"')
    
    return adjusted

def generate_description(titulo, cidade):
    """Gera uma descrição meta otimizada para SEO local e conversão."""
    return f"Solicite cotações gratuitas para {titulo} na Cota Facilities. Receba até 3 propostas comerciais em 24h de empresas de facilities credenciadas e verificadas em {cidade} e região. Sem burocracia."

def parse_existing_urls_from_sitemap(sitemap_path):
    """Extrai todas as URLs registradas no sitemap.xml atual usando Regex."""
    if not os.path.exists(sitemap_path):
        return []
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    locs = re.findall(r'<loc>(.*?)</loc>', content)
    return [l.strip() for l in locs if l.strip()]

def update_sitemap(new_urls, sitemap_path):
    """Mescla novas URLs com as existentes do sitemap.xml e reescreve-o ordenadamente."""
    existing_urls = parse_existing_urls_from_sitemap(sitemap_path)
    
    # Conjunto para checagem rápida de duplicados
    all_urls_set = set(existing_urls)
    merged_urls = list(existing_urls)
    
    for url in new_urls:
        if url not in all_urls_set:
            merged_urls.append(url)
            all_urls_set.add(url)
            
    now = datetime.now().strftime("%Y-%m-%d")
    xml_parts = []
    xml_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for url in merged_urls:
        if url == "https://cotafacilities.com.br/":
            priority, freq = "1.0", "daily"
        elif url == "https://cotafacilities.com.br/blog/":
            priority, freq = "0.8", "weekly"
        elif "blog/artigos/" in url:
            priority, freq = "0.7", "monthly"
        else:
            priority, freq = "0.9", "weekly"
            
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{url}</loc>')
        xml_parts.append(f'    <lastmod>{now}</lastmod>')
        xml_parts.append(f'    <changefreq>{freq}</changefreq>')
        xml_parts.append(f'    <priority>{priority}</priority>')
        xml_parts.append('  </url>')
        
    xml_parts.append('</urlset>')
    
    with open(sitemap_path, "w", encoding="utf-8") as f_xml:
        f_xml.write("\n".join(xml_parts))
        
    print(f"Sitemap atualizado: {sitemap_path} ({len(merged_urls)} URLs no total)")

def split_title_for_h1(titulo, cidade):
    """Divide o título de forma limpa para exibição em duas linhas no H1 do Hero."""
    city_suffix = f" em {cidade}"
    if titulo.lower().endswith(city_suffix.lower()):
        h1_l1 = titulo[:-len(city_suffix)].strip()
        h1_l2 = titulo[-len(city_suffix):].strip() # "em {cidade}"
    else:
        h1_l1 = titulo
        h1_l2 = f"em {cidade}"
    return h1_l1, h1_l2

def fetch_sheet_csv(url):
    """Baixa a planilha Google Sheets pública em formato CSV e parseia como lista de linhas."""
    print(f"Baixando dados do Google Sheets...")
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8-sig')
    
    if "<html" in content.lower():
        raise Exception("O download falhou. Certifique-se de que a planilha está configurada para compartilhamento público ('Qualquer pessoa com o link pode ler').")
        
    reader = csv.reader(io.StringIO(content))
    return list(reader)

def main():
    # Processar argumentos da linha de comando
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    
    if dry_run:
        print("====== MODO TESTE (DRY-RUN) ATIVO ======")
        print("Nenhum arquivo físico será persistido no repositório.")
    
    # 1. Carregar Estado
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            try:
                state = json.load(f)
            except Exception:
                state = {"published_slugs": []}
    else:
        state = {"published_slugs": []}
        
    published_slugs = set(state.get("published_slugs", []))
    
    # 2. Carregar Planilha (Banco de dados)
    try:
        rows = fetch_sheet_csv(SHEET_CSV_URL)
    except Exception as e:
        print(f"Erro ao baixar planilha: {e}")
        sys.exit(1)
        
    if not rows or len(rows) < 2:
        print("Planilha vazia ou sem linhas de dados.")
        sys.exit(1)
        
    headers = rows[0]
    data_rows = rows[1:]
    print(f"Total de {len(data_rows)} registros de SEO carregados da planilha.")
    
    # 3. Filtrar itens a serem publicados nesta execução
    candidates = []
    for idx, row in enumerate(data_rows):
        if len(row) < 3:
            continue
            
        titulo = row[0].strip()
        subtitulo = row[1].strip()
        cidade_raw = row[2].strip()
        backlinks_raw = row[3].strip() if len(row) > 3 else ""
        
        if not titulo or not cidade_raw:
            continue
            
        cidade = normalize_city_name(cidade_raw)
        cidade_slug = slugify(cidade)
        title_slug = get_clean_title_slug(titulo, cidade)
        
        full_slug = f"{cidade_slug}/{title_slug}"
        output_file_path = os.path.join(cidade_slug, title_slug, "index.html")
        
        # Ignorar se já consta no JSON ou se a pasta já existe fisicamente no repositório (evita sobreposições e bugs)
        if full_slug in published_slugs and not force:
            continue
        if os.path.exists(output_file_path) and not force:
            # Também adicionar ao published_slugs para manter consistência caso exista fisicamente
            published_slugs.add(full_slug)
            continue
            
        candidates.append({
            "line_number": idx + 2, # Linha real no Google Sheets (1-indexed + header)
            "titulo": titulo,
            "subtitulo": subtitulo,
            "cidade": cidade,
            "cidade_slug": cidade_slug,
            "title_slug": title_slug,
            "full_slug": full_slug,
            "backlinks": backlinks_raw,
            "service": get_service_from_title(titulo)
        })
        
    print(f"Total de registros inéditos pendentes na fila: {len(candidates)}")
    
    if not candidates:
        print("Tudo publicado! Não há novas landing pages a serem geradas.")
        sys.exit(0)
        
    # Pegar exatamente a primeira da fila para a publicação incremental
    to_publish = candidates[:1]
    print(f"Páginas selecionadas para publicação nesta rodada ({len(to_publish)} de 1 planejada):")
    for item in to_publish:
        print(f"  - Linha {item['line_number']}: {item['titulo']} (/{item['full_slug']}/)")
        
    # 4. Carregar Template HTML
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Erro: Template base '{TEMPLATE_PATH}' não encontrado na raiz.")
        sys.exit(1)
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f_temp:
        template_content = f_temp.read()
        
    new_urls = []
    
    # 5. Processar e renderizar as LPs selecionadas
    for item in to_publish:
        cidade = item["cidade"]
        cidade_slug = item["cidade_slug"]
        title_slug = item["title_slug"]
        titulo = item["titulo"]
        subtitulo = item["subtitulo"]
        backlinks_str = item["backlinks"]
        service_key = item["service"]
        full_slug = item["full_slug"]
        
        depth = 2
        canonical = f"https://cotafacilities.com.br/{full_slug}/"
        
        # Gerar os backlinks estruturados
        backlink_elements = []
        if backlinks_str:
            for url in backlinks_str.split("\n"):
                url = url.strip()
                if url:
                    backlink_elements.append(f'    <a href="{url}">{url}</a>')
        
        if backlink_elements:
            backlinks_html = '\n  <!-- Links Ocultos para SEO -->\n  <div style="display:none;" aria-hidden="true">\n' + '\n'.join(backlink_elements) + '\n  </div>\n'
        else:
            backlinks_html = ''
            
        custom_html = template_content
        
        # Injetar variáveis de pré-seleção do formulário no head
        preselect_script = f'\n  <script>window.PRESELECTED_CITY = "{cidade}";'
        if service_key:
            preselect_script += f'\n  window.PRESELECTED_SERVICE = "{service_key}";'
        preselect_script += '\n  </script>\n</head>'
        custom_html = custom_html.replace("</head>", preselect_script)
        
        # Formatar títulos de SEO e Descrições
        page_title = f"{titulo} | Cota Facilities"
        page_desc = generate_description(titulo, cidade)
        
        # Substituir tags do cabeçalho
        custom_html = re.sub(r'<title>.*?</title>', f'<title>{page_title}</title>', custom_html)
        custom_html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{page_desc}">', custom_html)
        
        # OpenGraph e Twitter tags
        custom_html = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{page_title}">', custom_html)
        custom_html = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{page_desc}">', custom_html)
        custom_html = re.sub(r'<meta name="twitter:title" content=".*?">', f'<meta name="twitter:title" content="{page_title}">', custom_html)
        custom_html = re.sub(r'<meta name="twitter:description" content=".*?">', f'<meta name="twitter:description" content="{page_desc}">', custom_html)
        
        # Injetar Canonical Link
        custom_html = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="{canonical}">', custom_html)
        
        # Substituir dados do Product Schema (SEO Stars)
        custom_html = custom_html.replace(
            '"name": "Cota Facilities — Cotações de Portaria, Segurança e Facilities em Minutos"',
            f'"name": "{page_title}"'
        )
        custom_html = custom_html.replace(
            '"description": "Solicite cotações de portaria terceirizada, segurança patrimonial, controle de acesso, limpeza terceirizada, vigilante e mais. Conectamos sua empresa às melhores prestadoras verificadas. 100% gratuito e sem burocracia."',
            f'"description": "{page_desc}"'
        )
        
        # Ajustar links de ativos e caminhos de navbar (depth = 2)
        custom_html = adjust_assets_path(custom_html, depth)
        
        # Mudar H1 Hero
        h1_l1, h1_l2 = split_title_for_h1(titulo, cidade)
        h1_regex = r'<h1 class="hero-headline">.*?</h1>'
        new_h1_markup = f"""<h1 class="hero-headline">
          <span class="line-wrap"><span class="hero-word">{h1_l1}</span></span>
          <span class="line-wrap"><span class="hero-word hero-word--accent">{h1_l2}</span></span>
          <span class="line-wrap"><span class="hero-word hero-word--light">{subtitulo}</span></span>
        </h1>"""
        custom_html = re.sub(h1_regex, new_h1_markup, custom_html, flags=re.DOTALL)
        
        # Ajustar textos adicionais de branding local do hero
        custom_html = custom_html.replace(
            "Conectamos sua empresa às melhores prestadoras certificadas de São Paulo.",
            f"Conectamos sua empresa às melhores prestadoras certificadas de {cidade} e região."
        )
        custom_html = re.sub(
            r'<span>500\+ empresas verificadas na plataforma</span>',
            f'<span>Empresas de facilities verificadas em {cidade}</span>',
            custom_html
        )
        
        # Substituir o FAQ da página baseado no serviço do título
        faq_list, faq_keyword = get_faq_for_title(titulo)
        faq_markup = build_faq_markup(faq_list, faq_keyword, cidade)
        custom_html = re.sub(r'<section id="faq" class="section-faq".*?</section>', faq_markup, custom_html, flags=re.DOTALL)
        
        # Pré-selecionar a cidade no dropdown padrão do formulário
        target_option = f'<option value="{cidade}">'
        selected_option = f'<option value="{cidade}" selected>'
        custom_html = custom_html.replace(target_option, selected_option)
        
        # Injetar os backlinks fixos e escondidos imediatamente antes do fechamento do footer
        if backlinks_html:
            custom_html = custom_html.replace("</footer>", backlinks_html + "\n</footer>")
            
        # 6. Salvar arquivos físicos (caso não seja dry-run)
        if not dry_run:
            output_dir = os.path.join(cidade_slug, title_slug)
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, "index.html")
            with open(output_file, "w", encoding="utf-8") as f_out:
                f_out.write(custom_html)
                
            published_slugs.add(full_slug)
            print(f"   [GERADO] {output_file} criado com sucesso.")
        else:
            print(f"   [DRY-RUN] Seria gerada a página para {canonical}")
            
        new_urls.append(canonical)
        
    # 7. Persistir Estado e Atualizar Sitemap
    if not dry_run:
        state["published_slugs"] = sorted(list(published_slugs))
        with open(STATE_FILE, "w", encoding="utf-8") as f_state:
            json.dump(state, f_state, indent=2)
        print(f"Estado de postagem salvo em {STATE_FILE}.")
        
        # Atualizar sitemap.xml
        update_sitemap(new_urls, SITEMAP_FILE)
    else:
        print("====== MODO TESTE (DRY-RUN) CONCLUÍDO COM SUCESSO ======")

if __name__ == "__main__":
    main()
