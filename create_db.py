from flask import Flask
from models import User, Price_Bez, Abonement, Сertificate, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print('Создана база данных')