import random
import telebot
import schedule
import traceback
from time import sleep
from threading import Thread
from telebot import types, custom_filters
from datetime import datetime
import txts


from settings import ADMINS, TELEGRAM_TOKEN
from orm import get_blocked_users, get_user, get_no_link_users, get_no_nickname_users, set_field, create_user, \
    get_admins, get_users, get_active_users, create_pair, delete_pairs, get_pairs, get_inactive_users, \
    get_verified_users, get_user_field,  is_user_fillevrth, \
    get_ban_users, create_pair_history, set_pair_field, set_pair_history_field, get_pair_history, get_users_by_loc
from passwords import password_map

bot = telebot.TeleBot(TELEGRAM_TOKEN)
wudmc_tg = '1205912479'
forward_users = []
# проблема с маркдаун только решает никнеймы
__escape_markdown_map = {

    "_": "\\_",  # underscore
    "-": "\\-",  # minus

}


def __escape_markdown(raw_string):
    s = raw_string
    for k in __escape_markdown_map:
        s = s.replace(k, __escape_markdown_map[k])
    return s


forward_users


# states

class States:
    ask_password = 1
    ask_name = 2
    ask_link = 3
    ask_work = 4
    ask_about = 5
    change_name = 6
    change_link = 7
    change_work = 8
    change_about = 9
    change_user_for_ask_id_admin = 10
    update_nickname = 11
    forward_message = 12
    userfeedback = 13
    send_message_to_user_id = 14
    send_message_to_all_users = 15
    complete = 16
    wait = 17


country_map = {
        'Грузия': ['Батуми', 'Тбилиси'],
        'Португалия': ['Лиссабон'],
        'Турция': ['Анталья', 'Бодрум', 'Акьяка'],
        'Армения': ['Ереван'],
        'Израиль': ['Тель Авив', 'Рамат Ган', 'Ришон Лецион', 'Хайфа'],
        'Испания': ['Валенсия', 'Барселона'],
        'Германия': ['Штутгарт', 'Гамбург', 'Берлин'],
        'Дания': ['Рибе'],
        'Россия': ['Москва', 'Санкт-Путербург'],
    }

flag_map = {
        'Грузия': '🇬🇪',
        'Португалия': '🇵🇹',
        'Турция': '🇹🇷',
        'Армения': '🇦🇲',
        'Израиль': '🇮🇱',
        'Испания': '🇪🇸',
        'Германия': '🇩🇪',
        'Дания': '🇩🇰',
        'Россия': '🇷🇺',
        'Онлайн' : '🌎'
    }

# заготовки сообщения


# функции рассылки
def send_admins():
    for user in get_admins():
        try:
            bot.send_message(user.telegram_id, txts.msg_for_active, parse_mode='Markdown')
            sleep(1)
            bot.send_message(user.telegram_id, txts.msg_for_admins, parse_mode='Markdown')
            sleep(1)
            bot.send_message(user.telegram_id, txts.msg_for_blocked, parse_mode='Markdown')
            sleep(1)
            bot.send_message(user.telegram_id, txts.msg_for_no_link, parse_mode='Markdown')
            sleep(1)
            bot.send_message(user.telegram_id, txts.msg_for_no_nickname, parse_mode='Markdown')
            sleep(1)
        except Exception:
            set_field(user.telegram_id, 'is_active', False)
            set_field(user.telegram_id, 'is_verified', False)
            bot.send_message(wudmc_tg, f' сообщение юзеру {user.telegram_id} не отправлено: {traceback.format_exc()}')
        sleep(2)
    bot.send_message(wudmc_tg, 'Сообщения админам отправлены')


def send_no_contacts():
    bot.send_message(wudmc_tg, 'Начинаю отправку пользователям без ссылки')
    for user in get_no_link_users():
        try:
            bot.send_message(wudmc_tg, f'отправляю сообщение юзеру {user.telegram_id}')
            bot.send_message(user.telegram_id, txts.msg_for_no_link, parse_mode='Markdown')
            bot.send_message(wudmc_tg, f' сообщение юзеру {user.telegram_id} успешно отправлено')
        except Exception:
            set_field(user.telegram_id, 'is_active', False)
            set_field(user.telegram_id, 'is_verified', False)
            bot.send_message(wudmc_tg, f' сообщение юзеру {user.telegram_id} не отправлено: {traceback.format_exc()}')
        sleep(2)
    bot.send_message(wudmc_tg, 'Сообщения без ссылки отправлены')
    bot.send_message(wudmc_tg, 'Начинаю отправку пользователям без никнейма')
    for user in get_no_nickname_users():
        try:
            bot.send_message(wudmc_tg, f'отправляю сообщение юзеру {user.telegram_id}')
            bot.send_message(user.telegram_id, txts.msg_for_no_nickname, parse_mode='Markdown')
            bot.send_message(wudmc_tg, f' сообщение юзеру {user.telegram_id} успешно отправлено')
        except Exception:
            set_field(user.telegram_id, 'is_active', False)
            set_field(user.telegram_id, 'is_verified', False)
            bot.send_message(wudmc_tg, f' сообщение юзеру {user.telegram_id} не отправлено: {traceback.format_exc()}')
        sleep(2)
    bot.send_message(wudmc_tg, 'Сообщения без никнейма отправлены')


def send_blocked_users():
    bot.send_message(wudmc_tg, 'Начинаю отправку блокированным пользователям по заготовке')
    for user in get_blocked_users():
        try:
            bot.send_message(wudmc_tg, f'отправляю сообщение юзеру {user.telegram_id}')
            bot.send_message(user.telegram_id, txts.msg_for_blocked, parse_mode='Markdown')
            bot.send_message(wudmc_tg, f' сообщение юзеру {user.telegram_id} успешно отправлено')
        except Exception:
            set_field(user.telegram_id, 'is_active', False)
            set_field(user.telegram_id, 'is_verified', False)
            bot.send_message(wudmc_tg, f' сообщение юзеру {user.telegram_id} не отправлено: {traceback.format_exc()}')
        sleep(2)
    bot.send_message(wudmc_tg, 'Сообщения блокированным отправлены')


def send_active_users():
    bot.send_message(wudmc_tg, 'Начинаю отправку авторизованным пользователям по заготовке')
    for user in get_verified_users():
        try:
            bot.send_message(wudmc_tg, f'отправляю сообщение юзеру {user.telegram_id}')
            bot.send_message(user.telegram_id, txts.msg_for_active, parse_mode='Markdown')
            bot.send_message(wudmc_tg, f' сообщение юзеру {user.telegram_id} успешно отправлено')
        except Exception:
            set_field(user.telegram_id, 'is_active', False)
            set_field(user.telegram_id, 'is_verified', False)
            bot.send_message(wudmc_tg, f' сообщение юзеру {user.telegram_id} не отправлено: {traceback.format_exc()}')
        sleep(2)
    bot.send_message(wudmc_tg, 'Сообщения авторизованным отправлены')


