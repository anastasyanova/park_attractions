from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Price_Bez, Abonement, Сertificate, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import io
import os
import qrcode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin = Admin(app, name='Панель администратора', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Price_Bez, db.session))
admin.add_view(ModelView(Abonement, db.session))
admin.add_view(ModelView(Сertificate, db.session))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль')
    return render_template('login.html')

users = {}

UPLOAD_FOLDER = 'static/qr_codes'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user = User.query.filter_by(username=username).first()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(username)
        qr.make(fit=True)
        
        # Сохраняем QR-код в папку
        qrcode_filename = f'{username}.png'
        qrcode_path = os.path.join(UPLOAD_FOLDER, qrcode_filename)
        qr.make_image(fill_color="black", back_color="white").save(qrcode_path)
        
        # Добавляем пользователя в список
        users[username] = qrcode_filename

        if user:
            flash('Имя пользователя уже занято')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', user=current_user)
    else:
        return redirect(url_for('login'))

#Аттракционы
@app.route('/attraction/attractions')
def attractions():
    if current_user.is_authenticated:
        return render_template('/attraction/attractions.html', user=current_user)
    else:
        return redirect(url_for('login'))

#Тематические парки
@app.route('/temparks/temparks')
def temparks():
    if current_user.is_authenticated:
        return render_template('/temparks/temparks.html', user=current_user)
    else:
        return redirect(url_for('login'))

#Мероприятия
@app.route('/meropriyatia/meropriyatia')
def meropriyatia():
    if current_user.is_authenticated:
        return render_template('/meropriyatia/meropriyatia.html', user=current_user)
    else:
        return redirect(url_for('login'))    

#Цены
@app.route('/prices/price')
def price():
    if current_user.is_authenticated:
        prices = Price_Bez.query.all()
        abons = Abonement.query.all()
        certif = Сertificate.query.all()
        return render_template('/prices/price.html', user=current_user, prices=prices, abons=abons, certif=certif)
    else:
        return redirect(url_for('login'))
    
@app.route('/price_add', methods=['GET', 'POST'])
def price_add():
    if request.method == 'POST':
        name = request.form['name']
        period = request.form['period']
        off_tickets = request.form['off_tickets']
        onn_tickets = request.form['onn_tickets']

        prices = Price_Bez(name=name, period=period, off_tickets=off_tickets, onn_tickets=onn_tickets)

        db.session.add(prices)
        db.session.commit()
        return redirect('/prices/price')
    return render_template('/prices/price_add.html')

@app.route('/abon_add', methods=['GET', 'POST'])
def abon_add():
    if request.method == 'POST':
        name = request.form['name']
        number_of_tickets = request.form['number_of_tickets']
        period = request.form['period']
        one_tickets = request.form['one_tickets']
        onn_tickets = request.form['onn_tickets']
        
        abons = Abonement(name=name, number_of_tickets=number_of_tickets, period=period, one_tickets=one_tickets, onn_tickets=onn_tickets)

        db.session.add(abons)
        db.session.commit()
        return redirect('/prices/price')
    return render_template('/prices/abon_add.html')

@app.route('/certificate_add', methods=['GET', 'POST'])
def certificate_add():
    if request.method == 'POST':
        name = request.form['name']
        period = request.form['period']
        tickets = request.form['tickets']
        
        certif = Сertificate(name=name, period=period, tickets=tickets)

        db.session.add(certif)
        db.session.commit()
        return redirect('/prices/price')
    return render_template('/prices/certificate_add.html')

@app.route('/price/<int:id>/del')
def certificate_delete(id):
    certif = Сertificate.query.get_or_404(id)

    try:
            db.session.delete(certif)
            db.session.commit()
            return redirect('/prices/price')
    except:
            return "При удалении возникла ошибка"

@app.route('/price/<int:id>/del')
def abon_delete(id):
    abons = Abonement.query.get_or_404(id)

    try:
            db.session.delete(abons)
            db.session.commit()
            return redirect('/prices/price')
    except:
            return "При удалении возникла ошибка"

@app.route('/price/<int:id>/del')
def price_delete(id):
    prices = Price_Bez.query.get_or_404(id)

    try:
            db.session.delete(prices)
            db.session.commit()
            return redirect('/prices/price')
    except:
            return "При удалении возникла ошибка"

#Профиль
@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        qrcode_path = os.path.join(UPLOAD_FOLDER, f'{user.username}.png')
        return render_template('/profile.html', user=current_user, qrcode_path =qrcode_path)
    else:
        return redirect(url_for('login'))
    
@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

#Корзина
@app.route('/cart/cart')
def cart():
    if current_user.is_authenticated:
        return render_template('/cart/cart.html', user=current_user)
    else:
        return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    logout_user()
    session.pop('qr_code', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)