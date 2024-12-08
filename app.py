from flask import Flask

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import mysql.connector

app = Flask(__name__,static_url_path='/static')
app.secret_key = 'aWcgfjbbj78#$@^&_+9_=0908BD3E3EF2DE50A52F1D82FC4828E1584E412D5608'

def connect_db():
    """ Connect to the MySQL database """
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return connection


