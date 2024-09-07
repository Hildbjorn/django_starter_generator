from django.core.mail import send_mail

from <project_name>.settings import TELEGRAM_TOKEN, MY_TELEGRAM_ID, DEFAULT_FROM_EMAIL


def email_to_customer(subject, html_message, email):
    """ Отправка письма пользователю """
    send_mail(subject, html_message,
              DEFAULT_FROM_EMAIL,
              [email],
              html_message=html_message
              )
