from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Helios import db
# db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    user = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    pswd = db.Column(db.String(64))
    pkey = db.Column(db.PickleType)
    skey = db.Column(db.PickleType)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:%s' % self.name

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, index=True)
    descrip = db.Column(db.Text,index=True)
    is_pri = db.Column(db.Boolean)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    admin_user = db.Column(db.String(64))
    admin_pkey = db.Column(db.PickleType)
    complete = db.Column(db.Boolean)
    finish = db.Column(db.Boolean)
    audit = db.Column(db.Boolean)
    email_list = db.relationship('Email_list',backref='vote')
    questions = db.relationship('Question',backref='vote')
    ballot = db.relationship('Ballot',backref='vote')


class Email_list(db.Model):
    __tablename__='email_list'
    id = db.Column(db.Integer, primary_key=True)
    email_add=db.Column(db.String(64))
    vote_id = db.Column(db.Integer, db.ForeignKey('votes.id'))

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text)
    options = db.Column(db.PickleType)
    options_num = db.Column(db.Integer)
    vote_id = db.Column(db.Integer, db.ForeignKey('votes.id'))

class Ballot(db.Model):
    __tablename__ = 'ballots'
    id = db.Column(db.Integer, primary_key=True)
    cipher = db.Column(db.PickleType)
    hash = db.Column(db.PickleType)
    is_valid = db.Column(db.Boolean)
    email = db.Column(db.String(64))
    vote_id = db.Column(db.Integer, db.ForeignKey('votes.id'))

class Shuffle(db.Model):
    __tablename__ = 'shuffle'
    id = db.Column(db.Integer, primary_key=True)
    ballot = db.Column(db.PickleType)
    result = db.Column(db.PickleType)
    vote_id = db.Column(db.Integer, db.ForeignKey('votes.id'))

db.create_all()
db.session.commit()