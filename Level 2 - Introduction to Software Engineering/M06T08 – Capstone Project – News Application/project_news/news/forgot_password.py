import secrets
import hashlib
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import ResetToken


def build_email(user, reset_url):
    """
    :param user: The user object for whom the password reset email is being
    built.
    :param reset_url: The URL that the user will use to reset their password.

    Build and return an email message for password reset.

    :return: An EmailMessage object containing the password reset email.
    """
    subject = "Password Reset"
    user_email = user.email
    domain_email = "example@domain.com"
    body = (
        f"Hi {user.username},\n\n"
        f"Please copy and paste the following link into your browser to "
        f"reset your password:\n\n"
        f"{reset_url}"
    )
    email = EmailMessage(subject, body, domain_email, [user_email])
    return email


def generate_reset_url(user):
    """
    :param user: The user who is requesting a password reset.
    :return: A URL that the user can use to reset their password.

    Generate a password reset URL for a given user. This function will create a
    unique token with an expiry time and returns a URL that the user can use
    to reset their password.
    """
    domain = "http://127.0.0.1:8000/"
    url = f"{domain}reset_password/"

    token = str(secrets.token_urlsafe(16))
    expiry_date = datetime.now() + timedelta(minutes=5)

    ResetToken.objects.create(
        user=user,
        token=hashlib.sha1(token.encode()).hexdigest(),
        expiry_date=expiry_date,
    )

    url += f"{token}/"
    return url


def change_user_password(username, password):
    """
    :param username: The username of the user whose password is to be changed.
    :param password: The new password to set for the user.

    Saves the new password for the specified user.
    """
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
