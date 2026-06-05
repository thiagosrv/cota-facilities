#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera a fila de páginas SEO pendentes (seo-queue.json)
Uso: python gerar_fila_seo.py
"""
import json, unicodedata, re

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
    ("Portaria","portaria"),
    ("Controle de Acesso","controle-de-acesso"),
    ("Portaria e Controle de Acesso","portaria-e-controle-de-acesso"),
    ("Limpeza","limpeza"),
    ("Limpeza e Conservação","limpeza-e-conservacao"),
    ("Jardinagem","jardinagem"),
    ("Zelador","zelador"),
    ("Zeladoria","zeladoria"),
    ("Recepcionista","recepcionista"),
    ("Recepção","recepcao"),
    ("Vigia","vigia"),
    ("Guarda","guarda"),
    ("Segurança","seguranca"),
    ("Vigilante","vigilante"),
    ("Rondas de Segurança","rondas-de-seguranca"),
    ("Portaria para Condomínio","portaria-para-condominio"),
    ("Segurança para Empresa","seguranca-para-empresa"),
]

# Nova intenção — diferente das 4 já publicadas
NOVA_INTENCAO = {
    "slug": "como-contratar",
    "h1": "Como Contratar {s} em {c}",
    "title": "Como Contratar {s} em {c} — Guia Completo | Cota Facilities",
    "desc": "Aprenda como contratar {s} em {c} com segurança. Documentos exigidos, cuidados no contrato e como comparar fornecedores. Cotação gratuita.",
    "intro": "Contratar <strong>{s}</strong> em <strong>{c}</strong> exige atenção a documentos, contratos e idoneidade do fornecedor. Neste guia, você encontra tudo que precisa saber — e pode solicitar cotação gratuita de empresas verificadas em {c} agora mesmo.",
}

def slugify(t):
    t = unicodedata.normalize('NFD', t).encode('ascii','ignore').decode('ascii')
    t = re.sub(r"[^\w\s-]","",t.lower())
    return re.sub(r"[\s_]+","-",t.strip())

pages = []
for s_nome, s_slug in SERVICOS:
    for cidade in CIDADES:
        pages.append({
            "intent_slug":  NOVA_INTENCAO["slug"],
            "intent_h1":    NOVA_INTENCAO["h1"],
            "intent_title": NOVA_INTENCAO["title"],
            "intent_desc":  NOVA_INTENCAO["desc"],
            "intent_intro": NOVA_INTENCAO["intro"],
            "servico":      s_nome,
            "servico_slug": s_slug,
            "cidade":       cidade,
            "cidade_slug":  slugify(cidade),
        })

queue = {"total": len(pages), "next_index": 0, "pages": pages}
with open("seo-queue.json","w",encoding="utf-8") as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

print(f"Fila criada: {len(pages)} páginas em seo-queue.json")
print(f"Tempo estimado (10/dia): {len(pages)//10} dias ({len(pages)//10//30} meses)")
