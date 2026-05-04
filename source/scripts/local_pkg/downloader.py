import requests
import os
import urllib3
from .config import PASTA_DESTINO

# Desativa avisos de segurança SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def baixar_arquivo_individual(url, nome_arquivo):
    if not os.path.exists(PASTA_DESTINO):
        os.makedirs(PASTA_DESTINO)
    
    caminho_completo = os.path.join(PASTA_DESTINO, nome_arquivo)
    
    if os.path.exists(caminho_completo):
        print(f"[-] Já existe: {nome_arquivo}")
        return True # Retorna True pois o arquivo já está disponível

    try:
        print(f"[+] Baixando: {nome_arquivo}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        # Adicionado verify=False para ignorar a validação do certificado SSL
        response = requests.get(url, headers=headers, timeout=60, stream=True, verify=False)
        response.raise_for_status()

        with open(caminho_completo, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: f.write(chunk)
        return True
    except Exception as e:
        print(f"    [X] Erro ao baixar {nome_arquivo}: {e}")
        return False