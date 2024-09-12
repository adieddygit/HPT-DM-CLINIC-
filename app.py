from flask import Flask, render_template, redirect, request, session, url_for
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models.users import Users
from models.users import Base
from models.patient import *
import settings
from utils import insert_data
# from app import app
from flask_simple_crypt import SimpleCrypt

def create_app()->Flask:
    app = Flask(__name__)
   
    # Set the SECRET_KEY
    app.config['SECRET_KEY'] = settings.secret_key
# Initialize Flask-Simple-Crypt
    crypt = SimpleCrypt(app)

    app.config['SQLALCHEMY_DATABASE_URI'] =f'mysql+pymysql://{settings.dbuser}:@{settings.dbhost}/{settings.dbname}'
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Base.metadata.create_all(engine, checkfirst=True)
    return app

app = create_app()
cipher = SimpleCrypt()
cipher.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(debug=True)