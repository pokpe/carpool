import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = "b5ca1c25bcdf0d75c8d504a463b809b2"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['SECURITY_EMAIL_SENDER'] = os.environ.get('EMAIL_USER')
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
print('LOL: %s', os.getenv('EMAIL_PASS'))
print('Email: %s',app.config['MAIL_USERNAME'])
print('Pass: %s',app.config['MAIL_PASSWORD'])
mail = Mail(app)

from carpool import routes
