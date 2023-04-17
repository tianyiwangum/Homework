from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import subprocess as sp
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
load_dotenv()
import os
###########init process#################
app =  Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(32).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
moment = Moment(app)
db = SQLAlchemy(app)
# with app.app_context():
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
@app.before_first_request
def create_tables():
    db.create_all()
from website import routes