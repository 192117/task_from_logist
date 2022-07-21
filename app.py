import psycopg2, os
import create_db
from dotenv import load_dotenv as load
from fastapi import FastAPI, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from models import *
from auth import *
from auth_bearer import JWTBearer
from errors import error_message
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr



app = FastAPI()


load()

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

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME'),
    MAIL_TLS=False,
    MAIL_SSL=True,
    TEMPLATE_FOLDER='./templates'
)

@app.get('/show/')
async def public_show(query: ShowTableGet = Depends(ShowTableGet)):
    values = query.dict()
    try:
        cur = con.cursor()
        result = []
        if values['types'] == 'small_tables':
            cur.execute("SELECT * FROM small_tables WHERE seats>=%s and cost>=%s and cost<%s", (values['seats'],
                                                                                                values['cost1'],
                                                                                                values['cost2']))
            rows = cur.fetchall()
            for row in rows:
                result.append(
                    {'ID': row[0], 'SEATS': row[1], 'COST': row[2]})
        elif values['types'] == 'medium_tables':
            cur.execute("SELECT * FROM medium_tables WHERE seats>=%s and cost>=%s and cost<%s", (values['seats'],
                                                                                                values['cost1'],
                                                                                                values['cost2']))
            rows = cur.fetchall()
            for row in rows:
                result.append(
                    {'ID': row[0], 'SEATS': row[1], 'COST': row[2]})
        elif values['types'] == 'big_tables':
            cur.execute("SELECT * FROM big_tables WHERE seats>=%s and cost>=%s and cost<%s", (values['seats'],
                                                                                                values['cost1'],
                                                                                                values['cost2']))
            rows = cur.fetchall()
            for row in rows:
                result.append(
                    {'ID': row[0], 'SEATS': row[1], 'COST': row[2]})
        return result
    except Exception as ex:
        return error_message(ex, ex.args)

@app.post('/order/')
async def public_order(body: OrderPost, background_tasks: BackgroundTasks):
    try:
        values = body.dict()
        message = MessageSchema(subject="Order status from LogicService", recipients=[values['mail'],], template_body=values)
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message, template_name='booking.html')
    except Exception as ex:
        return error_message(ex, ex.args)


@app.get('/cancel/')
async def public_cancel(id: int, types: str, mail: EmailStr, background_tasks: BackgroundTasks):
    try:
        message = MessageSchema(subject="Order status from LogicService", recipients=[mail,],
                                template_body={'id': id, 'types': types})
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message, template_name='cancel.html')
    except Exception as ex:
        return error_message(ex, ex.args)

@app.post('/registr/')
async def public_registr(body: UserRegistrModelPost):
    values = body.dict()
    cur = con.cursor()
    cur.execute("SELECT * FROM personal WHERE username = %s", (values['username'],))
    if cur.fetchone() is None:
        try:
            hashed_password = encode_password(values['password1'])
            cur.execute("INSERT INTO personal (username, password) VALUES (%s, %s)", (values['username'], hashed_password))
            con.commit()
            return {'username': values['username'], 'password': values['password1']}
        except Exception as ex:
            return error_message(ex, ex.args)
    else:
        return error_message('This username is already busy!')

@app.post('/login/')
async def privat_login(body: UserLoginModelPost):
    values = body.dict()
    cur = con.cursor()
    cur.execute("SELECT * FROM personal WHERE username = %s", (values['username'],))
    data = cur.fetchone()
    if data is None:
        return error_message('This username is not registered.')
    else:
        if (not verify_password(values['password'], data[-1])):
            return error_message('Invalid password')
        access_token = encode_token(values['username'])
        refresh_token = encode_refresh_token(values['username'])
        return {'access_token': access_token, 'refresh_token': refresh_token}

@app.post('/refresh_token/', dependencies=[Depends(JWTBearer())])
async def refresh_token(refresh: str):
    new_token = refr_token(refresh)
    return {'access_token': new_token}

@app.get('/show_all/', dependencies=[Depends(JWTBearer())])
async def privat_close():
    try:
        result = {}
        result.setdefault('SMALL_TABLES', [])
        result.setdefault('MEDIUM_TABLES', [])
        result.setdefault('BIG_TABLES', [])
        cur = con.cursor()
        cur.execute("SELECT * FROM small_tables")
        rows = cur.fetchall()
        for row in rows:
            result['SMALL_TABLES'].append({'ID': row[0], 'SEATS': row[1], 'COST': row[2], 'BOOKING': row[3], 'OPEN': row[4]})
        cur.execute("SELECT * FROM medium_tables")
        rows = cur.fetchall()
        for row in rows:
            result['MEDIUM_TABLES'].append(
                {'ID': row[0], 'SEATS': row[1], 'COST': row[2], 'BOOKING': row[3], 'OPEN': row[4]})
        cur.execute("SELECT * FROM big_tables")
        rows = cur.fetchall()
        for row in rows:
            result['BIG_TABLES'].append(
                {'ID': row[0], 'SEATS': row[1], 'COST': row[2], 'BOOKING': row[3], 'OPEN': row[4]})
        con.commit()
        return result
    except Exception as ex:
        return error_message(ex, ex.args)

