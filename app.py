from flask import Flask, render_template, redirect, request, session, url_for, g, flash
from sqlalchemy import create_engine, text 
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models.users import Users
from models.users import Base
from models.users import *
from models.patient import *
import settings
from utils import insert_data
# from app import app
from flask_simple_crypt import SimpleCrypt
import hashlib
# from flask_bcrypt import Bcrypt

def create_app()->Flask:
    app = Flask(__name__)
    
    # Set the SECRET_KEY
    app.config['SECRET_KEY'] = settings.secret_key
    
    # Initialize Flask-Simple-Crypt
    crypt = SimpleCrypt(app)

    # bcrypt = Bcrypt(app)
    
    # Set up the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{settings.dbuser}:@{settings.dbhost}/{settings.dbname}'
    
    # Create the engine
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    
    # Configure the scoped session
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    
    # Initialize the Base class
    Base.metadata.create_all(engine, checkfirst=True)
    
    return app

app = create_app()
cipher = SimpleCrypt()
cipher.init_app(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

@app.route('/')
def index():
      return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        username = request.form['username'].lower()
        password_entered = request.form['password']
        
        # decrypt the password
        hash = password_entered + app.config['SECRET_KEY']
        hash = hashlib.sha256(hash.encode())
        password = hash.hexdigest()
        
        # Check if the user exists in the database
        with engine.connect() as con:
            result = con.execute(text("SELECT * FROM users WHERE username = :username AND password = :password"),
                     {"username": username, "password": password})
            account = result.fetchone()
            # con.commit()
        
        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = f'You are welcome {username}'
            flash(msg, 'logged In')
            return redirect(url_for('home',msg=msg))

        else:
            msg = 'Incorrect username/password!'
    
    return render_template('login.html', msg=msg)
           

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        result = request.form
        username = result['username'].lower()
        email = result['email'].lower()
        role = result['role']
        
        # Encrypt the email (not necessary for most apps, just as an example)
        enc_email = cipher.encrypt(email)
        
        # Check if passwords match
        password = result['password'].lower()
        cpassword = result['cpassword'].lower()
        if password != cpassword:
            msg = 'Passwords do not match'
            return render_template('sign_up.html', msg=msg)
        
        # Check if the username already exists in the database
        with engine.connect() as con:
            result = con.execute(text(f"SELECT * FROM users WHERE username = :username"), {"username": username})
            account = result.fetchone()

        if account:
            msg = 'Account already exists!'
            return render_template('sign_up.html', msg=msg)
        
        if not username or not password or not cpassword:
            msg = 'Please fill out the form'
            return render_template('sign_up.html', msg=msg)

        # Hash the password
        hash_string = password + app.config['SECRET_KEY']
        hash = hashlib.sha256(hash_string.encode())
        password_hashed = hash.hexdigest()

        # Insert the new user into the database
        try:
            with engine.connect() as con:
                con.execute(text(f"INSERT INTO users (username, email, password, role) VALUES (:username, :email, :password, :role)"),
                            {"username": username, "email": enc_email, "password": password_hashed, "role": role})
                con.commit()
            msg = 'Account created successfully'
            flash(msg, 'success')
            return redirect(url_for('login'))  # Redirect to login after successful sign up
        
        except Exception as e:
            print(f"Error during sign-up: {e}")
            msg = 'There was an issue creating your account'
    
    return render_template('sign_up.html', msg=msg)

# return render_template('response.html', result=result)

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for(''))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/vitals')
def vitals():
    return render_template('vitals.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

# @app.route('/profile')
# def profile():
#     return render_template('profile.html')

@app.route('/profile/<int:patient_id>')
def profile(patient_id):
    # Retrieve the patient from the database by patient_id
    patient = SessionLocal.query(PatientReg).get_or_404(patient_id)
    
    # Retrieve the medical history and appointments
    medical_history = SessionLocal.query(RiskAssessment).filter_by(patient_id=patient_id).all()
    appointments = SessionLocal.query(Appointment).filter_by(patient_id=patient_id).all()

    # Pass the patient, medical history, and appointments to the template
    return render_template('profile.html', patient=patient, medical_history=medical_history, appointments=appointments)


@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

# @app.route('/history/<int:patient_id>')
# def history(patient_id):
#     # Fetch patient data by patient_id
#     patient = PatientReg.query.get_or_404(patient_id)  # Retrieve patient record
#     health_metrics = PatientHealthMetrics.query.filter_by(patient_id=patient_id).all()  # Retrieve health metrics

    # Pass the patient and health metrics data to the template
    # return render_template('history.html', patient=patient, health_metrics=health_metrics)

# @app.teardown_appcontext
# def remove_session(exception=None):
#     session = g.get('db_session', None)
#     if session is not None:
#         session.remove()

# Hashing a password
# password_hash = bcrypt.generate_password_hash(password_entered).decode('utf-8')

# Verifying a password
# is_valid = bcrypt.check_password_hash(password_hash, password_entered)

if __name__ == '__main__':
    app.run(debug=True)