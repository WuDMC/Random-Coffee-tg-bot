import random
import telebot
import schedule
from time import sleep
from threading import Thread
from telebot import types, custom_filters

from settings import ADMINS, TELEGRAM_TOKEN, SMTP
from messages import generate_password
from orm import get_user, get_no_link_users, get_no_nickname_users, set_field, create_user, get_admins, get_users, get_active_users, create_pair, delete_pairs, get_pairs

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_admins():
    for user in get_admins():
        bot.send_message(user.id, 'test')