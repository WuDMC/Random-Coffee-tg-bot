import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine, create_engine

default_pass = 'bebrip33'

Base = declarative_base()
engine = create_engine('sqlite:///data/db.db?check_same_thread=False')


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, nullable=False)
    nickname = Column(String, default='', nullable=True)
    name = Column(String, default='', nullable=False)
    link = Column(String, default='', nullable=False)
    work = Column(String, default='', nullable=False)
    about = Column(String, default='', nullable=False)
    password = Column(String, default=default_pass, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    ban = Column(Boolean, default=False, nullable=False)
    points = Column(Integer, default=0, nullable=False)
    temp = Column(String, default='', nullable=False)
    location = Column(String, default='', nullable=False)

    def __repr__(self):
        # проблема с маркдаун только решает никнеймы
        __escape_markdown_map = {

            "_": "\\_",  # underscore

        }

        def __escape_markdown(raw_string):
            s = raw_string
            for k in __escape_markdown_map:
                s = s.replace(k, __escape_markdown_map[k])
            return s

        # states
        return (f'{self.name}\n'
                f'*Соц. сеть:* {__escape_markdown(self.link)}\n\n'
                f'*Чем занимается:* {self.work}\n'
                f'*Зацепки для начала разговора:* {self.about}\n\n'
                f'Напиши собеседнику в Telegram – [{self.name}](tg://user?id={self.telegram_id})\n\n'
                f'*Никнейм в тг* {__escape_markdown(self.nickname)}\n\n')

    def __getitem__(self, field):
        return self.__dict__[field]


class Pair(Base):
    __tablename__ = 'pair'

    id = Column(Integer, primary_key=True)
    user_a = Column(String, nullable=False)
    user_b = Column(String, nullable=False)
    location = Column(String, default='', nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    pair_history_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f'<Pair {self.id}; User A {self.user_a} - User B {self.user_b}>'


class Pair_History(Base):
    __tablename__ = 'Pair_History'

    id = Column(Integer, primary_key=True)
    pair_id =Column(Integer, nullable=False)
    user_a = Column(String, nullable=False)
    user_b = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.now)
    invited = Column(Boolean, nullable=True)
    feedback_user_a = Column(Integer, nullable=True)
    feedback_user_b = Column(Integer, nullable=True)
    success_user_a = Column(Boolean, nullable=True)
    success_user_b = Column(Boolean, nullable=True)



Base.metadata.create_all(engine)
