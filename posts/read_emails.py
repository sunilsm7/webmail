import getpass, imaplib
import smtplib
import time
import email
import base64

from django.conf import settings
IMAP4_HOST = getattr(settings, "IMAP4_HOST")
IMAP4_PORT = getattr(settings, "IMAP4_PORT")


def get_emails(user_email, user_pass):
    message_list = []
    login_failed = False
    try: 
        mail = imaplib.IMAP4_SSL(IMAP4_HOST, IMAP4_PORT)
        mail.login(user_email, user_pass)
    except Exception as e:
        login_failed = True
        print(e)
        return message_list, login_failed
    mail.select()

    data_type, message_data = M.search(None, 'ALL')  # noqa
    mail_ids = message_data[0]
    id_list = mail_ids.split()

    for i in reversed(id_list):
        typ, data = mail.fetch(i, '(RFC822)' )  # noqa

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode("utf-8"))
                email_subject = msg.get('subject')
                email_from = msg.get('from')
                email_date = msg.get('date')
                mail_dict = {
                    'from': email_from,
                    'subject': email_subject,
                    'date': email_date,
                    'message': msg
                }
                message_list.append(mail_dict)

    mail.close()
    mail.logout()

    return message_list, login_failed
