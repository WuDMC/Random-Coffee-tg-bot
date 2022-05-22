import logging
from re import L
from sqlalchemy.orm import sessionmaker

from models import User, Pair, Pair_History, engine
from messages import generate_password

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

session = sessionmaker(engine)()


def get_user(user_id):
    user = (
        session.query(
            User
        )
        .filter(
            User.telegram_id == user_id,
        )
        .first()
    )
    return user if user else None

def is_user_fillevrth(user_id):
    user = (
        session.query(
            User
        )
        .filter(
            User.telegram_id == user_id,
        )
        .first()
    )
    return True if (user.link != '' and user.about != '' and user.work != '') else False

def get_user_field(user_id, field):
    user = (
        session.query(
            User
        )
        .filter(
            User.telegram_id == user_id,
        )
        .first()
    )
    return user[field] if user else 'None'


def get_admins():
    admins = (
        session.query(
            User
        )
        .filter(
            User.is_admin == True,
        )
        .all()
    )
    return admins if admins else []


def get_users():
    users = (
        session.query(
            User
        )
        .filter(
            User.ban == False

        )
        .all()
    )
    return users if users else []

def get_ban_users():
    users = (
        session.query(
            User
        )
        .filter(
            User.ban == True

        )
        .all()
    )
    return users if users else []


def get_blocked_users():
    users = (
        session.query(
            User
        )
        .filter(
            User.is_verified == False,
            User.ban == False

        )
        .all()
    )
    return users if users else []

def get_verified_users():
    users = (
        session.query(
            User
        )
        .filter(
            User.is_verified == True,
            User.ban == False
        )
        .all()
    )
    return users if users else []

def get_active_users():
    users = (
        session.query(
            User
        )
        .filter(
            User.is_active == True,
            User.is_verified == True,
            User.ban == False
        )
        .all()
    )
    return users if users else []

def get_users_by_loc():
  locs = [r.location for r in session.query(User.location).distinct()]
  users = []
  for loc in locs:
        users_loc = (
        session.query(
            User
        )
        .filter(
            User.is_active == True,
            User.is_verified == True,
            User.ban == False,
            User.location == loc
        )
        .all()
        )
        users.append(users_loc)

  return users if users else []

def get_active_online():
    users = (
        session.query(
            User
        )
        .filter(
            User.is_active == True,
            User.is_verified == True,
            User.ban == False,
            User.location == 'Online'
        )
        .all()
    )
    return users if users else []





def get_inactive_users():
    users = (
        session.query(
            User
        )
        .filter(
            User.is_active == False,
            User.is_verified == True,
            User.ban == False
        )
        .all()
    )
    return users if users else []

def get_no_nickname_users():
    users = (
        session.query(
            User
        )
        .filter(
            User.is_active == True,
            User.is_verified == True,
            User.ban == False,
            User.nickname == 'Не указан'
        )
        .all()
    )
    return users if users else []



def get_no_link_users():
    users = (
        session.query(
            User
        )
        .filter(
            User.is_active == True,
            User.is_verified == True,
            User.ban == False,
            User.link == 'Не указана'
        )
        .all()
    )
    return users if users else []


def create_user(user_id):
    if not get_user(user_id):
        session.add(User(
            nickname='Не указан',
            telegram_id=user_id,
            password=generate_password(),

        ))
        session.commit()


def set_field(user_id, key, value):
    (
        session.query(
            User
        )
        .filter(
            User.telegram_id == user_id,
        )
        .update(
            {key: value}
        )
    )
    session.commit()


def set_pair_field(pair_id, key, value):
    (
        session.query(
            Pair
        )
        .filter(
            Pair.id == pair_id,
        )
        .update(
            {key: value}
        )
    )
    session.commit()


def set_pair_history_field(pair_history_id, key, value):
    (
        session.query(
            Pair_History
        )
        .filter(
            Pair_History.id == pair_history_id,
        )
        .update(
            {key: value}
        )
    )
    session.commit()


def create_pair(user_id_a, user_id_b):
    session.add(Pair(
        user_a=user_id_a,
        user_b=user_id_b,
    ))
    session.commit()


def create_pair_history(id, user_id_a, user_id_b):
    pair = Pair_History(
        pair_id=id,
        user_a=user_id_a,
        user_b=user_id_b,
    )
    session.add(pair)
    session.commit()
    session.flush()
    return pair if pair else 'test'

def get_pair_history(id):
    pairs = (
        session.query(
            Pair_History
        )
        .filter(
            Pair_History.id == id,
        )
        .all()
    )
    return pairs if pairs else []


def delete_pairs():
    session.query(Pair).delete()


def get_pairs():
    pairs = (
        session.query(
            Pair
        )
        .all()
    )
    return pairs if pairs else []


