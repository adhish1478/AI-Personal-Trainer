from celery import shared_task # type: ignore
from django.core.mail import send_mail
from accounts.models import CustomUser
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore

@shared_task
def send_welcome_email(user_id, token):
    print('working fine')
    user= CustomUser.objects.get(id=user_id)
    subject= 'Welcome to AI Personal Trainer'
    verification_url = f"http://localhost:8000/api/verify-email/?token={token}"
    message= f"Hello {user.email},\n\nThank you for registering with AI Personal Trainer. Please verify your email address by clicking the link below:\n\n{verification_url}"
    from_email= settings.EMAIL_HOST_USER
    recipients_list= [user.email]

    send_mail(subject, message, from_email, recipients_list)

def get_email_token(user):
    # This function should generate a token for the user
    refresh= RefreshToken.for_user(user)
    return str(refresh.access_token)
