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

admin = Admin(app, name='Панель администратора', template_mode='bootstrap3')
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
            flash('Аккаунт успешно создан')
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

@app.route('/attractions/<int:id>/del')
def attractions_delete(id):
    items = Item.query.get_or_404(id)

    try:
            db.session.delete(items)
            db.session.commit()
            return redirect('/attraction/attractions')
    except:
            return "При удалении произошла ошибка"
    
@app.route('/attractions/<int:id>/update', methods=['POST', 'GET'])
def attractions_update(id):
    items = Item.query.get(id)
    if request.method == "POST":
        items.name = request.form['name']
        items.height = request.form['height']
        items.price = request.form['price']
        items.description = request.form['description']
        items.descriptions = request.form['descriptions']
        items.view = request.form['view']

        try:
            db.session.commit()
            return redirect('/attraction/attractions')
        except:
            return "При редактировании произошла ошибка"
    else:
        return render_template('/attraction/post_update_a.html', user=current_user, items=items)
   
@app.route('/attraction/create_a', methods=['POST', 'GET'])
def create_a():
    if request.method == "POST":
        name = request.form['name']
        height = request.form['height']
        price = request.form['price']
        description = request.form['description']
        descriptions = request.form['descriptions']
        view = request.form['view']

        items = Item(name=name, height=height, price=price, description=description, view=view, descriptions=descriptions)

        try:
            db.session.add(items)
            db.session.commit()
            return redirect('/attraction/attractions')
        except:
            return "Ошибка"
    else:
        return render_template('/attraction/create_a.html')
    

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

@app.route('/temparks/<int:id>/del')
def temparks_delete(id):
    parks = Park.query.get_or_404(id)

    try:
            db.session.delete(parks)
            db.session.commit()
            return redirect('/temparks/temparks')
    except:
            return "При удалении возникла ошибка"
    
@app.route('/temparks/<int:id>/update', methods=['POST', 'GET'])
def temparks_update(id):
    parks = Park.query.get(id)
    if request.method == "POST":
        parks.name = request.form['name']
        parks.height = request.form['height']
        parks.price = request.form['price']
        parks.description = request.form['description']
        parks.descriptions = request.form['descriptions']

        try:
            db.session.commit()
            return redirect('/temparks/temparks')
        except:
            return "При редактировании возникла ошибка"
    else:
        return render_template('/temparks/post_update_b.html', user=current_user, parks=parks)

@app.route('/temparks/create_b', methods=['POST', 'GET'])
def create_b():
    if request.method == "POST":
        name = request.form['name']
        height = request.form['height']
        price = request.form['price']
        description = request.form['description']
        descriptions = request.form['descriptions']

        parks = Park(name=name, height=height, price=price, description=description, descriptions=descriptions)

        try:
            db.session.add(parks)
            db.session.commit()
            return redirect('/temparks/temparks')
        except:
            return "Ошибка"
    else:
           return render_template('/temparks/create_b.html')

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
@app.route('/profile/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('/profile/profile.html', user=current_user)
    else:
        return redirect(url_for('login'))

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
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)