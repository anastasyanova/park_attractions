from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    points = db.Column(db.Integer, default = 0)
    role = db.Column(db.String(20), default='user')

    def __repr__(self):
        return f'<User {self.username}>' 
    
class Price_Bez(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    period = db.Column(db.Integer, nullable=False)
    off_tickets = db.Column(db.Integer, nullable=False)
    onn_tickets = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.name

class Abonement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    one_tickets = db.Column(db.Integer, nullable=False)
    onn_tickets = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.name
    
class Сertificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    period = db.Column(db.Integer, nullable=False)
    tickets = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.name