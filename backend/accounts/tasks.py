from celery import shared_task # type: ignore
from django.core.mail import send_mail
from accounts.models import CustomUser
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


@shared_task
def send_welcome_email(user_id, token):
    print('working fine')
    user= CustomUser.objects.get(id=user_id)
    subject= 'Welcome to AI Personal Trainer'
    verification_url = f"http://localhost:8000/api/verify-email/?token={token}"
    message= f"Hello {user.email},\n\nThank you for registering with AI Personal Trainer. Please verify your email address by clicking the link below:\n\n{verification_url}"
    from_email= settings.DEFAULT_FROM_EMAIL
    recipients_list= [user.email]

    send_mail(subject, message, from_email, recipients_list)

def get_email_token(user):
    return default_token_generator.make_token(user)
