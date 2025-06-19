from flask import Flask, render_template, redirect, request, session, url_for, flash, logging
from sqlalchemy import create_engine, text
from models.models import *
import hashlib
import random
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Decide which DB URL to use
if os.getenv("ENV") == "production":
    db_url = os.getenv("DATABASE_URI")  # Should be set in Render
else:
    db_url = "sqlite:///local.db"  # Local fallback

# Now set the config
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

# Create the engine with the correct db_url
engine = create_engine(db_url, echo=True)

# Initialize database models
Base.metadata.create_all(engine, checkfirst=True)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

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
            msg = f"You are logged in as {username}" 
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
            
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha256(hash.encode())
            password = hash.hexdigest()

            # Insert the new user into the database
        try: # For error handling
            with engine.connect() as con:
                con.execute(text(f"INSERT INTO user (username, email, password, role) VALUES ('{username}', '{email}', '{password}', '{role}')"))
                con.commit()
            msg = 'Account created successfully'
            flash(msg, 'success')
            return redirect(url_for('login'))  # Redirect to login after successful sign up
        except Exception as e:
            msg = 'There was an issue creating your account'
            flash(msg, 'error',e)
    
    return render_template('sign_up.html', msg=msg)
         
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html')
    return redirect(url_for(''))

@app.route('/register')
def register():
    if 'loggedin' in session:
        return render_template('register.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/register_client', methods=['POST'])
