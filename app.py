from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Item, Park, Price_Bez, Abonement, Сertificate, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

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

admin = Admin(app, name='Панель администратора')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Park, db.session))
admin.add_view(ModelView(Price_Bez, db.session))
admin.add_view(ModelView(Abonement, db.session))
admin.add_view(ModelView(Сertificate, db.session))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Неверное имя пользователя или пароль')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Имя пользователя уже занято')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
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
        items = Item.query.order_by(Item.price).all()
        return render_template('/attraction/attractions.html', user=current_user, items=items)
    else:
        return redirect(url_for('login'))
     
@app.route('/attractions/<int:id>')
def attractions_detail(id):
    items = Item.query.get(id)
    return render_template('/attraction/attractions_detail.html', user=current_user, items=items)

#Тематические парки
@app.route('/temparks/temparks')
def temparks():
    if current_user.is_authenticated:
        parks = Park.query.order_by(Park.price).all()
        return render_template('/temparks/temparks.html', user=current_user, parks=parks)
    else:
        return redirect(url_for('login'))
    
@app.route('/temparks/<int:id>')
def temparks_detail(id):
    parks = Park.query.get(id)
    return render_template('/temparks/temparks_detail.html', user=current_user, parks=parks)

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

#Мероприятия
@app.route('/promo/promotions')
def promo():
    if current_user.is_authenticated:
        return render_template('/promo/promotions.html', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/profile/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('/profile/profile.html', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)