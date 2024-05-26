from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Item, Park, db

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
    
@app.route('/attractions')
def attractions():
    if current_user.is_authenticated:
        items = Item.query.order_by(Item.price).all()
        return render_template('attractions.html', user=current_user, data=items)
    else:
        return redirect(url_for('login'))

@app.route('/create_a', methods=['POST', 'GET'])
def create_a():
    if request.method == "POST":
        name = request.form['name']
        height = request.form['height']
        price = request.form['price']
        description = request.form['description']
        view = request.form['view']

        item = Item(name=name, height=height, price=price, description=description, view=view)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    else:
        return render_template('create_a.html')
    
@app.route('/create_b', methods=['POST', 'GET'])
def create_b():
    if request.method == "POST":
        name = request.form['name']
        height = request.form['height']
        price = request.form['price']
        description = request.form['description']

        item = Park(name=name, height=height, price=price, description=description)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    else:
        return render_template('create_b.html')
       
@app.route('/temparks')
def temparks():
    if current_user.is_authenticated:
        items = Park.query.order_by(Park.price).all()
        return render_template('temparks.html', user=current_user, data=items)
    else:
        return redirect(url_for('login'))
    
@app.route('/meropriyatia')
def meropriyatia():
    if current_user.is_authenticated:
        return render_template('meropriyatia.html', user=current_user)
    else:
        return redirect(url_for('login'))
    
@app.route('/price')
def price():
    if current_user.is_authenticated:
        return render_template('price.html', user=current_user)
    else:
        return redirect(url_for('login'))
    
@app.route('/promotions')
def promotions():
    if current_user.is_authenticated:
        return render_template('promotions.html', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user)
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