import requests
from bs4 import BeautifulSoup
import os
import csv
import re
from .config import URL_SITE, BASE_URL, HISTORICO_CSV

def carregar_historico_urls():
    if not os.path.exists(HISTORICO_CSV):
        return set()
    urls = set()
    with open(HISTORICO_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            urls.add(row['url'])
    return urls

def limpar_nome_tag(texto):
    if "-" in texto:
        tag = texto.split("-")[-1].strip()
        tag = re.sub(r'[^\w\s-]', '', tag).replace(" ", "_").lower()
        return f"_{tag}"
    return ""

def salvar_no_historico(novos_dados):
    arquivo_novo = not os.path.exists(HISTORICO_CSV)
    with open(HISTORICO_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'pdf_name'])
        if arquivo_novo:
            writer.writeheader()
        writer.writerows(novos_dados)

def buscar_links_atuais():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL_SITE, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        resultados = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '.pdf' in href.lower():
                texto_link = a.get_text(strip=True)
                url_completa = href if href.startswith('http') else f"{BASE_URL}{href}"
                nome_base = url_completa.split('/')[-1].replace('.pdf', '')
                tag = limpar_nome_tag(texto_link)
                resultados.append({'url': url_completa, 'pdf_name': f"{nome_base}{tag}.pdf"})
        return resultados
    except Exception as e:
        print(f"Erro ao acessar o site: {e}")
        return []