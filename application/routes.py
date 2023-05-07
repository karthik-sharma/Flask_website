from flask import render_template, redirect, url_for, flash, get_flashed_messages
from sqlalchemy import desc
from application import app, db
from application.models import RegisterForm, LoginForm, ExpenseForm, User, ExpenseInfo, SearchForm
from application import bcrypt
from flask_login import login_user, LoginManager,  logout_user, login_required, current_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_check = User.query.filter_by(username=form.username.data).first()
        print(user_check)
        if not user_check:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            user = User(name=form.name.data, username=form.username.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Successfully Registered", 'success')
            return redirect(url_for('login'))
        else:
            flash("username already exists, please try with new username", 'warning')
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for('expense'))
            else:
                flash("Password incorrect", 'error')
        else:
            flash("Incorrect username", 'error')
    return render_template('login.html', form=form)

@app.route('/expense', methods=['POST','GET'])
@login_required
def expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        info = ExpenseInfo(amount = form.amount.data, category = form.category.data, username = current_user.username)
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('expense.html', form=form)

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    sums = ExpenseInfo.query.filter_by(username=current_user.username).order_by(desc(ExpenseInfo.date))
    total_amount = sum(total.amount for total in sums)
    print(total_amount)
    info = ExpenseInfo.query.filter_by(username=current_user.username).order_by(desc(ExpenseInfo.date))
    return render_template('dashboard.html', form=info, total_amount=total_amount)

@app.route('/search', methods=['POST','GET'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash("Incorrect username! user doesn't exist", 'error')
        info = ExpenseInfo.query.filter_by(username=form.username.data).all()
        if info:
            sums = ExpenseInfo.query.filter_by(username=form.username.data).order_by(desc(ExpenseInfo.date))
            total_amount = sum(total.amount for total in sums)
            print(total_amount)
            return render_template('dashboard.html', form=info, total_amount=total_amount)
    return render_template('search.html', form=form)

@app.route('/account', methods=['POST','GET'])
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file)