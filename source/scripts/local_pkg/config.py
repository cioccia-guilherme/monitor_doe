import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configurações de Scraping (Podem continuar fixas aqui)
URL_SITE = "https://www.diariooficial.ms.gov.br/"
BASE_URL = "https://assets.imprensaoficial.ms.gov.br"
HISTORICO_CSV = os.path.join(os.getenv("PATH_HISTORICO_URL"), "historico.csv")
PASTA_DESTINO = os.getenv("PATH_PDF")

# Configurações Sensíveis (Lidas do .env)
# O segundo argumento é um valor padrão caso a variável não seja encontrada
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP = os.getenv("SENHA_EMAIL")
EMAIL_DESTINATARIO = [
    'guilherme.cioccia@gmail.com',
    'lethycia.anjoss@gmail.com'
]