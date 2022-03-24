import re
import string
import secrets



re_mail = re.compile(r'\b.*\b')
alphabet = string.ascii_letters + string.digits


def is_correct_mail(mail):
    mail = 'undefined'
    return re_mail.fullmatch(mail)


def generate_password():
    passwrd = 'Batumi'
    return passwrd
