from Config.BASE.exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    portrait = db.Column(db.BLOB(length=52428800), nullable=False)


class CommunityModel(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)

    create_time = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(UserModel, backref='cmtys')

    picture_1 = db.Column(db.BLOB(length=52428800), nullable=True)
    picture_2 = db.Column(db.BLOB(length=52428800), nullable=True)
    picture_3 = db.Column(db.BLOB(length=52428800), nullable=True)
    picture_4 = db.Column(db.BLOB(length=52428800), nullable=True)
    picture_5 = db.Column(db.BLOB(length=52428800), nullable=True)
    picture_6 = db.Column(db.BLOB(length=52428800), nullable=True)
    picture_7 = db.Column(db.BLOB(length=52428800), nullable=True)
    picture_8 = db.Column(db.BLOB(length=52428800), nullable=True)
    picture_9 = db.Column(db.BLOB(length=52428800), nullable=True)


class ChatMessageModel(db.Model):
    __tablename__ = 'chat_massage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    sender = db.relationship(UserModel, backref='message_sender', foreign_keys=[sender_id])
    receiver = db.relationship(UserModel, backref='message_receiver', foreign_keys=[receiver_id])


class MemoModel(db.Model):
    __tablename__ = 'memo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    target_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship(UserModel, backref='memos')