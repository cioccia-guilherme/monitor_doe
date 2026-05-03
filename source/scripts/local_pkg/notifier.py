import smtplib
from email.message import EmailMessage
from .config import EMAIL_REMETENTE, SENHA_APP, EMAIL_DESTINATARIO

def enviar_email_com_anexo(caminho_completo_pdf, nome_arquivo):
    msg = EmailMessage()
    msg['Subject'] = f"Novo Diário Disponível: {nome_arquivo}"
    msg['From'] = EMAIL_REMETENTE
    
    # Concatena a lista de destinatários com vírgulas
    msg['To'] = ", ".join(EMAIL_DESTINATARIO)
    
    msg.set_content(f"O sistema detectou uma nova publicação: {nome_arquivo}")

    try:
        with open(caminho_completo_pdf, 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=nome_arquivo)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(msg)
        print(f"✅ Notificação enviada: {nome_arquivo}")
    except Exception as e:
        print(f"❌ Falha ao enviar e-mail: {e}")