def send_stats():
    users_len = len(get_users())
    pairs_len = len(get_pairs())
    stats = (
        'Йо,йо , уже понедельник и вот немного статистики: \n'
        f'Всего участников: {users_len}\n'
        f'Пар на прошлой неделе:  {pairs_len}\n\n'
        f'а всего через 2 часа будут новые пары!\n'
        f'Проверь свой статус в профиле /help!\n'
    )

    bot.send_message(wudmc_tg, 'Отправляю статистики')
    for user in get_users():
        try:
            bot.send_message(wudmc_tg, f'отправляю стату юзеру {user.telegram_id}')
            bot.send_message(user.telegram_id, stats, parse_mode='Markdown')
            bot.send_message(wudmc_tg, f' стата юзеру {user.telegram_id} успешно отправлена')
        except Exception:
            bot.send_message(wudmc_tg, f' стату юзеру {user.telegram_id} не отправлено: {traceback.format_exc()}')
            set_field(user.telegram_id, 'is_active', False)
            set_field(user.telegram_id, 'is_verified', False)
            bot.send_message(wudmc_tg, f' юзер {user.telegram_id} отключен')
        sleep(2)
    bot.send_message(wudmc_tg, 'Статистика отправлена')


def help(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    pause_data = 'set_pause' if user.is_active else 'set_run'
    pause_txt = '⏸ Поставить на паузу' if user.is_active else '▶ Снять с паузы'
    location = str(user.location)
    next_state = States.complete
    keyboard = types.InlineKeyboardMarkup()
    profile_status = '' if is_user_fillevrth(user_id) else '🟥'
    if str(user.nickname)[1:] != str(message.from_user.username):
        nickname = str(message.from_user.username or 'Не указан')
        if nickname != 'Не указан':
            nickname = '@' + nickname
        set_field(user_id, 'nickname', nickname)
    flag = '🌎'
    for country, cities in country_map.items():
        if location in cities:
            flag = flag_map[country]
    keyboard.row_width = 1
    keyboard.add(
        types.InlineKeyboardButton(
            text='📌 Как все работает',
            callback_data='how_it_works'
        ),
        types.InlineKeyboardButton(
            text='👀Посмотреть свой профиль',
            callback_data='show_profile'
        ),
        types.InlineKeyboardButton(
            text=f'{profile_status}Поменять данные профиля{profile_status}',
            callback_data='change_profile'
        ),
        types.InlineKeyboardButton(
            text=f'{pause_txt}',
            callback_data=pause_data
        ),
        types.InlineKeyboardButton(
            text=f'{flag}󠁧󠁢󠁥 Локация: {location}',
            callback_data='change_location'
        ),
    )
    if user.nickname == 'Не указан':
        keyboard.add(
            types.InlineKeyboardButton(
                text='‼ALERT‼️Укажи НИК в TG',
                callback_data='update_nickname'
            )
        )
    if user.is_admin:
        keyboard.add(
            types.InlineKeyboardButton(
                text='Управление',
                callback_data='manage_users'
            ),
            types.InlineKeyboardButton(
                text='Рассылки',
                callback_data='sender'
            )
        )
    status = '🟩 Участвую в Random Coffee 🟩'
    if not user.is_active:
        status = '🟥 Не участвую в Random Coffee 🟥'

    help_txt = (f'*Статус на этой неделе:* {status}\n\n'
                'Поддержка по боту в чате Civilians Capital Chat\n\n'
                'Выбери подходящую опцию ниже')
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, help_txt,
                     reply_markup=keyboard, parse_mode='Markdown')
    bot.set_state(user_id, next_state)


# admin callbacks

@bot.message_handler(state=States.change_user_for_ask_id_admin)
def ask_nickname_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    telegram_id = message.text

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1

    user = get_user(telegram_id)
    if not user:
        answer = ('Не знаю такого пользователя')
    else:
        answer = (
            f'Настройки пользователя [{user.name}](tg://user?id={user.telegram_id})')
        keyboard.add(
            types.InlineKeyboardButton(
                text='Посмотреть профиль',
                callback_data=f'show_profile_for_admin_{user.telegram_id}'
            ),
            types.InlineKeyboardButton(
                text='Заблокировать',
                callback_data=f'refuse_{user.telegram_id}'
            ),
            types.InlineKeyboardButton(
                text='ЗАБАНИТЬ',
                callback_data=f'ban_{user.telegram_id}'
            ),
            types.InlineKeyboardButton(
                text='Поставить на паузу',
                callback_data=f'set_pause_for_admin_{user.telegram_id}'
            ),
            types.InlineKeyboardButton(
                text='Снять c паузы',
                callback_data=f'set_run_for_admin_{user.telegram_id}'
            )
        )

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_profile_for_admin_'))
def show_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    target_user_id = call.data[len('show_profile_for_admin_'):]
    answer = ('👉 Посмотреть профиль')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    user = get_user(target_user_id)
    answer = (
        f'Вот так будет выглядеть твой профиль для собеседника:\n\n'
        f'{user}'
    )

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help_from_show_profile'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('refuse_'))
def refuse__callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    target_user_id = call.data[len('refuse_'):]
    answer = ('👉 Убрать подтверждение')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    set_field(target_user_id, 'is_active', False)
    set_field(target_user_id, 'is_verified', False)
    try:
        bot.send_message(
            target_user_id, 'Ваш аккаунт заблокирован!\nДля повторной регистрации напишите /start')
    except Exception:
        bot.send_message(wudmc_tg,
                         f' сообщения юзеру {target_user_id} не отправлено: {traceback.format_exc()}')
    answer = ('Пользователь заблокирован')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('ban_'))
def ban_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    target_user_id = call.data[len('ban_'):]
    answer = ('👉 ЗАБАНИТЬ НАВСЕГДА')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    set_field(target_user_id, 'is_active', False)
    set_field(target_user_id, 'is_verified', False)
    set_field(target_user_id, 'ban', True)
    try:
        bot.send_message(
            target_user_id, 'Ауч! Вы забанены за нарушения правил!\nЕсли вы не согласны, напишите в чат поддержки')
    except Exception:
        bot.send_message(wudmc_tg,
                         f' сообщения юзеру {target_user_id} не отправлено: {traceback.format_exc()}')
    answer = ('Пользователь ЗАБАНЕН')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('set_pause_for_admin_'))
def set_pause_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    target_user_id = call.data[len('set_pause_for_admin_'):]
    answer = ('👉 Поставить на паузу')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    set_field(target_user_id, 'is_active', False)
    bot.send_message(target_user_id, 'Админ поставил тебя на паузу')
    answer = ('Пользователь на паузе')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('set_run_for_admin_'))
