import requests
from bs4 import BeautifulSoup
import os
import csv
import re
import base64
import json
import urllib.parse
import urllib3
from .config import URL_SITE, BASE_URL, HISTORICO_CSV

# Desativa os avisos de segurança para conexões sem verificação SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Desativa avisos de certificado SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def buscar_links_atuais_diogrande():
    url_api = "https://diogrande.campogrande.ms.gov.br/wp-admin/admin-ajax.php?action=edicao2_dia_json"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Cria uma sessão do requests forçando a desativação do SSL
    session = requests.Session()
    session.verify = False
    
    try:
        response = session.get(url_api, headers=headers, timeout=20)
        response.raise_for_status()  # Levanta exceção para erros HTTP
        
        dados = response.json()
        resultados = []
        
        # Uso do .get() para evitar erros caso a estrutura do JSON mude
        atual = dados.get('atual')
        ultimas_edicoes = dados.get('ultimasedicoes', [])
        
        todas = [atual] + ultimas_edicoes if atual else ultimas_edicoes
        
        for edicao in todas:
            for arq in edicao.get('arquivos', []):
                payload = {"codigodia": str(arq['codigodia'])}
                json_str = json.dumps(payload, separators=(',', ':'))
                b64 = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
                b64_url = urllib.parse.quote(b64)
                url = f"https://diogrande.campogrande.ms.gov.br/download_edicao/{b64_url}.pdf"
                
                nome_arquivo = f"diogrande_{arq.get('numeroFormatado', '')}_{str(arq.get('nomearquivo', '')).replace(' ', '_')}.pdf"
                
                resultados.append({
                    'url': url,
                    'pdf_name': nome_arquivo
                })
        return resultados
        
    except requests.exceptions.RequestException as e:
        print(f"Erro de rede ou HTTP na API do Diogrande: {e}")
    except Exception as e:
        print(f"Erro ao processar os dados da API do Diogrande: {e}")
        
    return []