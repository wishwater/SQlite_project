from flask import Flask

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///K:\\Nikita\\SQlite\\SQlite_project\\test_db.db"
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80))


    def __init__(self, username, nickname):
        self.username = username
        self.nickname = nickname

    def __repr__(self):
        return '<User %r>' % self.nickname

@app.route('/')
def home():
    return('ok')

if __name__ == "__main__":
    app.run(port = '8000')
