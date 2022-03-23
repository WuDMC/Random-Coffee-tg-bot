import re
import string
import secrets

from settings import COMPANY

re_mail = re.compile(r'\b.*\b')
alphabet = string.ascii_letters + string.digits


def is_correct_mail(mail):
    return re_mail.fullmatch(mail)


def generate_password():
    return ''.join(secrets.choice(alphabet) for i in range(20))