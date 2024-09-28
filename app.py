from flask import Flask, render_template, redirect, request, session,  url_for, g
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
    
    # Set up the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{settings.dbuser}:@{settings.dbhost}/{settings.dbname}'
    
    # Create the engine
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    
    # Configure the scoped session
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    
    # Initialize the Base class
    Base.metadata.create_all(engine, checkfirst=True)
    
    return app

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False))


app = create_app()
cipher = SimpleCrypt()
cipher.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = request.form
        session = SessionLocal()
        try:
            username = result['username']
            email = result['email']
            password = cipher.encrypt(result['password'])  # Encrypt password
            role = result['role']  # Admin, Client, Clinical

            # Create a new user and insert into DB
            new_user = Users(username=username, email=email, password=password, role=role)
            session.add(new_user)
            session.commit()

            return redirect(url_for('home'))
        finally:
            session.close()
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

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
    # Use the scoped session to query the database
    patient = SessionLocal.query(PatientReg).get_or_404(patient_id)
    medical_history = SessionLocal.query(RiskAssessment).filter_by(patient_id=patient_id).all()
    appointments = SessionLocal.query(Appointment).filter_by(patient_id=patient_id).all()

    return render_template('profile.html', patient=patient, medical_history=medical_history, appointments=appointments)

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/history/<int:patient_id>')
def history(patient_id):
    # Fetch patient data by patient_id
    patient = PatientReg.query.get_or_404(patient_id)  # Retrieve patient record
    health_metrics = PatientHealthMetrics.query.filter_by(patient_id=patient_id).all()  # Retrieve health metrics

    # Pass the patient and health metrics data to the template
    return render_template('history.html', patient=patient, health_metrics=health_metrics)

@app.teardown_appcontext
def remove_session(exception=None):
    session = g.get('db_session', None)
    if session is not None:
        session.remove()



if __name__ == '__main__':
    app.run(debug=True)