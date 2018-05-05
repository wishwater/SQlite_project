# -*- coding:utf-8 -*-
from flask import Flask,redirect, url_for

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///K:\\Nikita\\SQlite\\trash\\my_db.db"
db = SQLAlchemy(app)

from datetime import datetime, timedelta
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from schematics.models import Model
from schematics.types import StringType, EmailType, BooleanType, IntType, ListType, ModelType, DateTimeType
from datetime import datetime

class Unprocessed(db.Model):
    __tablename__ = 'unprocessed'
    id = db.Column(db.Integer, primary_key=True)
    city_country = db.Column(db.String(80))
    c_min = db.Column(db.Integer)
    c_max = db.Column(db.Integer)
    c_current = db.Column(db.Integer)
    status = db.Column(db.Integer)
    wind = db.Column(db.Integer)
    site = db.Column(db.String(80))
    time = db.Column(db.DateTime(timezone=True), default=db.func.now())
    user = db.Column(db.String(80))

    def __init__(self, id, city_country , c_min , c_max  , c_current ,  status , wind , site , time , user  ):
        self.id = id
        self.city_country = city_country
        self.c_min = c_min
        self.c_max = c_max
        self.c_current = c_current
        self.status = status
        self.wind = wind
        self.site = site
        self.time = time
        self.user = user

class Processed(db.Model):
    __tablename__ = 'processed'
    id = db.Column(db.Integer, primary_key=True)
    city_country = db.Column(db.String(80))
    c_min = db.Column(db.Integer)
    c_max = db.Column(db.Integer)
    c_current = db.Column(db.Integer )
    status = db.Column(db.Integer)
    wind = db.Column(db.Integer)
    time = db.Column(db.DateTime(timezone=True), default=db.func.now())
    user = db.Column(db.String(80))

    def __init__(self, id, city_country , c_min , c_max  , c_current ,  status , wind , time , user  ):
        self.id = id
        self.city_country = city_country
        self.c_min = c_min
        self.c_max = c_max
        self.c_current = c_current
        self.status = status
        self.wind = wind
        self.time = time
        self.user = user

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80))
    user_tag = db.Column(db.String(80))
    locations = db.Column(db.Integer)

    def as_dict(self):
     return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, id, nickname , user_tag , locations):
        self.id = id
        self.nickname = nickname
        self.user_tag = user_tag
        self.locations = locations

class SqliteSequence(db.Model):
    __tablename__ = 'SqlSequence'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    seq = db.Column(db.String(80))

    def __init__(self, id, name, seq):
        self.id = id
        self.name = name
        self.seq = seq

@app.route('/')
def home():
    result1 = User.query.filter_by(nickname = 'Frau Merkel').all()
    print(result1)
    print(type(result1))

    return('ok')

@app.route('/def/<nickname>')
def find(nickname):
    result = User.query.filter_by(nickname = nickname)
    print(type(result))
    if isinstance(result,list):
        for i in result:
            print('first_print')
            return redirect(url_for('as_dict'))
    else:
        print('second_print')
        return redirect(url_for('as_dict'))
    return('okei')

def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

if __name__ == '__main__':
    app.run(debug=True, port=2228)
