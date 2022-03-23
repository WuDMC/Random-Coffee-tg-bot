import re
import string
import secrets

re_mail = re.compile(r'\b.*\b')
alphabet = string.ascii_letters + string.digits


def is_correct_mail(mail):
    return re_mail.match(mail)


def generate_password():
    passwrd = 'Batumi'
    print(passwrd)
    return passwrd