def register_client():
    msg=''

    #get the data from the form 
    if request.method=='POST' and 'unique_id' in request.form:
        unique_id = 'DHC' + str(random.randint(111, 1111))
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

    try:
        with engine.connect() as con:
            result =  con.execute(text(f"""INSERT IGNORE INTO client_profile(created_by, created_at, updated_at, updated_by, unique_id, first_name, last_name, middle_name, dob,
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
            
            con.commit()
            msg = 'Client successfully registered'
            flash(msg, 'success')
        # redirect the user to the home page
            return redirect(url_for('register', msg = msg))
    except Exception as e:
            msg= f"Please fill out the form: {e}."
            flash(msg,'fill form')
    return render_template('register.html')


@app.route('/add_metrics', methods=['POST'])
def add_metrics():
    msg =''
    if request.method == 'POST' and 'unique_id' in request.form:
        # Extract form data
        data = {key: request.form.get(key, None) for key in [
            'unique_id', 'recorded_date', 'health_care_facility', 'provider_name', 'provider_contact',
            'weight', 'height', 'blood_pressure', 'fasting_blood_suger', 'random_blood_suger',
            'temperature', 'respiration', 'pulse', 'spo2', 'urine_ketones', 'lab_investigation_type',
            'lab_investigation_result', 'radiograph_investigation_type', 'radiograph_investigation_result',
            'metric_notes', 'diagnosis', 'hospitalized_for_hpt_dm', 'complications'
        ]}

        # Add metadata
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        data['created_by'] = session.get('username', 'system')  # Fallback to 'system' if no session
        data['updated_by'] = data['created_by']

        try:
            with engine.begin() as con:
                con.execute(
                    text("""
                        INSERT INTO health_metrics (
                            created_by, created_at, updated_at, updated_by, unique_id, recorded_date, 
                            health_care_facility, provider_name, provider_contact, weight, height, 
                            blood_pressure, fasting_blood_suger, random_blood_suger, temperature, respiration, 
                            pulse, spo2, urine_ketones, lab_investigation_type, lab_investigation_result, 
                            radiograph_investigation_type, radiograph_investigation_result, metric_notes, 
                            diagnosis, hospitalized_for_hpt_dm, complications
                        ) VALUES (
                            :created_by, :created_at, :updated_at, :updated_by, :unique_id, :recorded_date, 
                            :health_care_facility, :provider_name, :provider_contact, :weight, :height, 
                            :blood_pressure, :fasting_blood_suger, :random_blood_suger, :temperature, :respiration, 
                            :pulse, :spo2, :urine_ketones, :lab_investigation_type, :lab_investigation_result, 
                            :radiograph_investigation_type, :radiograph_investigation_result, :metric_notes, 
                            :diagnosis, :hospitalized_for_hpt_dm, :complications
                        )
                    """), data
                )
            msg = 'Health records added successfully.'
            flash(msg, 'success')
            return redirect(url_for('home', msg=msg))
        
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
            flash('Failed to submit records. Please try again.', 'error')
            return render_template('metrics.html')  # Return to form with error message

    # If method is not POST or 'unique_id' is missing in form data
    
    msg = 'Invalid form submission.'
    flash(msg, 'error')
    return render_template('metrics.html', msg=msg)


@app.route('/add_treatment', methods=['POST'])
def add_treatment():
    msg=''
    # Check if request method is POST and unique_id is provided
    if request.method == 'POST' and 'unique_id' in request.form:
        unique_id = request.form['unique_id']
        
        # Optional fields; use get() with defaults as needed
        date_of_treatment = request.form.get('date_of_treatment', datetime.now())
        treatment_type = request.form.get('treatment_type')  # None if not provided
        defaulted_treatment = request.form.get('defaulted_treatment', 'No')  # Default to 'No'
        health_care_facility = request.form.get('health_care_facility')  # None if not provided
        provider_type = request.form.get('provider_type') # None if not provided
        provider_contact = request.form.get('provider_contact')  # None if not provided
        treatment_plan = request.form.get('treatment_plan')  # None if not provided
        treatment_notes = request.form.get('treatment_notes')  # None if not provided

        # Metadata fields
        created_at = datetime.now()
        updated_at = datetime.now()
        created_by = session.get('username', 'system')
        updated_by = session.get('username', 'system')

        try:
            # Insert data into database using a parameterized query
         with engine.connect() as con:
            con.execute(text("""INSERT INTO treatment (
                            created_at, updated_at, created_by, updated_by, unique_id,
                            date_of_treatment, defaulted_treatment,
                            health_care_facility, provider_type, provider_contact, treatment_type, treatment_plan, treatment_notes
                        ) VALUES (
                            :created_at, :updated_at, :created_by, :updated_by, :unique_id,
                            :date_of_treatment, :defaulted_treatment,
                            :health_care_facility, :provider_type, :provider_contact, :treatment_type, :treatment_plan, :treatment_notes
                        )
                    """),
                    {
                        'created_at': created_at,
                        'updated_at': updated_at,
                        'created_by': created_by,
                        'updated_by': updated_by,
                        'unique_id': unique_id,
                        'date_of_treatment': date_of_treatment,
                        'defaulted_treatment': defaulted_treatment,
                        'health_care_facility': health_care_facility,
                        'provider_type': provider_type,
                        'provider_contact': provider_contact,
                        'treatment_type': treatment_type,
                        'treatment_plan': treatment_plan,
                        'treatment_notes': treatment_notes
                    }
                )
            
            con.commit()
            msg = 'Treatment record added successfully.'
            flash(msg, 'success')
            return redirect(url_for('home', msg=msg))

        except Exception as e:
            msg = 'Please fill out the form.'
            flash(msg, 'fill')

    # Render treatment form if method is not POST or unique_id is missing
    return render_template('treatment.html')


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


@app.route('/retrieve_client', methods=['POST'])
def retrieve_client():
    msg = ''
    client_id = request.form.get('client_id')  # Retrieve client ID safely

    if client_id:
        # Get the client data from the database
        with engine.connect() as con:
            # Fetch each result
            result_profile = con.execute(text("SELECT * FROM client_profile WHERE unique_id = :client_id"), {'client_id': client_id})
            result_appointment = con.execute(text("SELECT * FROM appointment WHERE unique_id = :client_id"), {'client_id': client_id})
            result_health_metrics = con.execute(text("SELECT * FROM health_metrics WHERE unique_id = :client_id"), {'client_id': client_id})
            result_treatment = con.execute(text("SELECT * FROM treatment WHERE unique_id = :client_id"), {'client_id': client_id})

            # Fetch data as dictionaries
            client_profile = result_profile.fetchone()  
            client_appointment = result_appointment.fetchone()  
            client_health_metrics = result_health_metrics.fetchone()  
            client_treatment = result_treatment.fetchone()  

        # Check if any data is available
        if client_profile or client_appointment or client_health_metrics or client_treatment:
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

    flash('Please enter a valid Client ID.', 'error')
    return redirect(url_for('profile'))


@app.route('/update_profile', methods=['POST'])
def update_profile():
    msg=""
    client_id = request.form['unique_id']
    if 'loggedin' in session:
        if client_id:
            #get the client data from the database
            with engine.connect() as con:
                result_profile = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{client_id}'"))
                client_profile = result_profile.fetchone()
                con.commit()
            if client_profile:
                #display the client data
                updated_at = datetime.now()
                updated_by = session['username']
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                middle_name = request.form['middle_name']
                dob = request.form['dob']
                cob = request.form['cob']
                gender = request.form['gender']
                marital_status = request.form['marital_status']
                occupation = request.form['occupation']
                gender = request.form['gender']
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
                with engine.connect() as con:
                    result = con.execute(text(f"UPDATE client_profile SET updated_at = '{updated_at}', updated_by = '{updated_by}',\
                                              first_name = '{first_name}', last_name = '{last_name}',\
                                                middle_name = '{middle_name}', dob = '{dob}',\
                                                cob = '{cob}', gender = '{gender}',\
                                                marital_status = '{marital_status}', occupation = '{occupation}',\
                                                gender ='{gender}',\
                                                phone = '{phone}', address = '{address}', city = '{city}',\
                                                state = '{state}', zip_code = '{zip_code}', country = '{country}',\
                                                email = '{email}', ethnicity = '{ethnicity}', race ='{race}',\
                                                emergency_contact_name = '{emergency_contact_name}', emergency_contact_number = '{emergency_contact_number}',\
                                                emergency_contact_relationship = '{emergency_contact_relationship}', emergency_contact_address = '{emergency_contact_address}',\
                                                family_has_history_of_hpt_dm = '{family_has_history_of_hpt_dm}', has_underlying_medical_condition = '{has_underlying_medical_condition}',\
                                                underlying_condition = '{underlying_condition}', alcohol_intake = '{alcohol_intake}', smoking_tobacco_use = '{smoking_tobacco_use}',\
                                                type_of_diet = '{type_of_diet}', bmi = '{bmi}', dose_exercise = '{dose_exercise}'  WHERE unique_id = '{client_id}'"))
                    con.commit()
                msg = "Client profile updated successfully"
                flash(msg, 'success')
                return render_template('home.html', msg=msg)
                
            else:
                #redirect to the home page
                msg = 'The client does not exist.'
                flash(msg, 'exist')
                return redirect(url_for('home', msg = msg))



@app.route('/update_metrics', methods=['POST'])
def update_metrics():
    msg = ""
    client_id = request.form['unique_id']
    
    if 'loggedin' not in session:
        msg = "Error: User not logged in."
        flash(msg, 'error')
        return redirect(url_for('login'))
    
    if not client_id:
        msg = "Error: Client ID is required."
        flash(msg, 'error')
        return redirect(url_for('home'))

    with engine.connect() as con:
        # Check if health metrics already exist for the given unique_id
        result_metrics = con.execute(
            text("SELECT * FROM health_metrics WHERE unique_id = :client_id"),
            {'client_id': client_id}
        )
        health_metrics = result_metrics.fetchone()

        if health_metrics:
            # Update existing health metrics record
            updated_at = datetime.now()
            updated_by = session['username']

            # Retrieve form data
            form_data = {
                'recorded_date': request.form['recorded_date'],
                'health_care_facility': request.form['health_care_facility'],
                'provider_name': request.form['provider_name'],
                'provider_contact': request.form['provider_contact'],
                'weight': request.form['weight'],
                'height': request.form['height'],
                'blood_pressure': request.form['blood_pressure'],
                'fasting_blood_suger': request.form['fasting_blood_suger'],
                'random_blood_suger': request.form['random_blood_suger'],
                'temperature': request.form['temperature'],
                'respiration': request.form['respiration'],
                'pulse': request.form['pulse'],
                'spo2': request.form['spo2'],
                'urine_ketones': request.form['urine_ketones'],
                'lab_investigation_type': request.form['lab_investigation_type'],
                'lab_investigation_result': request.form['lab_investigation_result'],
                'radiograph_investigation_type': request.form['radiograph_investigation_type'],
                'radiograph_investigation_result': request.form['radiograph_investigation_result'],
                'metric_notes': request.form['metric_notes'],
                'diagnosis': request.form['diagnosis'],
                'hospitalized_for_hpt_dm': request.form['hospitalized_for_hpt_dm'],
                'complications': request.form['complications']
            }

            # Execute update query using parameterized queries to prevent SQL injection
            con.execute(
                text("""
                    UPDATE health_metrics 
                    SET updated_at = :updated_at,
                        updated_by = :updated_by,
                        recorded_date = :recorded_date,
                        health_care_facility = :health_care_facility,
                        provider_name = :provider_name,
                        provider_contact = :provider_contact,
                        weight = :weight,
                        height = :height,
                        blood_pressure = :blood_pressure,
                        fasting_blood_suger = :fasting_blood_suger,
                        random_blood_suger = :random_blood_suger,
                        temperature = :temperature,
                        respiration = :respiration,
                        pulse = :pulse,
                        spo2 = :spo2,
                        urine_ketones = :urine_ketones,
                        lab_investigation_type = :lab_investigation_type,
                        lab_investigation_result = :lab_investigation_result,
                        radiograph_investigation_type = :radiograph_investigation_type,
                        radiograph_investigation_result = :radiograph_investigation_result,
                        metric_notes = :metric_notes,
                        diagnosis = :diagnosis,
                        hospitalized_for_hpt_dm = :hospitalized_for_hpt_dm,
                        complications = :complications
                    WHERE unique_id = :client_id
                """),
                {**form_data, 'updated_at': updated_at, 'updated_by': updated_by, 'client_id': client_id}
            )

            con.commit()  # Commit the transaction after the update
            msg = "Health metrics updated successfully."
            flash(msg, 'success')
            return render_template('treatment.html', msg=msg)
        
        else:
            msg = "No health records found for the provided ID."
            flash(msg, 'error')
            return redirect(url_for('home'))


                

@app.route('/update_treatment', methods=['POST'])
def update_treatment():
    msg = ''
    client_id = request.form['unique_id']
    
    if 'loggedin' in session:
        if client_id:
            with engine.connect() as con:
                # Fetch the existing treatment record
                result_treatment = con.execute(
                    text("SELECT * FROM treatment WHERE unique_id = :client_id"), 
                    {'client_id': client_id}
                )
                treatment = result_treatment.fetchone()

                if treatment:
                    # Update treatment details
                    updated_at = datetime.now()
                    updated_by = session['username']
                    date_of_treatment = request.form['date_of_treatment']
                    treatment_type = request.form['treatment_type']
                    defaulted_treatment = request.form['defaulted_treatment']
                    health_care_facility = request.form['health_care_facility']
                    provider_contact = request.form['provider_contact']
                    treatment_plan = request.form['treatment_plan']
                    treatment_notes = request.form['treatment_notes']

                    # Execute the update within the same connection
                    con.execute(
                        text("""
                            UPDATE treatment 
                            SET updated_at = :updated_at,
                                updated_by = :updated_by,
                                date_of_treatment = :date_of_treatment,
                                treatment_type = :treatment_type,
                                defaulted_treatment = :defaulted_treatment,
                                health_care_facility = :health_care_facility,
                                provider_contact = :provider_contact,
                                treatment_plan = :treatment_plan,
                                treatment_notes = :treatment_notes
                            WHERE unique_id = :client_id
                        """),
                        {
                            'updated_at': updated_at,
                            'updated_by': updated_by,
                            'date_of_treatment': date_of_treatment,
                            'treatment_type': treatment_type,
                            'defaulted_treatment': defaulted_treatment,
                            'health_care_facility': health_care_facility,
                            'provider_contact': provider_contact,
                            'treatment_plan': treatment_plan,
                            'treatment_notes': treatment_notes,
                            'client_id': client_id
                        }
                    )
                    con.commit()  # Commit the transaction after the update
                    msg = "Treatment record updated successfully."
                    flash(msg, 'success')
                else:
                    msg = "Error: Treatment record not found."
                    flash(msg, 'error')
                
            return render_template('treatment.html')
        
        else:
            msg = "Error: No client ID provided."
            flash(msg, 'error')
            return redirect(url_for('home'))
    
    else:
        msg = "Error: User not logged in."
        flash(msg, 'error')
        return redirect(url_for('login'))


@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    msg = ''

    if request.method == 'POST' and 'unique_id' in request.form:
        unique_id = request.form['unique_id']
        purpose = request.form['purpose']
        appointment_date_time = request.form['appointment_date_time']
        message = request.form['message']

        # Record creation and update timestamps
        created_at = datetime.now()
        updated_at = datetime.now()
        created_by = session.get('username')
        updated_by = session.get('username')

        # try:
            # Insert the values into the database with parameterized query
        with engine.begin() as con:  # `begin` will ensure a commit at the end
                con.execute(
                    text("""
                        INSERT INTO appointment (
                            created_by, created_at, updated_at, updated_by, unique_id, 
                             purpose, appointment_date_time, message
                        ) VALUES (
                            :created_by, :created_at, :updated_at, :updated_by, :unique_id, 
                            :purpose, :appointment_date_time, :message
                        )
                    """),
                    {
                        'created_by': created_by,
                        'created_at': created_at,
                        'updated_at': updated_at,
                        'updated_by': updated_by,
                        'unique_id': unique_id,
                        'purpose': purpose,
                        'appointment_date_time': appointment_date_time,
                        'message': message
                    }
                )
        con.commit()    
        msg = 'Appointment Submitted Successfully'
        flash(msg, 'Appointment')
        return redirect(url_for('home', msg=msg))
        # except Exception as e:
        #     msg = 'Failed to submit appointment. Please try again.'
        #     flash(msg, 'error')

        # except Exception as e:
        #     msg = 'Please fill out the form.'
        #     flash(msg, 'Error')
    return render_template('appointment.html', msg=msg)


@app.route('/update_appointment', methods=['POST'])
def update_appointment():
    msg = ""
    client_id = request.form.get('unique_id')

    if 'loggedin' in session:
        if client_id:
            try:
                with engine.connect() as con:
                    # Check if the appointment already exists
                    result_appointment = con.execute(
                        text("SELECT * FROM appointment WHERE unique_id = :client_id"),
                        {'client_id': client_id})
                    appointment = result_appointment.fetchone()
                    con.commit()

                    if appointment:
                        # Update existing record
                        updated_at = datetime.now()
                        updated_by = session['username']
                        
                        # Retrieve form data
                        purpose = request.form['purpose']
                        appointment_date_time = request.form['appointment_date_time']
                        message = request.form['message']

                        # Execute update statement
                        con.execute(
                            text("""
                                UPDATE appointment
                                SET updated_at = :updated_at, updated_by = :updated_by, purpose = :purpose,
                                    message = :message, appointment_date_time = :appointment_date_time
                                WHERE unique_id = :client_id
                            """),
                            {
                                'updated_at': updated_at,
                                'updated_by': updated_by,
                                'purpose': purpose,
                                'message': message,
                                'appointment_date_time': appointment_date_time,
                                'client_id': client_id
                            }
                        )
                        con.commit()
                        msg = "Appointment updated successfully"
                        flash(msg, 'success')
                    else:
                        msg = "Appointment not found."
                        flash(msg, 'error')

                return render_template('appointment.html', msg=msg)
            
            except Exception as e:
                logging.error(f"Error updating appointment: {e}")
                flash("An error occurred while updating the appointment.", 'error')
                return redirect(url_for('appointment'))
        
        
@app.route('/metrics')
def metrics():
    return render_template('metrics.html')

@app.route('/treatment')
def treatment():
    return render_template('treatment.html')


@app.route('/client')
def client():
    if 'loggedin' in session:
        client_id = request.form.get('unique_id')

    if client_id:
        
        with engine.connect() as con:
            result_profile = con.execute(text("SELECT * FROM client_profile WHERE unique_id = :client_id"), {'client_id': client_id})
            con.commit()

    return render_template('client.html')


if __name__ == '__main__':
    app.run(debug=True)