def set_run_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    target_user_id = call.data[len('set_run_for_admin_'):]
    answer = ('👉 Снять c паузы')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    set_field(target_user_id, 'is_active', True)
    answer = ('Пользователь запущен')
    bot.send_message(target_user_id, 'Админ включил тебя во встречи')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('feedback_'))
def feedback_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    pair_history_id = call.data.partition('_id_')[2]
    feedback_status = call.data.partition('_id_')[0][len('feedback_'):]
    bot.send_chat_action(user_id, 'typing')
    bot.delete_message(
        chat_id=user_id,
        message_id=message_id,
    )
    pair_history = get_pair_history(pair_history_id)

    field = 'test'
    if str(user_id) == str(pair_history[0].user_b):
        field = 'success_user_b'
        feedback_field = 'feedback_user_b'
        reported_user = pair_history[0].user_a
    elif str(user_id) == str(pair_history[0].user_a):
        field = 'success_user_a'
        feedback_field = 'feedback_user_a'
        reported_user = pair_history[0].user_b
    if feedback_status == 'yes':
        answer = (f'👍 Рад слышать, что все прошло как надо\n\n'
                  f'Оцени на сколько хорошо я подобрал тебе пару в этот раз? \n\n'
                  f'По возможности, поделись впечатлением об этой встрече в нашем чате')
        set_pair_history_field(pair_history_id, field, 1)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1
        keyboard.add(
            # types.InlineKeyboardButton(
            #     text='Оставить отзыв',
            #     callback_data='feedbacktxt_' + str(pair_history_id) + '_pair_' + 'userfeedback'
            # ),
            types.InlineKeyboardButton(
                text='⭐⭐⭐⭐⭐',
                callback_data='feedbacktxt_' + str(pair_history_id) + '_pair_' + 'star5'
            ),
            types.InlineKeyboardButton(
                text='⭐⭐⭐⭐',
                callback_data='feedbacktxt_' + str(pair_history_id) + '_pair_' + 'star4'
            ),
            types.InlineKeyboardButton(
                text='⭐⭐⭐',
                callback_data='feedbacktxt_' + str(pair_history_id) + '_pair_' + 'star3'
            ),
            types.InlineKeyboardButton(
                text='⭐⭐',
                callback_data='feedbacktxt_' + str(pair_history_id) + '_pair_' + 'star2'
            ),
            types.InlineKeyboardButton(
                text='⭐',
                callback_data='feedbacktxt_' + str(pair_history_id) + '_pair_' + 'star1'
            ),
            types.InlineKeyboardButton(
                text='Не хочу оставлять отзыв',
                callback_data='feedbacktxt_' + str(pair_history_id) + '_pair_' + 'dontwant'
            )
        )
        bot.send_chat_action(user_id, 'typing')
        bot.send_message(user_id, answer, parse_mode='Markdown',
                         reply_markup=keyboard)
    elif feedback_status == 'no':
        answer = (f'Мне очень жаль =(\n\n'
                  f' а собеседник отвечал?')
        set_pair_history_field(pair_history_id, field, 0)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1
        keyboard.add(
            types.InlineKeyboardButton(
                text='Отвечал, просто не получилось',
                callback_data='feedbacktxt_' + str(pair_history_id) + '_pair_' + 'nesroslos'
            ),
            types.InlineKeyboardButton(
                text='Собеседник мне не отетил',
                callback_data='feedbacktxt_' + str(pair_history_id) + '_pair_' + 'reportuser_' + str(reported_user)
            )
        )
        bot.send_chat_action(user_id, 'typing')
        bot.send_message(user_id, answer, parse_mode='Markdown',
                         reply_markup=keyboard)
    elif feedback_status == 'cancel':
        set_pair_history_field(pair_history_id, feedback_field, 'cancel')
        answer = (f'😎А твой отзыв надеюсь получу уже в следующий раз\n\n'
                  f'В понедельник будут назначены новые пары!\n'
                  f'Проверь, что в твоем профиле актуальная информация')
        bot.send_chat_action(user_id, 'typing')
        sleep(1)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text='ПРОФИЛЬ',
                callback_data='help'
            )
        )
        bot.send_message(user_id, answer, parse_mode='Markdown',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('feedbacktxt_'))
def feedbacktxt_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    pair_history_id = call.data.partition('_pair_')[0][len('feedbacktxt_'):]
    feedback_status = call.data.partition('_pair_')[2]
    answer = ('Уже почти всё...')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    pair_history = get_pair_history(pair_history_id)
    field = 'test'
    try:
        if str(user_id) == str(pair_history[0].user_b):
            field = 'feedback_user_b'
        elif str(user_id) == str(pair_history[0].user_a):
            field = 'feedback_user_a'
        if feedback_status == 'dontwant':
            set_pair_history_field(pair_history_id, field, 'dontwant')
            answer = (f'Спасибо , я запомню что ты не очень общительный 😂\n\n'
                      f'В понедельник будут назначены новые пары!\n'
                      f'Проверь, что в твоем профиле актуальная информация')

            keyboard = types.InlineKeyboardMarkup()

            keyboard.add(
                types.InlineKeyboardButton(
                    text='ПРОФИЛЬ',
                    callback_data='help'
                )
            )
            bot.send_chat_action(user_id, 'typing')
            bot.send_message(user_id, answer, reply_markup=keyboard)

        elif feedback_status == 'nesroslos':
            answer = (f'😢 Обязательно получится в следующий раз.\n\n'
                      f'В понедельник будут назначены новые пары!\n'
                      f'Проверь, что в твоем профиле актуальная информация')
            set_pair_history_field(pair_history_id, field, 'nesroslos')
            keyboard = types.InlineKeyboardMarkup()

            keyboard.add(
                types.InlineKeyboardButton(
                    text='ПРОФИЛЬ',
                    callback_data='help'
                )
            )
            bot.send_chat_action(user_id, 'typing')
            bot.send_message(user_id, answer, reply_markup=keyboard)
        elif feedback_status.startswith('star'):
            answer = (f'Спасибо за оценку, в следующий раз я учту это при подборе пары.\n\n'
                      f'В понедельник будут назначены новые пары!\n'
                      f'Проверь, что в твоем профиле актуальная информация')
            set_pair_history_field(pair_history_id, field, feedback_status[len('star'):])
            keyboard = types.InlineKeyboardMarkup()

            keyboard.add(
                types.InlineKeyboardButton(
                    text='ПРОФИЛЬ',
                    callback_data='help'
                )
            )
            bot.send_chat_action(user_id, 'typing')
            bot.send_message(user_id, answer, reply_markup=keyboard)
        # elif feedback_status == 'userfeedback':
        #     next_state = States.userfeedback
        #
        #     answer = (f'Оцени от 1 до 5 на сколько интересно было тебе')
        #
        #     set_field(user_id, 'temp', pair_history_id)
        #     set_pair_history_field(pair_history_id, field, 'userfeedback')
        #     bot.set_state(user_id, next_state)
        #     bot.send_chat_action(user_id, 'typing')
        #     bot.send_message(user_id, answer)

        else:
            answer = (f'😢 Вот негодяй, я отмечу у себя. Как только на него будет 3 жалобы - БАН.\n\n'
                      f'В понедельник будут назначены новые пары!\n'
                      f'Проверь, что в твоем профиле актуальная информация')
            keyboard = types.InlineKeyboardMarkup()

            keyboard.add(
                types.InlineKeyboardButton(
                    text='ПРОФИЛЬ',
                    callback_data='help'
                )
            )
            reported_user = feedback_status[len('reportuser_'):]

            set_pair_history_field(pair_history_id, field, 'bezotveta')
            set_field(reported_user, 'points', int(get_user(reported_user).points) + 1)
            bot.send_message(wudmc_tg,
                             f' у юзера {reported_user} points: {int(get_user(reported_user).points)}')
            bot.send_message(reported_user,
                             f' Ауч! Ты нарушил правила и не отвечал собеседнику, больше не делай так. \n Помни: 3 жалобы = бан. Жалоб сейчас: {int(get_user(reported_user).points)}')
            if get_user(reported_user).points > 2:
                set_field(reported_user, 'ban', True)
                set_field(reported_user, 'is_active', False)
                set_field(reported_user, 'is_verified', False)
                bot.send_message(reported_user,
                                 f' Ауч! Ты нарушил правила 3 раза. \n 😡 Ты забанен!')
            bot.send_chat_action(user_id, 'typing')
            bot.send_message(user_id, answer, reply_markup=keyboard)



    except Exception:
        bot.send_message(wudmc_tg,
                         f' ошибка: {traceback.format_exc()}')


