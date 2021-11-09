# from requests import request
import json
from flask import Flask, request,  jsonify
from datetime import datetime
import pyodbc


app = Flask(__name__)

server = 'dblocator.database.windows.net'
database = 'locatorserver'
username = 'AdminLocator'
password = 'LovelyLocator1!'
driver = '{ODBC Driver 17 for SQL Server}'

sCon = 'DRIVER='+driver+';SERVER=tcp:'+server + \
    ';PORT=1433;DATABASE='+database+';UID='+username+';PWD=' + password


def InsertWifi(ssid, mac, level, phoneid, dt):
    try:
        con = pyodbc.connect(sCon)
        mycursor = con.cursor()
        sql = "INSERT INTO dbo.Wifi(ssid, mac, level, phoneid,dt) VALUES (?,?,?,?,?) "

        mycursor.execute(sql, (ssid, mac, level, phoneid, dt))
        con.commit()
        con.close()
        return "Succeded"
    except Exception as ex:
        return str(ex)


def InsertBluetooth(name, code, address, rssi, phoneid, dt):
    try:
        con = pyodbc.connect(sCon)
        mycursor = con.cursor()
        sql = "INSERT INTO dbo.Bluetooth(namex, codex,addressx,rssi,phoneid,dt) VALUES (?,?,?,?,?,?) "

        mycursor.execute(sql, (name, code, address, rssi, phoneid, dt))
        con.commit()
        con.close()
        return "Succeded"
    except Exception as ex:
        return str(ex)


def InsertLocation(lot, lat, dt, phoneid, accuracy, speed):
    try:
        con = pyodbc.connect(sCon)
        mycursor = con.cursor()
        sql = "INSERT INTO dbo.Location(Longitute, Latitude,dt,phoneid,accuracy,speed) VALUES (?,?,?,?,?,?) "

        mycursor.execute(sql, (lot, lat, dt, phoneid, accuracy, speed))
        con.commit()
        con.close()
        return "Succeded"
    except Exception as ex:
        return str(ex)


@app.route("/testconnection")
def TestConnectio():
    return "Works"


@app.route("/bluetooth", methods=['POST'])
def bluetooth():
    data = request.get_data()
    sData = data.decode('utf-8')
    d = json.loads(sData)
    name = d['name']
    code = d['code']
    address = d['address']
    rssi = d['rssi']
    phoneid = d['phoneid']
    dt = d['dt']
    try:
        date_time_obj = datetime. strptime(dt, '%d/%m/%y %H:%M:%S')
    except Exception as ex:
        print(ex)
    return InsertBluetooth(name, code, address, rssi, phoneid, date_time_obj)


@app.route("/wifi", methods=['POST'])
def wifi():
    data = request.get_data()
    sData = data.decode('utf-8')
    d = json.loads(sData)
    ssid = d['ssid']
    mac = d['mac']
    level = d['level']
    phoneid = d['phoneid']
    dt = d['dt']
    try:
        date_time_obj = datetime. strptime(dt, '%d/%m/%y %H:%M:%S')
    except Exception as ex:
        print(ex)
    return InsertWifi(ssid, mac, level, phoneid, date_time_obj)


@ app.route("/location", methods=['POST'])
def location():

    data = request.get_data()
    sData = data.decode('utf-8')
    d = json.loads(sData)
    x = 1
    Longitute = d['longitude']
    Latitude = d['latitude']
    dt = d['datetime']
    phoneid = d['phoneid']
    accuracy = d['accuracy']
    speed = d['speed']
    try:
        date_time_obj = datetime. strptime(dt, '%d/%m/%y %H:%M:%S')
    except Exception as ex:
        print(ex)

    return InsertLocation(Longitute, Latitude, date_time_obj, phoneid, accuracy, speed)


@ app.route("/getName")
def getName():
    dic = {}
    dic["name"] = "xxxx"
    dic["age"] = 23
    dic["num"] = 17
    data = json.dumps(dic)

    return data


@ app.route("/")
def hello():
    try:
        con = pyodbc.connect(sCon)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM test")
        rows = cursor.fetchall()
        s = ""
        for row in rows:
            for field in row:
                s += str(field)+" "

        print("Handling request to home page.")
        con.close()
        return "Hello, Azure2!"+s
    except Exception as ex:
        return (str(ex))


# @app.route("/location", methods=['POST'])
# def Location():
#     try:
#         content = request.get_json()
#         lot = content["longitude"]
#         lat = content["latitude"]
#         sdt = content["datetime"]
#         phoneid = content["phoneid"]
#         dt = datetime.strptime(sdt, '%d/%m/%y %H:%M:%S')
#         InsertLocation(lot, lat, phoneid, dt)

#         data = json.dumps(content)
#         print(data)
#         # datetime = request.form.get('datetime')
#         # longitude = request.form.get('longitude')
#         # Latitude = request.form.get('latitude')
#         # phoneid = request.form.get('phoneid')
#     except Exception as ex:
#         print(ex)

# app.run()
