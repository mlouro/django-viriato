# -*- coding: utf-8 -*-
def send_mail(send_from, send_to, subject, text, file_path, server, host, pwd):
    import smtplib
    import os
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.Utils import formatdate
    from email import Encoders

    port = 25 # or 587 (ambas as portas são usadas pelo servidor da gmail

    #Cria o objecto
    msg = MIMEMultipart()

    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    #aloca o texto à msg
    msg.attach( MIMEText(text) )

    #Permite fazer o upload de qualquer tipo de ficheiro, e aloca tb à msg
    #Crias um "for" se mandares uma lista com varios endereços
    for file in file_path:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    #faz a coneção com o servidor
    try:
        smtp = smtplib.SMTP(server,port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(host,pwd)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        return True
    except:
        return False