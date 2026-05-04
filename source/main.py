import os
from local_pkg import (
    buscar_links_atuais,
    buscar_links_atuais_diogrande, 
    carregar_historico_urls, 
    salvar_no_historico,
    baixar_arquivo_individual,
    enviar_email_com_anexo
)
from local_pkg.config import PASTA_DESTINO

def executar():
    print("--- Iniciando Monitoramento ---")
    
    # 1. Mapeamento
    urls_vistas = carregar_historico_urls()
    
    # Busca dados do Diogrande E do site original (DOE)
    dados_atuais = buscar_links_atuais_diogrande() + buscar_links_atuais()
    
    # 2. Identificação de Novidades
    novos = [item for item in dados_atuais if item['url'] not in urls_vistas]
    
    if not novos:
        print("Nenhuma novidade encontrada.")
        return

    # 3. Processamento (Download + E-mail + Histórico)
    for item in novos:
        sucesso = baixar_arquivo_individual(item['url'], item['pdf_name'])
        
        if sucesso:
            caminho_pdf = os.path.join(PASTA_DESTINO, item['pdf_name'])
            
            # Só envia e-mail e salva histórico se o download funcionou
            enviar_email_com_anexo(caminho_pdf, item['pdf_name'])
            salvar_no_historico([item])
            
    print("--- Ciclo Finalizado ---")

if __name__ == "__main__":
    executar()