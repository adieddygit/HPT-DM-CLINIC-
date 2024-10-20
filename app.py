from flask import Flask, render_template, redirect, request, session, url_for, g, flash
from sqlalchemy import create_engine, text 
import sqlalchemy
# import sys
# import os
from flask import render_template
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models.models import *
import settings
import random
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
    
    # Set up the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{settings.dbuser}:@{settings.dbhost}/{settings.dbname}'
    
    # Create the engine
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True, pool_pre_ping=True)
    
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
        username = request.form['username']
        password_entered = request.form['password']
        
        # decrypt the password
        hash = password_entered + app.config['SECRET_KEY']
        hash = hashlib.sha256(hash.encode())
        password = hash.hexdigest()
        
        # Check if the user exists in the database
        with engine.connect() as con:
            result = con.execute(text("SELECT * FROM user WHERE username = :username AND password = :password"),
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
            msg = 'Incorrect username or password!'
            flash(msg, 'Incorect')
    
    return render_template('login.html', msg=msg)
           

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        result = request.form
        username = result['username']
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
            result = con.execute(text(f"SELECT * FROM user WHERE username = username"), {"username": username})
            account = result.fetchone()

        if account:
            msg = 'Account already exists!'
            return render_template('sign_up.html', msg=msg)
        
        if not username or not password or not cpassword:
            msg = 'Please fill out the form'
            flash(msg, 'form')
            return render_template('sign_up.html', msg=msg)

        # Hash the password
        hash_string = password + app.config['SECRET_KEY']
        hash = hashlib.sha256(hash_string.encode())
        password_hashed = hash.hexdigest()

        # Insert the new user into the database
        try:
            with engine.connect() as con:
                con.execute(text(f"INSERT IGNORE INTO user (username, email, password, role) VALUES ('{username}', '{email}', '{password}', '{role}'"))
                con.commit()
            msg = 'Account created successfully'
            flash(msg, 'success')
            return redirect(url_for('login'))  # Redirect to login after successful sign up
        
        except Exception as e:
            print(f"Error during sign-up: {e}")
            msg = 'There was an issue creating your account'
            flash(msg, 'error')
    
    return render_template('sign_up.html', msg=msg)

# return render_template('response.html', result=result)

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for(''))

@app.route('/register')
def register():
    if 'loggedin' in session:
        return render_template('register.html', username=session['username'])
    return redirect(url_for('login'))

# @app.route('/profile')
# def profile():
#       return render_template('profile.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')



