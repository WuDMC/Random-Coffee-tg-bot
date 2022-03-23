import re
import string
import secrets

from settings import COMPANY

re_mail = re.compile(r'\b.*\b')
alphabet = string.ascii_letters + string.digits

passwrd = 'Путин ХУЙЛО'

def is_correct_mail(mail):
    return re_mail.fullmatch(mail) and mail.endswith(f'@{COMPANY}')


def generate_password():
    return passwrd