@bot.callback_query_handler(func=lambda call: call.data == 'show_users')
def show_users_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    users = get_users()
    active_users = get_active_users()
    blocked_users = get_blocked_users()
    no_link_users = get_no_link_users()
    no_nickname_users = get_no_nickname_users()
    answer = (f'👉 Участники: {len(users)}')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    try:
        answer = (
            '\n'.join(
                [
                    f'[{user.telegram_id}](tg://user?id={user.telegram_id}) \- {__escape_markdown(user.nickname)} \- {"Verified" if user.is_verified else "Blocked"} \- {"Run" if user.is_active else "Pause"} \-  {(datetime.now() - user.created_at).days} days  \- '
                    for user in users])
        )
    except Exception:
        bot.send_message(wudmc_tg,
                         f' Список пользователенй не сформирован: {traceback.format_exc()}')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    answer_res = []
    for c in range(0, len(answer.splitlines()), 50):
        answer_res.append('\n'.join(answer.splitlines()[c: c + 50]))
    try:
        for user_txt in answer_res:
            bot.send_message(user_id, user_txt, parse_mode='MarkdownV2')

    except Exception:
        bot.send_message(wudmc_tg,
                         f' Список пользователенй не сформирован: {traceback.format_exc()}')
    bot.send_message(user_id,
                     f'активных {len(active_users)}, блокированых {len(blocked_users)}, без соц сети {len(no_link_users)}, без ника {len(no_nickname_users)}',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'change_user')
def change_user_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.change_user_for_ask_id_admin
    answer = ('👉 Настройки пользователя')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = 'Введи номер пользователя'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'show_pairs')
def show_pairs_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    answer = ('👉 Пары')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    pairs = get_pairs()
    if pairs:
        answer = (
            '\n'.join(
                [
                    f'[{get_user(pair.user_a).name}](tg://user?id={get_user(pair.user_a).telegram_id}) - [{get_user(pair.user_b).name}](tg://user?id={get_user(pair.user_b).telegram_id})' if pair.user_b != '' else f'[{get_user(pair.user_a).name}](tg://user?id={get_user(pair.user_a).telegram_id}) - None'
                    for pair in pairs]
            )
        )

    else:
        answer = 'Пар нету'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


def generate_pairs():
    all_active_users = get_users_by_loc()
    delete_pairs()

    for user_list in all_active_users:
        random.shuffle(user_list)
        pairs = [user_list[i:i + 2]
                 for i in range(0, len(user_list), 2)]
        for pair in pairs:
            if len(pair) == 2:
                create_pair(pair[0].telegram_id, pair[1].telegram_id, get_user_field(pair[0].telegram_id, 'location'))
            else:
                create_pair(pair[0].telegram_id, '', get_user_field(pair[0].telegram_id, 'location'))
    sleep(1)
    pairs_db = get_pairs()
    for pair in pairs_db:
        pair_history = create_pair_history(pair.id, pair.user_a, pair.user_b, pair.location)
        set_pair_field(pair.id, 'pair_history_id', pair_history.id)
        bot.send_message(wudmc_tg, pair_history.id)

    sleep(1)
    for user in get_verified_users():
        if user.is_active:
            try:
                bot.send_message(wudmc_tg,
                                 f'Отправляю сообщение юзеру {user.telegram_id} о назначении пары ')
                bot.send_message(user.telegram_id,
                                 'Ура! Пары назначены, скоро тебе придет сообщение с твоей парой на эту неделю')
            except Exception:
                set_field(user.telegram_id, 'is_active', False)
                set_field(user.telegram_id, 'is_verified', False)
                bot.send_message(wudmc_tg,
                                 f' Сообщение юзеру о назначении пары {user.telegram_id} не отправлено: {traceback.format_exc()}')
        else:
            try:
                bot.send_message(wudmc_tg,
                                 f'Отправляю сообщение юзеру {user.telegram_id} о назначении пары ')
                bot.send_message(user.telegram_id,
                                 'Пары назначены, но твой профиль был на паузе. Не упусти свой шанс на будущей неделе.')
            except Exception:
                set_field(user.telegram_id, 'is_active', False)
                set_field(user.telegram_id, 'is_verified', False)
                bot.send_message(wudmc_tg,
                                 f'Сообщение юзеру о назначении пары {user.telegram_id} не отправлено: {traceback.format_exc()}')
        sleep(1)


