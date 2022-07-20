import os
import psycopg2
from dotenv import load_dotenv


def start_db():
    load_dotenv()
    name_db = os.getenv('name_db')
    user_db = os.getenv('user_db')
    password_db = os.getenv('password_db')
    host_db = os.getenv('host_db')
    port_db = os.getenv('port_db')
    con = psycopg2.connect(
        database=name_db,
        user=user_db,
        password=password_db,
        host=host_db,
        port=port_db
    )

    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS PERSONAL  
             (ID SERIAL PRIMARY KEY,
             username CHAR(100) UNIQUE NOT NULL,
             password TEXT NOT NULL);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS CAFE_TABLES  
         (ID SERIAL PRIMARY KEY,
         TYPE CHAR(100) UNIQUE NOT NULL,
         COUNT INTEGER);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS SMALL_TABLES  
         (ID SERIAL PRIMARY KEY,
         SEATS INTEGER,
         COST REAL,
         BOOKING BOOL DEFAULT FALSE,
         OPEN BOOL DEFAULT TRUE);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS MEDIUM_TABLES  
             (ID SERIAL PRIMARY KEY,
             SEATS INTEGER,
             COST REAL,
             BOOKING BOOL DEFAULT FALSE,
             OPEN BOOL DEFAULT TRUE);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS BIG_TABLES  
             (ID SERIAL PRIMARY KEY,
             SEATS INTEGER,
             COST REAL,
             BOOKING BOOL DEFAULT FALSE,
             OPEN BOOL DEFAULT TRUE);''')

    con.commit()

    con.close()

start_db()
