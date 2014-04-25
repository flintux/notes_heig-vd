#Module with fucntions for sending emails through gmail

import smtplib

def send_email(user, password, sender, recepient, subject, text):
    """Sending an email based on given settings"""
    message = """\From: {sender}\nTo: {recepient}\n"""\
    """Subject: {subject}\n\n{text}""".format(sender=sender,
                                           recepient=", ".join(recepient),
                                           subject=subject,
                                           text=text).encode('utf-8')
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(user, password)
        server.sendmail(sender, recepient, message)
        server.close()
        print('mail sent')
    except:
        print ('mail failed')

    