@bot.callback_query_handler(func=lambda call: call.data == 'generate_pairs')
def generate_pairs_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    answer = ('👉 Сгенерировать пары')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    generate_pairs()
    answer = (
        'Сгенерировал пары'
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


def no_info_users():
    # TODO: добавить напоминание пользователям заполнять профили.
    bot.send_message(wudmc_tg,
                     f'no_info_users')


def ask_about_next_week():
    for user in get_verified_users():
        try:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row_width = 1
            keyboard.add(
                types.InlineKeyboardButton(
                    text='Буду участвовать',
                    callback_data='set_run'
                ),
                types.InlineKeyboardButton(
                    text='Возьму перерыв',
                    callback_data='set_pause'
                )
            )
            bot.send_message(wudmc_tg,
                             f' отправля запрос участия  юзеру {user.telegram_id} ')

            if ((datetime.now() - user.created_at).days > 6) and user.is_active:
                set_field(user.telegram_id, 'is_active', False)
                bot.send_message(user.telegram_id, '[Ты со мной уже больше недели, поэтому я поставил твой профиль на паузу]')
            elif user.is_active:
                set_field(user.telegram_id, 'is_active', False)
                bot.send_message(user.telegram_id, '[Я поставил твой профиль на паузу, подтверди участие еще раз вручную пожалуйста]')
            bot.send_message(
                user.telegram_id, txts.next_week_txt, parse_mode='Markdown',
                reply_markup=keyboard)
            bot.send_message(wudmc_tg,
                             f' запрос участия  юзеру {user.telegram_id} успешно отправлен')
        except Exception:
            set_field(user.telegram_id, 'is_active', False)
            set_field(user.telegram_id, 'is_verified', False)
            bot.send_message(wudmc_tg,
                             f' запрос участия юзеру {user.telegram_id} не отправлен: {traceback.format_exc()}')
        sleep(1)
    bot.send_message(wudmc_tg,
                     f' запрос участия успешно отправлены')


def remind_inactive():
    for user in get_inactive_users():
        try:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row_width = 1
            keyboard.add(
                types.InlineKeyboardButton(
                    text='Конечно, участвую!',
                    callback_data='set_run'
                ),
                types.InlineKeyboardButton(
                    text='Не хочу участвовать',
                    callback_data='set_pause'
                )
            )
            bot.send_message(wudmc_tg,
                             f' отправляю напоминание  юзеру {user.telegram_id} ')
            bot.send_message(
                user.telegram_id, txts.reminder_for_inactive, parse_mode='Markdown',
                reply_markup=keyboard)
            bot.send_message(wudmc_tg,
                             f' напоминание юзеру {user.telegram_id} успешно отправлен')

        except Exception:
            set_field(user.telegram_id, 'is_active', False)
            set_field(user.telegram_id, 'is_verified', False)
            bot.send_message(wudmc_tg,
                             f' напоминания неактивному юзеру {user.telegram_id} не отправлен: {traceback.format_exc()}')
        sleep(1)
    bot.send_message(wudmc_tg,
                     f' напоминания неактивным юзерам успешно отправлены')


def ask_about_last_week():
    for pair in get_pairs():
        try:
            if pair.user_b:
                try:
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.row_width = 1
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text='Встреча состоялась',
                            callback_data='feedback_yes_id_' + str(pair.pair_history_id)
                        ),
                        types.InlineKeyboardButton(
                            text='Не состоялась',
                            callback_data='feedback_no_id_' + str(pair.pair_history_id)
                        ),
                        types.InlineKeyboardButton(
                            text='Не хочу отвечать',
                            callback_data='feedback_cancel_id_' + str(pair.pair_history_id)
                        )

                    )

                    bot.send_message(
                        pair.user_a, txts.poll_txt_1, parse_mode='Markdown', reply_markup=keyboard)
                    bot.send_message(wudmc_tg,
                                     f' запрос фидбека юзеру А {pair.user_a} успешно отправлено')


                except Exception:
                    set_field(pair.user_a, 'is_active', False)
                    set_field(pair.user_a, 'is_verified', False)
                    bot.send_message(wudmc_tg,
                                     f' запрос фидбека юзеру А {pair.user_b} НЕ отправлено: {traceback.format_exc()}')

                try:
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.row_width = 1
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text='Встреча состоялась',
                            callback_data='feedback_yes_id_' + str(pair.pair_history_id)
                        ),
                        types.InlineKeyboardButton(
                            text='Не состоялась',
                            callback_data='feedback_no_id_' + str(pair.pair_history_id)
                        ),
                        types.InlineKeyboardButton(
                            text='Не хочу отвечать',
                            callback_data='feedback_cancel_id_' + str(pair.pair_history_id)
                        )

                    )
                    bot.send_message(
                        pair.user_b, txts.poll_txt_1, parse_mode='Markdown', reply_markup=keyboard)
                    bot.send_message(wudmc_tg,
                                     f' запрос фидбека юзеру Б {pair.user_b} успешно отправлено')

                except Exception:
                    set_field(pair.user_b, 'is_active', False)
                    set_field(pair.user_b, 'is_verified', False)
                    bot.send_message(wudmc_tg,
                                     f' запрос фидбека юзеру Б {pair.user_b} НЕ отправлено: {traceback.format_exc()}')

            bot.send_message(wudmc_tg,
                             f' запрос фидбека паре {pair.id} успешно отправлено')
        except Exception:

            bot.send_message(wudmc_tg,
                             f' запрос фидбека паре {pair.id} не отправлен: {traceback.format_exc()}')


def send_invites():
    len_pairs = len(get_pairs())
    for pair in get_pairs():
        try:
            if pair.user_b:
                bot.send_message(

                    pair.user_a,
                    f'На этой неделе я познакомил {len_pairs} пар\n\nТвоя пара!\n\n{get_user(pair.user_b)}',
                    parse_mode='Markdown')

                bot.send_message(
                    pair.user_b,
                    f'На этой неделе я познакомил {len_pairs} пар\n\nТвоя пара!\n\n{get_user(pair.user_a)}',
                    parse_mode='Markdown')
            else:
                bot.send_message(
                    pair.user_a,
                    f'Привет!\n\nНа этой неделе пары не нашлось😞 Такое случается если количество участников не чётное.',
                    parse_mode='Markdown')
            bot.send_message(wudmc_tg,
                             f' сообщения паре {pair.id} успешно отправлено')
            set_pair_history_field(pair.pair_history_id, 'invited', True)
        except Exception:
            set_field(pair.user_a, 'is_active', False)
            set_field(pair.user_a, 'is_verified', False)
            bot.send_message(wudmc_tg,
                             f' сообщения паре {pair.id} не отправлено: {traceback.format_exc()}')


