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
    description = db.Column(db.String(15), nullable=False)
    descriptions = db.Column(db.String(100), nullable=False)
    view = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.name
    
class Park(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    height = db.Column(db.String(3), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(15), nullable=False)
    descriptions = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.name
    
class Price_Bez(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    period = db.Column(db.Integer, nullable=False)
    off_tickets = db.Column(db.Integer, nullable=False)
    onn_tickets = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.name
    
class Abonement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    one_tickets = db.Column(db.Integer, nullable=False)
    onn_tickets = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.name
    
class Сertificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    period = db.Column(db.Integer, nullable=False)
    tickets = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.name
    
class Promo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    conditions = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return self.name