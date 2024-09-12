import os
from dotenv import load_dotenv

load_dotenv()

environ=os.getenv('ENV')
secret_key=os.getenv('SECRET_KEY')
if environ=='local':
    dbuser=os.getenv('DATABASE_USER_LOCAL')
    dbport=os.getenv('DATABASE_PORT_LOCAL')
    dbpassword=os.getenv('DATABASE_PASSWORD_LOCAL')
    dbhost=os.getenv('DATABASE_HOST_LOCAL')
    dbname=os.getenv('DATABASE_NAME_LOCAL')
if environ=='production':
    dbuser=os.getenv('DATABASE_USER_PRODUCTION')
    dbport=os.getenv('DATABASE_PORT_PRODUCTION')
    dbpassword=os.getenv('DATABASE_PASSWORD_PRODUCTION')
    dbhost=os.getenv('DATABASE_HOST_PRODUCTION')
    dbname=os.getenv('DATABASE_NAME_PRODUCTIONL') 
    
