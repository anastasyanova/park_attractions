from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>' 
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    height = db.Column(db.String(3), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(15), default=True)
    descriptions = db.Column(db.String(100), default=True)
    view = db.Column(db.String(30), default=True)

    def __repr__(self):
        return self.name
    
class Park(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    height = db.Column(db.String(3), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(15), default=True)
    descriptions = db.Column(db.String(100), default=True)

    def __repr__(self):
        return self.name