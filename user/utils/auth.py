import string
import secrets
from random import choice
from user.models import User


def generate_unique_username(username: str) -> str:
    try:
        User.objects.get(username=username)
        generatedUsername = username + ''.join([choice(string.digits) for i in range(3)])
        return generate_unique_username(generatedUsername)
    except User.DoesNotExist:
        return username


def generate_username_from_email(email: str) -> str:
    try:
        emailUsername = email.split('@')[0]
        return generate_unique_username(emailUsername)
    except IndexError:
        raise Exception("Invalid Email")


def generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(10))


__all__ = [
    'generate_unique_username',
    'generate_username_from_email',
    'generate_password'
]
