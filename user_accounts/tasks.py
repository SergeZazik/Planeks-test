from django.core.mail import EmailMessage
from news_service.celery import app

@app.task
def user_email_activate_task(mail_subject, message, to_email):
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()