@app.route('/register_client', methods=['POST'])
def register_client():
    #get the data from the form
    if request.method=='POST' and 'unique_id' in request.form:
        unique_id = random.randint(10000, 19999)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        dob = request.form['dob']
        cob = request.form['cob']
        gender = request.form['gender']
        marital_status = request.form['marital-status']
        occupation = request.form['occupation']
        phone = request.form['phone']
        address = request.form['line1']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip-code']
        country = request.form['country']
        email = request.form['email']
        ethnicity = request.form['ethnicity']
        race = request.form['race']
        #check if the unique_id is already in the database
        with engine.connect() as con:
            result = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{unique_id}'"))
            client = result.fetchone()
            if client:
                msg = 'The client already exists.'
                flash(msg, 'exists')
                return redirect(url_for('register', msg = msg))
        #check if all the required fields are filled
        
        #insert the values in the database
        created_at = datetime.now()
        updated_at = datetime.now()
        created_by = session['username']
        updated_by = session['username']
        with engine.connect() as con:
            con.execute(text(f"INSERT IGNORE INTO client_profile(created_by, created_at, updated_at, updated_by, unique_id, first_name, last_name, middle_name, dob,\
                                      cob, gender, marital_status, occupation,\
                                      phone, address, city, state, zip_code, country,\
                                      email, ethnicity, race)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}', '{first_name}', '{last_name}', '{middle_name}',\
                                      '{dob}', '{cob}', '{gender}', '{marital_status}',\
                                      '{occupation}', '{phone}',\
                                      '{address}', '{city}', '{state}', '{zip_code}', '{country}', '{email}',\
                                      '{ethnicity}', '{race}'\
                                    )"))
            
            con.execute(text(f"INSERT IGNORE INTO client_profile(created_by, created_at, updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
        
            con.execute(text(f"INSERT IGNORE INTO risk_assessment(created_by, created_at, updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
            con.execute(text(f"INSERT IGNORE INTO appointment(created_by, created_at,updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
            con.execute(text(f"INSERT IGNORE INTO health_metrics(created_by, created_at,updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
            
            con.execute(text(f"INSERT IGNORE INTO treatment(created_by, created_at, updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
            con.commit()
        msg = 'You have successfully registered the client.'
        flash(msg, 'success')
        # redirect the user to the home page
        return redirect(url_for('register', msg = msg))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    msg = f'You are logged out'
    flash(msg, 'logged out')
    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/vitals')
def vitals():
    return render_template('vitals.html')

#The retieve client page based on passed client_id
@app.route('/retrieve_client', methods=['POST'])
def retrieve_client():
    msg = ''
    #get the client_id from the urlß
    client_id = request.form['unique_id']
    #validate the client_id
    #if the client_id is not valid, redirect to the home page
    #if the client_id is valid, continue
    if 'loggedin' in session:
        if client_id:
            #get the client data from the database
            with engine.connect() as con:
                result_client_profile = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{client_id}'"))
                result_risk_assessment = con.execute(text(f"SELECT * FROM risk_assessment WHERE unique_id = '{client_id}'"))
                result_appointment = con.execute(text(f"SELECT * FROM appointment WHERE unique_id = '{client_id}'"))
                result_health_metrics = con.execute(text(f"SELECT * FROM health_metrics WHERE unique_id = '{client_id}'"))
                result_treatment = con.execute(text(f"SELECT * FROM treatment WHERE unique_id = '{client_id}'"))
                
                client_client_profile = result_client_profile.fetchone()
                client_risk_assessment = result_risk_assessment.fetchone()
                client_appointment = result_appointment.fetchone()
                client_health_metrics = result_health_metrics.fetchone()
                client_treatment = result_treatment.fetchone()
                

                con.commit()
            if client_client_profile and client_risk_assessment and client_appointment and client_health_metrics and client_treatment:
                #display the client data
                return render_template('profile.html', client_profile = client_client_profile,
                                        risk_assessment = client_risk_assessment, appointment = client_appointment,
                                          health_metrics = client_health_metrics, 
                                          treatment = client_treatment)
            else:
                #redirect to the home page
                msg = 'The client does not exist.'
                flash(msg, 'exist')
                return redirect(url_for('register', msg = msg))
    return redirect(url_for('profile', client=client_client_profile))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST' and client_id in  request.form:
        client_id = request.form['unique_id']
    
    if 'loggedin' in session:
        if client_id:
         with engine.connect() as con:
            try:
                # Check if the client already exists
                result_profile = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{client_id}'"))
                client_profile = result_profile.fetchone()
                

                if client_profile:
                    # Update existing record
                    update_at = datetime.now()
                    updated_by = session['username']
                    
                    # Retrieve form data  
                    first_name = request.form['first_name']
                    last_name = request.form['last_name']
                    middle_name = request.form['middle_name']
                    date_of_birth = request.form['dob']
                    country_of_birth = request.form['country_of_birth']
                    gender = request.form['gender']
                    marital_status = request.form['marital-status']
                    occupation = request.form['occupation']
                    gender_identity = request.form['gender-identity']
                    sexual_orientation = request.form['sexual-orientation']
                    phone_number = request.form['phone']
                    address = request.form['line1']
                    city = request.form['city']
                    state = request.form['state']
                    zip_code = request.form['zip-code']
                    country = request.form['country']
                    email = request.form['email']
                    ethnicity = request.form['ethnicity']
                    race = request.form['race']

                    print(f"Updating Client: {client_id}")
                    con.execute(text(f"""
                        UPDATE client_profile 
                        SET updated_at = '{update_at}', updated_by = '{updated_by}',
                            first_name = '{first_name}', last_name = '{last_name}',
                            middle_name = '{middle_name}', date_of_birth = '{date_of_birth}',
                            country_of_birth = '{country_of_birth}', gender = '{gender}',
                            marital_status = '{marital_status}', occupation = '{occupation}',
                            gender_identity ='{gender_identity}', sexual_orientation = '{sexual_orientation}',
                            phone_number = '{phone_number}', address = '{address}', city = '{city}',
                            state = '{state}', zip_code = '{zip_code}', country = '{country}',
                            email = '{email}', ethnicity = '{ethnicity}', race ='{race}' 
                        WHERE unique_id = '{client_id}'
                    """))
                    con.commit()
                    msg = "Client profile updated successfully"
                    flash(msg, 'success') 
                else:
                    # Insert new record if it doesn't exist
                    created_at = updated_at = datetime.now()
                    created_by = updated_by = session['username']
                    
                    print(f"Inserting new Client: {client_id}")
                    con.execute(text(f"""
                        INSERT INTO client_profile (created_by, created_at, updated_at, updated_by, unique_id, first_name, last_name, middle_name, date_of_birth, 
                        country_of_birth, gender, marital_status, occupation, gender_identity, sexual_orientation, phone_number, address, city, state, 
                        zip_code, country, email, ethnicity, race)
                        VALUES ('{created_by}', '{created_at}', '{updated_at}', '{updated_by}', '{client_id}', '{first_name}', '{last_name}', 
                        '{middle_name}', '{date_of_birth}', '{country_of_birth}', '{gender}', '{marital_status}', '{occupation}', '{gender_identity}', 
                        '{sexual_orientation}', '{phone_number}', '{address}', '{city}', '{state}', '{zip_code}', '{country}', '{email}', '{ethnicity}', '{race}')
                    """))
                    con.commit()
                    msg = "Client profile created successfully"
                    flash(msg, 'success')

                
                return render_template('home.html', msg=msg)

            except sqlalchemy.exc.IntegrityError as e:
                con.rollback()
                msg = f"Integrity error: {str(e)}"
                print(msg)
                return render_template('profile.html', msg=msg)
    else:
        msg = "You need to be logged in to update profiles."
        flash(msg, 'update')
        return redirect(url_for('login', msg=msg))


@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    msg = ''
    if request.method == 'POST' and 'unique_id' in request.form:
        unique_id = request.form['unique_id']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        purpose = request.form['purpose']
        provider_type = request.form['provider_type'] 
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        appointment_status = request.form['appointment_status']
        last_appointment_date = request.form['last_appointment_date']
        treatment_notes = request.form['treatment_notes']
        #check if the unique_id is already in the database
        with engine.connect() as con:
            result = con.execute(text(f"SELECT * FROM appointment WHERE unique_id = '{client_id}'"))
            client_id = result.fetchone()
            if client_id:
                msg = 'Pending Appointment.'
                return redirect(url_for('appointment', msg = msg))
        #check if all the required fields are filled

        #insert the values in the database
        created_at = datetime.now()
        updated_at = datetime.now()
        created_by = session['username']
        updated_by = session['username']
        with engine.connect() as con:
            con.execute(text(f"INSERT INTO appointment(created_by, created_at, updated_at, updated_by, unique_id, username,\
                              email, phone, provider_type, purpose, appointment_date, appointment_time, appointment_status,\
                              last_appointment_date, treatment_notes)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}', '{username}',\
                            '{email}', '{phone}', '{provider_type}', '{purpose}', '{appointment_date}', '{appointment_time}', '{appointment_status}',\
                                      '{last_appointment_date}', '{treatment_notes}')"))
            
            
            con.commit()
        msg = 'You have successfully booked for an appointment.'
        # redirect the user to the home page
        return redirect(url_for('appointment', msg = msg))
    return render_template('appointment.html')
        
@app.route('/patient')
def patient():
    return render_template('patient.html')

# Hashing a password
# password_hash = bcrypt.generate_password_hash(password_entered).decode('utf-8')

# Verifying a password
# is_valid = bcrypt.check_password_hash(password_hash, password_entered)

if __name__ == '__main__':
    app.run(debug=True)