@bot.callback_query_handler(func=lambda call: call.data == 'send_to_nocontact')
def send_to_nocontact_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    send_no_contacts()
    answer = ('👉 Отправить заготовку  без контактов')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    answer = (
        'Напоминание пользователям без контактов прошло успешно'
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'send_to_blocked')
def send_to_blocked_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    send_blocked_users()
    answer = ('👉 Отправить заготовку  не верифицированным')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    answer = (
        'Напоминание пользователям без верификации прошло успешно'
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'send_to_active')
def send_to_active_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    send_active_users()
    answer = ('👉 Отправить заготовку верифицированным юзерам')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    answer = (
        'сообщение верифицированным пользователям прошло успешно'
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'send_to_admins')
def send_to_admins_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    send_admins()
    answer = ('👉 Отправить test админам')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    answer = (
        'Отправил test'
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'send_invites')
def send_invites_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    send_invites()
    answer = ('👉 Отправить приглашения')
    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    answer = (
        'Отправил приглашения'
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


# user commands


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    next_state = States.ask_password
    nickname = str(message.from_user.username or 'Не указан')
    if nickname != 'Не указан':
        nickname = '@' + nickname
    user = get_user(user_id)
    if user and user.ban:
        answer = ('BANNED')
    elif user and not user.is_verified and message.from_user.username in ADMINS:
        answer = ('Что то пошло не так, вернул тебя к жизни')
        set_field(user_id, 'is_verified', True)
        next_state = States.complete

    elif (not user or not user.is_verified) and message.from_user.username not in ADMINS:
        create_user(user_id)
        set_field(user_id, 'link', 'Не указана')
        set_field(user_id, 'nickname', nickname)
        set_field(user_id, 'name', 'Имя не указано')
        answer = ('Привет!🤩\n'
                  'Я Random Coffee бот 🤖  для Сivilians\n\n'
                  'Каждую неделю я буду предлагать '
                  'тебе для встречи интересного человека, '
                  'случайно выбранного среди '
                  'других участников🎲\n\n'
                  'Введи инвайт-код, чтобы продолжить\n\n'
                  'ПОДСКАЗКА - инвайт-код был в прикреплен в сообщении со ссылкой на меня\n'
                  'Или спроси в нашем чате в Civilians Capital Chat')


    elif not user and message.from_user.username in ADMINS:
        create_user(user_id)
        set_field(user_id, 'nickname', nickname)
        set_field(user_id, 'is_admin', True)
        set_field(user_id, 'is_verified', True)

        answer = ('Привет, админ!⭐\n\n'
                  'Как тебя зовут?☕️')
        next_state = States.ask_name
    else:
        answer = ('Рад тебя видеть!🔥\n'
                  'Твой профиль - /help\n'
                  'Обсуждение и вопросы по боту Civilians Capital Chat\n\n'
                  )
        next_state = States.complete

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown')
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.ask_password)
def ask_password_handler(message):
    user_id = message.from_user.id
    next_state = States.ask_name
    # тут закостылил админа  можно использовать get_admins() с циклом потом
    admin = wudmc_tg
    user = get_user(user_id)
    password = message.text
    if password in password_map.keys():
        try:
            answer_to_admin = (
                'Новый пользователь!\n'
                f'[{user.telegram_id}](tg://user?id={user.telegram_id})\n')
            bot.send_message(admin,
                             answer_to_admin, parse_mode='Markdown')

            answer = ('Ты в системе🌐\n\n'
                      'Как тебя зовут?☕️')
            set_field(user_id, 'password', password)
            set_field(user_id, 'is_verified', True)
        except Exception:
            bot.send_message(wudmc_tg,
                             f' сообщения юзеру {user.telegram_id} не отправлено: {traceback.format_exc()}')

    else:
        answer = ('Попробуй еще раз\n')
        next_state = States.ask_password
    bot.send_message(user_id, answer)
    bot.set_state(user_id, next_state)



@bot.message_handler(state=States.ask_name)
def ask_name_handler(message):
    user_id = message.from_user.id
    next_state = States.wait
    name = message.text
    set_field(user_id, 'name', name)
    answer = ('Рад познакомиться! \n\n'
              'Теперь выбери локацию для встреч, ты сможешь изменить ее в любое время.')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1

    keyboard.add(
        types.InlineKeyboardButton(
            text=f'Онлайн',
            callback_data='first_location_Online'
        )
    )
    for country in country_map.keys():
        keyboard.add(
            types.InlineKeyboardButton(
                text=f'{country}',
                callback_data=f'country_{country}'
            )
        )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data.startswith('country_'))
def change_location_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    action = 'first'
    if is_user_fillevrth(user_id):
        action = 'set'

    country = call.data[len('country_'):]
    bot.delete_message(
        chat_id=user_id,
        message_id=message_id
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    for city in country_map[country]:
        keyboard.add(
            types.InlineKeyboardButton(
                text=f'{city}',
                callback_data=f'{action}_location_{city}'
            )
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=f'Назад',
            callback_data='change_location'
            )
    )
    answer = ('Со станой разобрались, теперь выбери город \n\n'
              'Если твоего города нету, ты можешь участвовать 🌎 ОНЛАЙН \n'
              'Чтобы выбрать онлайн >>> нажми "Назад"')

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('first_location_'))
def change_location_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    location = call.data[len('first_location_'):]
    set_field(user_id, 'location', location)
    bot.delete_message(
        chat_id=user_id,
        message_id=message_id
    )

    answer = ('Отлично! Перед тем как твой профиль станет активным надо заполнить информацию о себе.'
              'Так вы в паре сможете лучше узнать '
              'друг о друге до встречи🔎\n\n'
              'Для начала пришли ссылку (или никнейм) на свой профиль '
              'в любой социальной сети. ')

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer)
    bot.set_state(user_id, States.ask_link)


# эту часть кода перенес в change_location handler
# @bot.message_handler(state=States.ask_location)
# def ask_location_handler(message):
#     user_id = message.from_user.id
#     next_state = States.ask_link
#
#
#     answer = ('Отлично! \n\n'
#               'Теперь пришли ссылку (или никнейм) на свой профиль '
#               'в любой социальной сети. '
#               'Так вы в паре сможете лучше узнать '
#               'друг о друге до встречи🔎')
#     nickname = str(message.from_user.username or 'Не указан')
#     if nickname == 'Не указан':
#         answer = ('Отлично!\n\n'
#
#                   'Теперь пришли ссылку (или никнейм) на свой профиль '
#                   'в любой социальной сети. '
#                   'Так вы в паре сможете лучше узнать '
#                   'друг о друге до встречи🔎\n\n'
#                   'ВАЖНО: У тебя не указан nickname в Telegram\n'
#                   'Обязательно укажи актуальную ссылку, иначе с тобой не получиться связаться'
#                   )
#
#
#     bot.send_chat_action(user_id, 'typing')
#     bot.send_message(user_id, answer)
#     bot.set_state(user_id, next_state)

@bot.message_handler(state=States.ask_link)
def ask_link_handler(message):
    user_id = message.from_user.id
    next_state = States.ask_work

    link = message.text

    answer = ('Так, ясно. 😎 А кем работаешь?✨\n\n'
              'Расскажи в двух словах о том как зарабатываешь на жизнь или о '
              'своих профессиональных увлечениях\n\n')

    set_field(user_id, 'link', link)

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer)
    bot.set_state(user_id, next_state)

@bot.message_handler(state=States.ask_work)
def ask_link_handler(message):
    user_id = message.from_user.id
    next_state = States.ask_about

    work = message.text

    answer = ('Уууу, вот это да!✨\n\n'
              'Остался последний шаг: \n'
              'Добавь зацепки для разговора, например, что то про свои хобби, '
              'увлечения или интересы.')

    set_field(user_id, 'work', work)

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer)
    bot.set_state(user_id, next_state)