@app.post('/close/', dependencies=[Depends(JWTBearer())])
async def privat_price(body: UserCloseModelPost):
    values = body.dict()
    cur = con.cursor()
    try:
        if values['types'] == 'small_tables':
            cur.execute("UPDATE small_tables set open=%s WHERE id=%s", (False, values['id']))
        elif values['types'] == 'medium_tables':
            cur.execute("UPDATE medium_tables set open=%s WHERE id=%s", (False, values['id']))
        elif values['types'] == 'big_tables':
            cur.execute("UPDATE big_tables set open=%s WHERE id=%s", (False, values['id']))
        con.commit()
    except Exception as ex:
        return error_message(ex, ex.args)

@app.post('/change_price/', dependencies=[Depends(JWTBearer())])
async def privat_price(body: UserChangePriceModelPost):
    values = body.dict()
    cur = con.cursor()
    try:
        if values['types'] == 'small_tables':
            cur.execute("UPDATE small_tables set cost=%s WHERE id=%s", (values['cost'], values['id']))
        elif values['types'] == 'medium_tables':
            cur.execute("UPDATE medium_tables set cost=%s WHERE id=%s", (values['cost'], values['id']))
        elif values['types'] == 'big_tables':
            cur.execute("UPDATE big_tables set cost=%s WHERE id=%s", (values['cost'], values['id']))
        con.commit()
    except Exception as ex:
        return error_message(ex, ex.args)

@app.post('/add_tables/', dependencies=[Depends(JWTBearer())])
async def privat_add(body: UserAddModelPost):
    values = body.dict()
    try:
        cur = con.cursor()
        cur.execute("SELECT count FROM CAFE_TABLES WHERE type=%s", (values['types'],))
        row = cur.fetchone()
        if row is None:
            cur.execute("INSERT INTO cafe_tables (count, type) values(%s, %s)", (values['count'], values['types']))
            con.commit()
        else:
            cur.execute("UPDATE cafe_tables SET count=%s WHERE type=%s", (values['count']+row[0], values['types']))
            con.commit()
        datas = [(values['seats'], values['cost'], False, True) for x in range(values['count'])]
        args = ','.join(cur.mogrify("(%s, %s, %s, %s)", x).decode('utf-8') for x in datas)
        if values['types'] == 'small_tables':
            cur.execute("INSERT INTO small_tables (seats, cost, booking, open) VALUES " + (args))
        elif values['types'] == 'medium_tables':
            cur.execute("INSERT INTO medium_tables (seats, cost, booking, open) VALUES " + (args))
        elif values['types'] == 'big_tables':
            cur.execute("INSERT INTO big_tables (seats, cost, booking, open) VALUES " + (args))
        con.commit()
    except Exception as ex:
        return error_message(ex, ex.args)

@app.post('/change_table/', dependencies=[Depends(JWTBearer())])
async def privat_change(body: UserChangeTableModelPost):
    values = body.dict()
    cur = con.cursor()
    try:
        if values['types'] == 'small_tables':
            cur.execute("UPDATE small_tables SET seats=%s , cost=%s WHERE id=%s", (values['seats'],
                                                                                     values['cost'], values['id']))
        elif values['types'] == 'medium_tables':
            cur.execute("UPDATE medium_tables SET seats=%s , cost=%s WHERE id=%s", (values['seats'],
                                                                                      values['cost'], values['id']))
        elif values['types'] == 'big_tables':
            cur.execute("UPDATE big_tables SET seats=%s , cost=%s WHERE id=%s", (values['seats'],
                                                                                   values['cost'], values['id']))
        con.commit()
    except Exception as ex:
        return error_message(ex, ex.args)

@app.post('/booking/', dependencies=[Depends(JWTBearer())])
async def booking_change(body: UserBookingPost):
    values = body.dict()
    cur = con.cursor()
    try:
        if values['types'] == 'small_tables':
            cur.execute("UPDATE small_tables set booking=%s WHERE id=%s", (values['booking'], values['id']))
        elif values['types'] == 'medium_tables':
            cur.execute("UPDATE medium_tables set booking=%s WHERE id=%s", (values['booking'], values['id']))
        elif values['types'] == 'big_tables':
            cur.execute("UPDATE big_tables set booking=%s WHERE id=%s", (values['booking'], values['id']))
        con.commit()
    except Exception as ex:
        return error_message(ex, ex.args)

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
        'Event': 'Error',
        'Detail': str(exc),
        'Arguments': []
    },
    )