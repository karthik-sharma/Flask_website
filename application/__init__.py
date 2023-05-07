from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt


basepath = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basepath, 'database.db')
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from application import routes