@bot.message_handler(state=States.ask_about)
def ask_link_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    about = message.text

    answer = ('Отлично, все готово!\n\n'
              'Свою пару для встречи ты будешь узнавать'
              ' каждый понедельник в 12-00 — сообщение придет в этот чат\n\n'
              'Напиши партнеру в Telegram, '
              'чтобы договориться о встрече или звонке\n'
              'Время и место вы выбираете сами\n\n'
              'Изменить свой профиль тут - /help')

    set_field(user_id, 'about', about)

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer)
    bot.set_state(user_id, next_state)


@bot.message_handler(commands=['help'])
def help_handler(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user and user.is_verified:
        help(message)
    else:
        start_handler(message)


@bot.message_handler(state=States.change_name)
def change_name_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    name = message.text

    answer = 'Готово'

    set_field(user_id, 'name', name)

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)

#
# @bot.message_handler(state=States.userfeedback)
# def add_user_feedback(message):
#     user_id = message.from_user.id
#     next_state = States.complete
#
#     user_feedback = message.text
#     pair_history_id = get_user(user_id).about
#     pair_history = get_pair_history(pair_history_id)
#     field = 'test'
#
#     if str(user_id) == str(pair_history[0].user_b):
#         field = 'feedback_user_b'
#     elif str(user_id) == str(pair_history[0].user_a):
#         field = 'feedback_user_a'
#     answer = (f'Твой отзыв очень полезен\n\n'
#               f'В понедельник будут назначены новые пары!\n'
#               f'Проверь, что в твоем профиле актуальная информация')
#
#     set_pair_history_field(pair_history_id, field, user_feedback)
#     set_field(user_id, 'temp', 'None')
#     keyboard = types.InlineKeyboardMarkup()
#
#     keyboard.add(
#         types.InlineKeyboardButton(
#             text='ПРОФИЛЬ',
#             callback_data='help'
#         )
#     )
#     bot.send_chat_action(user_id, 'typing')
#     bot.send_message(user_id, answer, reply_markup=keyboard)
#     bot.set_state(user_id, next_state)


@bot.message_handler(state=States.change_link)
def change_link_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    link = message.text

    answer = 'Готово'

    set_field(user_id, 'link', link)

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.change_work)
def change_work_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    work = message.text

    answer = 'Готово'

    set_field(user_id, 'work', work)

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.change_about)
def change_about_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    about = message.text

    answer = 'Готово'

    set_field(user_id, 'about', about)

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)

#
# @bot.message_handler(state=States.update_nickname)
# def update_nickname_handler(message):
#     user_id = message.from_user.id
#     next_state = States.complete
#
#     nickname = str(message.from_user.username or 'Не указан')
#     if nickname != 'Не указан':
#         nickname = '@' + nickname
#
#     answer = 'Готово'
#
#     set_field(user_id, 'nickname', nickname)
#
#     keyboard = types.InlineKeyboardMarkup()
#
#     keyboard.add(
#         types.InlineKeyboardButton(
#             text='Назад',
#             callback_data='help'
#         )
#     )
#     bot.send_chat_action(user_id, 'typing')
#     bot.send_message(user_id, answer, reply_markup=keyboard)
#     bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'manage_users')
def manage_users_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.complete

    answer = ('👉 Меню управления')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Выбери пункт меню')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1

    keyboard.add(
        types.InlineKeyboardButton(
            text='Участники',
            callback_data='show_users'
        ),
        types.InlineKeyboardButton(
            text='Настройки пользователя',
            callback_data='change_user'
        ),
        types.InlineKeyboardButton(
            text='Пары',
            callback_data='show_pairs'
        ),
        types.InlineKeyboardButton(
            text='Сгенерировать пары',
            callback_data='generate_pairs'
        ),
        types.InlineKeyboardButton(
            text='Отправить приглашения',
            callback_data='send_invites'
        ),
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'sender')
def sender_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.complete

    answer = ('👉 Отправить рассылку')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Что хочешь отправить?')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1

    keyboard.add(
        types.InlineKeyboardButton(
            text='TEST',
            callback_data='test'
        ),
        # types.InlineKeyboardButton(
        #     text='Отправить админам заготовку',
        #     callback_data='send_to_admins'
        # ),
        # types.InlineKeyboardButton(
        #     text='Отправить безконтактным заготовку',
        #     callback_data='send_to_nocontact'
        # ),
        # types.InlineKeyboardButton(
        #     text='Отправить не подтверждённым заготовку',
        #     callback_data='send_to_blocked'
        # ),
        # types.InlineKeyboardButton(
        #     text='Отправить верифицированным заготовку',
        #     callback_data='send_to_active'
        # ),
        types.InlineKeyboardButton(
            text='Отправить свое сообщение всем ',
            callback_data='send_to_all'
        ),
        types.InlineKeyboardButton(
            text='Отправить свое сообщение юзеру по айди',
            callback_data='send_to_user_id'
        ),
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'test')
def test_handler(call):
    try:
        # ask_about_last_week()
        bot.send_message(wudmc_tg, 'test')
    except Exception:
        bot.send_message(wudmc_tg, f' ошибка: {traceback.format_exc()}')


@bot.callback_query_handler(func=lambda call: call.data == 'send_to_all')
def send_to_all_handler(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.send_message_to_all_users
    answer = ('👉 Отправка сообщения всем юзерам')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = 'Напиши GO, чтобы продолжить'

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)

@bot.callback_query_handler(func=lambda call: call.data == 'send_to_user_id')
def send_to_user_handler(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.send_message_to_user_id

    answer = ('👉 Отправка сообщения юзеру по айди')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = 'Введи номер пользователя'

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.send_message_to_user_id)
def send_message_to_user_id_handler(message):
    user_id = message.from_user.id
    next_state = States.forward_message
    telegram_id = message.text
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    user = get_user(telegram_id)
    global forward_users
    forward_users = []
    forward_users.append(user)
    if not user:
        answer = ('Не знаю такого пользователя')
    else:
        answer = (
            f'Отправить сообщение [{user.name}](tg://user?id={user.telegram_id})')

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.send_message_to_all_users)
def send_message_to_all_users(message):
    user_id = message.from_user.id
    next_state = States.forward_message

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    global forward_users
    forward_users = get_verified_users()

    answer = (
        f'Введи сообщение которое отправится всем пользователям')

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.forward_message)
def send_to_user_msg_callback(message):
    user_id = message.from_user.id
    message = message.text
    # photo = message.photo[-1]
    next_state = States.complete

    for target_user in forward_users:
        target_user_id = target_user.telegram_id
        answer = (f'👉 Отправляю сообщение пользователю {target_user_id}')
        bot.send_message(wudmc_tg, answer)

        try:
            bot.send_message(
                target_user_id, message)
            # bot.send_photo(
            #     target_user_id, photo, caption=message)
        except Exception:
            set_field(target_user_id, 'is_active', False)
            set_field(target_user_id, 'is_verified', False)
            bot.send_message(wudmc_tg,
                             f' сообщения юзеру {target_user_id} не отправлено: {traceback.format_exc()}')

    answer = ('Done')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.set_state(user_id, next_state)


