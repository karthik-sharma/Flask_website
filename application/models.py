from flask_login import UserMixin
from application import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, ValidationError
from datetime import datetime


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')

class ExpenseInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer)
    category = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.now)

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=4, max=10)], render_kw={'placeholder': 'Name'})
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=10)], render_kw={'placeholder': 'Username'})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=10)], render_kw={'placeholder':'password'})
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=10)], render_kw={'placeholder': 'Username'})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=10)], render_kw={'placeholder':'password'})
    submit = SubmitField('Register')

class ExpenseForm(FlaskForm):
    amount = IntegerField("Amount", validators=[InputRequired()])
    category = SelectField("Category", validators=[InputRequired()], choices=[('rent', 'rent'), ('groceries', 'groceries'),
                                                                              ('food', 'food'), ('entertainment', 'entertainment')])
    submit = SubmitField("Generate Report")
class SearchForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=10)],
                           render_kw={'placeholder': 'Username'})
    submit = SubmitField('Search')

with app.app_context():
    db.create_all()