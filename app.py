from flask import Flask, render_template, redirect, request, session, url_for, flash
from sqlalchemy import create_engine, text
from models.models import *
import random
# from utils import insert_data
import hashlib

app = Flask(__name__)
# Set the SECRET_KEY
app.secret_key="somesecretkey"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/hpt_dm_clinic_management_db'
# Create the engine
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
# Initialize the Base class
Base.metadata.create_all(engine, checkfirst=True)

@app.route('/')
def index():
      return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Get the form values
        username = request.form['username']
        password_entered = request.form['password']
        
        # Hash the password entered by the user
        hash = password_entered + app.secret_key
        hash = hashlib.sha256(hash.encode())
        password = hash.hexdigest()
        
        # Check if the user exists in the database
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}' and password = '{password}'"))
            account = result.fetchone()
            con.commit()

        # Verify if the account exists
        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = "You are logged in successfully"
            flash(msg, 'success')
            return redirect(url_for('home', msg=msg))
        
        if not username or not password:
            msg = "Please enter username and password"
            flash(msg, 'enter')
            return render_template('login.html', msg=msg)
        
        else:
            msg = "Incorrect username or password"
            flash(msg, 'Incorrect')
    return render_template('login.html', msg=msg)
          

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        username = request.form['username']
        email = request.form['email'].lower()
        role = request.form['role']
        password = request.form['password'].lower()
        cpassword = request.form['cpassword'].lower()

         # Check if passwords match
        
        if password != cpassword:
            msg = 'Passwords do not match'
            flash(msg, 'Password')
            return render_template('sign_up.html', msg=msg)
        
        # Check if the username already exists in the database
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}'"))            
            account = result.fetchone()
            con.commit()

        if account:
            msg = 'Account already exists!'
            flash(msg, 'Account')
            return render_template('sign_up.html', msg=msg)
        
        if not username or not password or not cpassword:
            msg = 'Please fill out the form'
            flash(msg, 'form')
            return render_template('sign_up.html', msg=msg)
        else:
            #Encrypt the email (not necessary for most apps, just as an example)
            # enc_email = cipher.encrypt(email)
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha256(hash.encode())
            password = hash.hexdigest()

            # Insert the new user into the database
        # try:
            with engine.connect() as con:
                con.execute(text(f"INSERT INTO user (username, email, password, role) VALUES ('{username}', '{email}', '{password}', '{role}')"))
                con.commit()
            msg = 'Account created successfully'
            flash(msg, 'success')
            return redirect(url_for('login'))  # Redirect to login after successful sign up
        
        # except Exception as e:
            # print(f"Error during sign-up: {e}")
            # msg = 'There was an issue creating your account'
            # flash(msg, 'error')
    
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
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_number = request.form['emergency_contact_number']
        emergency_contact_relationship = request.form['emergency_contact_relationship']
        emergency_contact_address = request.form['emergency_contact_address']
        family_has_history_of_hpt_dm = request.form['family_has_history_of_hpt_dm']
        has_underlying_medical_condition = request.form['has_underlying_medical_condition']
        underlying_condition = request.form['underlying_condition']
        alcohol_intake = request.form['alcohol_intake']
        smoking_tobacco_use = request.form['smoking_tobacco_use']
        type_of_diet = request.form['type_of_diet']
        bmi = request.form['bmi']
        dose_exercise = request.form['dose_exercise']

      
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
            con.execute(text(f"""INSERT IGNORE INTO client_profile(created_by, created_at, updated_at, updated_by, unique_id, first_name, last_name, middle_name, dob,
                                  cob, gender, marital_status, occupation,
                                  phone, address, city, state, zip_code, country,
                                  email, ethnicity, race, emergency_contact_name, emergency_contact_number, emergency_contact_relationship,
                                  emergency_contact_address, family_has_history_of_hpt_dm, has_underlying_medical_condition,
                                                        underlying_condition, alcohol_intake, smoking_tobacco_use, type_of_diet, bmi, dose_exercise)
                                VALUES('{created_by}', '{created_at}', '{updated_at}', '{updated_by}', '{unique_id}', '{first_name}', '{last_name}', '{middle_name}',
                            '{dob}', '{cob}', '{gender}', '{marital_status}', '{occupation}', '{phone}', '{address}', '{city}', '{state}', '{zip_code}', '{country}',
                            '{email}', '{ethnicity}', '{race}', '{emergency_contact_name}', '{emergency_contact_number}', '{emergency_contact_relationship}',
                            '{emergency_contact_address}', '{family_has_history_of_hpt_dm}', '{has_underlying_medical_condition}', '{underlying_condition}',
                            '{alcohol_intake}', '{smoking_tobacco_use}', '{type_of_diet}', '{bmi}', '{dose_exercise}'\
                                                            )"""))
    
            con.execute(text(f"INSERT INTO health_metrics(created_by, created_at,updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
            
            con.execute(text(f"INSERT INTO treatment(created_by, created_at, updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
            con.commit()
        msg = 'Client successfully registered'
        flash(msg, 'success')
        # redirect the user to the home page
        return redirect(url_for('home', msg = msg))
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
    client_id = request.form['client_id']  # Retrieving client using the Client's ID

    if 'loggedin' in session:
        if client_id:
            # Get the client data from the database
            with engine.connect() as con:
                # Fetch each result
                result_profile = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{client_id}'"))
                result_appointment = con.execute(text(f"SELECT * FROM appointment WHERE unique_id = '{client_id}'"))
                result_health_metrics = con.execute(text(f"SELECT * FROM health_metrics WHERE unique_id = '{client_id}'"))
                result_treatment = con.execute(text(f"SELECT * FROM treatment WHERE unique_id = '{client_id}'"))
                
                # Fetchone for each query to retrieve data as dictionaries
                client_profile = result_profile.fetchone()
                client_appointment = result_appointment.fetchone()
                client_health_metrics = result_health_metrics.fetchone()
                client_treatment = result_treatment.fetchone()

                con.commit()
            # Check if data is available for each
            if client_profile and client_appointment and client_health_metrics and client_treatment:
                return render_template(
                    'profile.html', 
                    client=client_profile, 
                    appointment=client_appointment, 
                    health_metrics=client_health_metrics, 
                    treatment=client_treatment
                )
            
            else:
                msg = 'The client does not exist.'
                flash(msg, 'exist')
                return redirect(url_for('register', msg=msg))
    
    return redirect(url_for('login'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    msg=""
    if request.method == 'POST':
        client_id = request.form['unique_id']
    
    if 'loggedin' in session:
        if client_id:
         with engine.connect() as con:
            # try:
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
                    dob = request.form['dob']
                    cob = request.form['cob']
                    gender = request.form['gender']
                    marital_status = request.form['marital_status']
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
                    emergency_contact_name = request.form['emergency_contact_name']
                    emergency_contact_number = request.form['emergency_contact_number']
                    emergency_contact_relationship = request.form['emergency_contact_relationship']
                    emergency_contact_address = request.form['emergency_contact_address']
                    family_has_history_of_hpt_dm = request.form['family_has_history_of_hpt_dm']
                    has_underlying_medical_condition = request.form['has_underlying_medical_condition']
                    underlying_condition = request.form['underlying_condition']
                    alcohol_intake = request.form['alcohol_intake']
                    smoking_tobacco_use = request.form['smoking_tobacco_use']
                    type_of_diet = request.form['type_of_diet']
                    bmi = request.form['bmi']
                    dose_exercise = request.form['dose_exercise']

                    print(f"Updating Client: {client_id}")
                    con.execute(text(f"""
                        UPDATE client_profile 
                        SET updated_at = '{update_at}', updated_by = '{updated_by}',\
                            first_name = '{first_name}', last_name = '{last_name}',\
                            middle_name = '{middle_name}', dob = '{dob}',\
                            cob = '{cob}', gender = '{gender}',\
                            marital_status = '{marital_status}', occupation = '{occupation}',\
                            phone = '{phone}', address = '{address}', city = '{city}',\
                            state = '{state}', zip_code = '{zip_code}', country = '{country}',\
                            email = '{email}', ethnicity = '{ethnicity}', race ='{race}',\
                            emergency_contact_name = '{emergency_contact_name}',\
                            emergency_contact_number = '{emergency_contact_number}',\
                             
                            emergency_contact_relationship = '{emergency_contact_relationship}',\
                            emergency_contact_address = '{emergency_contact_address}',\
                            family_has_history_of_hpt_dm = '{family_has_history_of_hpt_dm}',\
                            has_underlying_medical_condition = '{has_underlying_medical_condition}',\
                            underlying_condition = '{underlying_condition}',\
                            alcohol_intake = '{alcohol_intake}', smoking_tobacco_use = '{smoking_tobacco_use}',\
                            type_of_diet = '{type_of_diet}', bmi = '{bmi}', dose_exercise = '{dose_exercise}'\
                        WHERE unique_id = '{client_id}'"""))
                    con.commit()
                    msg = "Client profile updated successfully"
                    flash(msg, 'success') 
                else:
                    # Insert new record if it doesn't exist
                    created_at = updated_at = datetime.now()
                    created_by = updated_by = session['username']
                    
                    print(f"Inserting new Client: {client_id}")
                    con.execute(text(f"""
                        INSERT INTO client_profile (created_by, created_at, updated_at, updated_by, unique_id, first_name, last_name, middle_name, dob, 
                        cob, gender, marital_status, occupation,  phone, address, city, state, 
                        zip_code, country, email, ethnicity, race, emergency_contact_name, emergency_contact_number,
                        emergency_contact_relationship, emergency_contact_address, family_has_history_of_hpt_dm, 
                        has_underlying_medical_condition, underlying_condition, alcohol_intake, smoking_tobacco_use, type_of_diet, bmi, dose_exercise)
                        VALUES ('{created_by}', '{created_at}', '{updated_at}', '{updated_by}', '{client_id}', '{first_name}', '{last_name}', 
                        '{middle_name}', '{dob}', '{cob}', '{gender}', '{marital_status}', '{occupation}', 
                         '{phone}', '{address}', '{city}', '{state}', '{zip_code}', '{country}', '{email}', '{ethnicity}', '{race}', '{emergency_contact_name}',
                         '{emergency_contact_number}', '{emergency_contact_relationship}', '{emergency_contact_address}', '{family_has_history_of_hpt_dm}', '{has_underlying_medical_condition}',
                          '{underlying_condition}', '{alcohol_intake}', '{smoking_tobacco_use}', '{type_of_diet}',
                         '{bmi}', '{dose_exercise}')
                    """))
                    con.commit()
                    msg = "Client profile created successfully"
                    flash(msg, 'success')
                return render_template('home.html', msg=msg)
        else:
            msg = "You need to login to update client."
            flash(msg, 'update')
            return redirect(url_for('login', msg=msg))



@app.route('/appointment')
def appointment():
    return render_template('appointment.html')


from flask import flash, redirect, render_template, request, session, url_for
from sqlalchemy import text, create_engine
from datetime import datetime


@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    msg = ''
    if request.method == 'POST' and 'unique_id' in request.form:
        unique_id = request.form['unique_id']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        purpose = request.form['purpose']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        message = request.form['message']

        # Record creation and update timestamps
        created_at = datetime.now()
        updated_at = datetime.now()
        created_by = session.get('username')
        updated_by = session.get('username')

        try:
            # Test the connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("Database connection test result:", result.scalar())  # Should print "1" if connected

            # Insert the values into the database with parameterized query
            with engine.begin() as conn:  # `begin` will ensure a commit at the end
                conn.execute(
                    text("""
                        INSERT INTO appointment (
                            created_by, created_at, updated_at, updated_by, unique_id, 
                            username, email, phone, purpose, appointment_date, appointment_time, message
                        ) VALUES (
                            :created_by, :created_at, :updated_at, :updated_by, :unique_id, 
                            :username, :email, :phone, :purpose, :appointment_date, :appointment_time, :message
                        )
                    """),
                    {
                        'created_by': created_by,
                        'created_at': created_at,
                        'updated_at': updated_at,
                        'updated_by': updated_by,
                        'unique_id': unique_id,
                        'username': username,
                        'email': email,
                        'phone': phone,
                        'purpose': purpose,
                        'appointment_date': appointment_date,
                        'appointment_time': appointment_time,
                        'message': message
                    }
                )
            msg = 'Appointment Submitted Successfully'
            flash(msg, 'Appointment')
            return redirect(url_for('home', msg=msg))
        except Exception as e:
            print(f"Error inserting data: {e}")  # Print error for debugging
            msg = 'Failed to submit appointment. Please try again.'
            flash(msg, 'Error')
    return render_template('appointment.html')




@app.route('/update_appointment', methods=['POST'])
def update_appointment():
    msg=""
    # if request.method == 'POST':
    client_id = request.form['unique_id']
    
    if 'loggedin' in session:
        if client_id:
         with engine.connect() as con:
            # try:
                # Check if the client already exists
                result_appointment = con.execute(text(f"SELECT * FROM appointment WHERE unique_id = '{client_id}'"))
                appointment = result_appointment.fetchone()
                con.commit()
                if appointment:
                    # Update existing record
                    updated_at = datetime.now()
                    updated_by = session['username']
                    
                    # Retrieve form data 
                    # username = request.form['username']
                    email = request.form['email']
                    phone = request.form['phone']
                    purpose = request.form['purpose']
                    appointment_date = request.form['appointment_date']
                    appointment_time = request.form['appointment_time']
                    message = request.form['message']
                   
                    with engine.connect() as con:
                        result = con.execute(text(f"""UPDATE appointment SET updated_at = '{updated_at}', updated_by = '{updated_by}',\
                                                   email = '{email}',\
                                                    phone = '{phone}', purpose = '{purpose}',\
                                                    message = '{message}', appointment_date = '{appointment_date}',\
                                                    appointment_time = '{appointment_time}'\
                                                    WHERE unique_id = '{client_id}'"""))
                    
                    con.commit()
                    # print(request.form)
                    msg = "Appointment updated successfully"
                    flash(msg, 'success') 
                    return render_template('appointment.html', msg=msg)
        else:
            msg = "You need to login to update appointment."
            flash(msg, 'update')
            return redirect(url_for('login', msg=msg))
        
        
@app.route('/metrics')
def metrics():
    return render_template('metrics.html')

@app.route('/treatment')
def treatment():
    return render_template('treatment.html')

@app.route('/patient')
def patient():
    return render_template('patient.html')

if __name__ == '__main__':
    app.run(debug=True)