# user callbacks


@bot.callback_query_handler(func=lambda call: call.data in ['help', 'help_from_show_profile', 'help_from_how_txt'])
def change_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    answer = call.message.text
    # print(answer)

    if call.data == 'help_from_show_profile':
        user = get_user(user_id)
        answer = (
            f'*Твоя локация на этой неделе:* {user.location}\n\n'
            'Вот так будет выглядеть твой профиль для собеседника:\n\n'
            f'{user}'
        )

    bot.send_chat_action(user_id, 'typing')
    if call.data == 'help_from_how_txt':
        bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=answer
        )
    else:
        bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=answer,
            parse_mode='Markdown'
        )

    help(call)


@bot.callback_query_handler(func=lambda call: call.data == 'how_it_works')
def how_it_works_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    answer = ('👉 Все очень просто')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer,
        parse_mode='Markdown'
    )
    answer = txts.how_txt

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help_from_how_txt'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'show_profile')
def show_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    answer = ('👉 Хочу посмотреть свой профиль')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )
    user = get_user(user_id)
    answer = (
        f'*Твоя локация на этой неделе:* {user.location}\n\n'
        'Вот так будет выглядеть твой профиль для собеседника:\n\n'
        f'{user}\n\n'
    )

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help_from_show_profile'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'change_name')
def change_name_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.change_name

    answer = ('👉 Своё имя')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Введи свое имя')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'change_link')
def change_link_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.change_link

    answer = ('👉 Ссылку (или никнейм) на социальную сеть')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Введи новую ссылку')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'change_work')
def change_work_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.change_work

    answer = ('👉 Кем работаю')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Напиши, чем ты занимаешься по работе')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'change_about')
def change_about_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.change_about

    answer = ('👉 О себе')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Напиши  новое описание:'
              ' пара предложений о твоих профессиональных'
              ' интересах, взглядах, хобби')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'update_nickname')
def update_nickname_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    # next_state = States.update_nickname
    nickname = str(call.message.chat.username or 'Не указан')
    if nickname != 'Не указан':
        nickname = '@' + nickname

    set_field(user_id, 'nickname', nickname)
    nickname_db = get_user(user_id).nickname
    nick = f'🟥{nickname_db}🟥' if nickname_db == 'Не указан' else nickname_db
    answer = ('👉 Обновить Имя пользователя\n'
              f'Твой никнейм сейчас {nick}')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Чтобы обновить никнейм зайди в настройки:'
              ' Изменить профиль >> Имя пользователя.\n'
              ' После изменения нажми "Обновить"')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Обновить',
            callback_data='update_nickname'
        ),
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    # bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'change_profile')
def change_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.complete

    answer = ('👉 Поменять данные профиля')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Что хочешь поменять?')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    link_status = '⬅️Не заполнено🟥' if get_user_field(user_id, 'link') == '' else ''
    work_status = '⬅️Не заполнено🟥' if get_user_field(user_id, 'work') == '' else ''
    about_status = '⬅️Не заполнено🟥' if get_user_field(user_id, 'about') == '' else ''
    nick_status = '⬅️Не Указан🟥' if get_user_field(user_id, 'nickname') == 'Не указан' else ''
    keyboard.add(
        types.InlineKeyboardButton(
            text='Своё имя',
            callback_data='change_name'
        ),
        # types.InlineKeyboardButton(
        #     text='Интересы',
        #     callback_data='change_interests'
        # ),
        types.InlineKeyboardButton(
            text= f'Ссылку на социальную сеть {link_status}',
            callback_data='change_link'
        ),
        types.InlineKeyboardButton(
            text=f'Кем работаю {work_status}',
            callback_data='change_work'
        ),
        types.InlineKeyboardButton(
            text=f'О себе {about_status}',
            callback_data='change_about'
        ),
        types.InlineKeyboardButton(
            text=f'Обновить Никнейм {nick_status}',
            callback_data='update_nickname'
        ),
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data.startswith('set_location_'))
def set_location_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    location = call.data[len('set_location_'):]
    set_field(user_id, 'location', location)

    answer = f'Ты изменил локацию на {location}'
    bot.delete_message(
                        chat_id=user_id,
                        message_id=message_id
                      )

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer)
    help(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_location'))
def change_location_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    answer = 'Выбери локацию для встречи и нажми "ГОТОВО"'
    bot.send_chat_action(user_id, 'typing')
    bot.delete_message(
                        chat_id=user_id,
                        message_id=message_id
                      )
    location_value = get_user_field(user_id, 'location')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 2

    keyboard.add(
        types.InlineKeyboardButton(
            text=f'Онлайн',
            callback_data='set_location_Online'
        )
    )
    for country in country_map.keys():
        if location_value in country_map[country]:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=f'✅{country}: {location_value}',
                    callback_data=f'country_{country}'
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=f'{country}',
                    callback_data=f'country_{country}'
                )
            )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data == 'set_pause')
def set_pause_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    answer = ('👉 Поставить на паузу')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = 'Готово'

    set_field(user_id, 'is_active', False)

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'set_run')
def set_run_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    user = get_user(user_id)
    if user.link != '' and user.work != '' and user.about != '':
        answer = '👉 Снять с паузы'

        bot.send_chat_action(user_id, 'typing')
        bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=answer
        )
        answer = 'Готово'
        set_field(user_id, 'is_active', True)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text='Назад',
                callback_data='help'
            )
        )

    else:
        answer = (' 🟥 Я не могу снять с паузы твой профиль, он еще не до конца заполнен  🟥\n\n'
                  '👇👇👇Проверь, что у тебя заполнены все разделы профиля и попробуй еще раз')
        bot.delete_message(
            chat_id=user_id,
            message_id=message_id
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text='Меню',
                callback_data='help'
            )
        )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)


# хрен знает что это


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())


def schedule_checker():
    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except Exception as e:
        print(e)
        bot.send_message(wudmc_tg, f' ошибка расписания {traceback.format_exc()} или {e}')


if __name__ == "__main__":
    schedule.every().monday.at('10:20').do(send_stats)
    schedule.every().monday.at('10:40').do(generate_pairs)
    schedule.every().monday.at('12:00').do(send_invites)
    schedule.every().wednesday.at('17:30').do(send_blocked_users)
    schedule.every().saturday.at('14:05').do(ask_about_next_week)
    schedule.every().sunday.at('14:30').do(ask_about_last_week)
    schedule.every().sunday.at('19:42').do(remind_inactive)
    Thread(target=schedule_checker).start()

    bot.infinity_polling()
    # bot.polling()
