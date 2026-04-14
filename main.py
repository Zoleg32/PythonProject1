# from flask import Flask, render_template, request, redirect
# import psycopg2
# from datetime import datetime
# import os
#
# app = Flask(__name__)
#
# # Параметры подключения к PostgreSQL
# DB_CONFIG = {
#     "dbname": os.getenv("DB_NAME"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "host": os.getenv("DB_HOST"),
#     "port": os.getenv("DB_PORT")
# }
# # DB_CONFIG = {
# #     "dbname": "button_db",
# #     "user": "postgres",
# #     "password": "postgres",
# #     "host": "localhost",
# #     "port": "5432"
# # }
#
# def init_db():
#     conn = psycopg2.connect(**DB_CONFIG)
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS button_clicks (
#             id SERIAL PRIMARY KEY,
#             click_time TIMESTAMP NOT NULL
#         )
#     """)
#     conn.commit()
#     cur.close()
#     conn.close()
#
# @app.route("/", methods=["GET"])
# def index():
#     return render_template("index.html", clicks=None)
#
# @app.route("/add_click", methods=["POST"])
# def add_click():
#     conn = psycopg2.connect(**DB_CONFIG)
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO button_clicks (click_time) VALUES (%s)",
#         (datetime.now(),)
#     )
#     conn.commit()
#     cur.close()
#     conn.close()
#     return redirect("/")
#
# @app.route("/show_clicks", methods=["POST"])
# def show_clicks():
#     conn = psycopg2.connect(**DB_CONFIG)
#     cur = conn.cursor()
#     cur.execute("SELECT id, click_time FROM button_clicks ORDER BY id DESC")
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#     return render_template("index.html", clicks=rows)
#
# if __name__ == "__main__":
#     init_db()
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask, render_template, request, redirect
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)


# Универсальная конфигурация для Railway и локальной разработки
def get_db_config():
    # Проверяем, запущено ли в Railway (есть переменная RAILWAY_ENVIRONMENT)
    database_url = "postgresql://postgres:nbCxFJHwjXaHiMfhNRhiKAgUZRddVpwY@postgres.railway.internal:5432/railway"
    # if database_url:
    return database_url
    # if os.getenv("RAILWAY_ENVIRONMENT"):
    #     # Railway предоставляет DATABASE_URL


    # Локальная разработка или кастомные переменные
    # return {
    #     "dbname": os.getenv("button_db"),
    #     "user": os.getenv("postgres"),
    #     "password": os.getenv("nbCxFJHwjXaHiMfhNRhiKAgUZRddVpwY"),
    #     "host": os.getenv("monorail.proxy.rlwy.net"),
    #     "port": os.getenv("18740")
    # }


def get_db_connection():
    config = get_db_config()
    return psycopg2.connect(config,sslmode='require')


def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS button_clicks (
                id SERIAL PRIMARY KEY,
                click_time TIMESTAMP NOT NULL
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", clicks=None)


@app.route("/add_click", methods=["POST"])
def add_click():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO button_clicks (click_time) VALUES (%s)",
            (datetime.now(),)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error adding click: {e}")
    return redirect("/")


@app.route("/show_clicks", methods=["POST"])
def show_clicks():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, click_time FROM button_clicks ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("index.html", clicks=rows)
    except Exception as e:
        print(f"Error showing clicks: {e}")
        return render_template("index.html", clicks=None)


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 5000))  # Railway использует PORT
    app.run(host="0.0.0.0", port=port)



# from flask import Flask, render_template, request, json, jsonify, redirect
# import threading
# from datetime import datetime
# import time
#
# import json
# app = Flask(__name__)
# counter = 1
# Temperature1=0.0
# Temperature2=0.0
# Manual = False
# State = False
# Min_level=21.1
# Max_level=22.3
# room=True
# room1=""
# room2=""
# AV=""
# time_buffer = []
# temp_buffer = []
# def upd_heat():
#     global State
#     if Temperature1 < Min_level:
#         State = True
#     elif Temperature1 > Max_level:
#         State = False
# def set_min(value):
#     global Min_level
#     if float(value) < Max_level:
#         Min_level = float(value)
#         upd_heat()
#
# def set_max(value):
#     global Max_level
#     if float(value) > Min_level:
#         Max_level = float(value)
#         upd_heat()
#
# @app.route('/')
# def index():
#     global AV,room1,room2
#     if Manual:
#         AV="checked"
#     else:
#         AV = ""
#     if room:
#         room1="checked"
#         room2=""
#     else:
#         room1=""
#         room2="checked"
#     templateData = {'Temperature1':Temperature1,'Temperature2':Temperature2,'Manual':Manual,
#                     'State':State,'N1':Min_level,'N2':Max_level,'AV':AV,'ROOM1':room1,'ROOM2':room2}
#     return render_template('index.html', 	**templateData)
#
# @app.route('/getTemp')
# def temp_info():
#     x = [Temperature1, Temperature2, Manual, State]
#     return jsonify(x)
#
# @app.route('/relay_switch')
# def rel_switch():
#     global State
#     if Manual:
#         State=not State
#     x = [State]
#     return jsonify(x)
#
# @app.route('/Hating', methods=['GET', 'POST'])
# def Hating():
#     global AV,room1,room2
#     if Manual:
#         AV="checked"
#     else:
#         AV = ""
#     if room:
#         room1="checked"
#         room2=""
#     else:
#         room1=""
#         room2="checked"
#     templateData = {'Temperature1': Temperature1, 'Temperature2': Temperature2, 'Manual': Manual,
#                     'State': State, 'N1': Min_level, 'N2': Max_level, 'AV': AV, 'ROOM1': room1,'ROOM2': room2}
#     return render_template("index.html", **templateData)
#
# @app.route('/setLimits', methods=['GET', 'POST'])
# def limits():
#     global Min_level
#     global Max_level
#     global Manual,room
#     if request.method == 'POST':
#         set_min(request.form.get('min_lim'))
#         set_max(request.form.get('max_lim'))
#         Manual=bool(request.form.get('avto'))
#         if(request.form.get('r_room')=='on'):
#             room=True
#         else:
#             room=False
#         # x = [Min_level, Max_level, Manual, room, not room]
#     # return jsonify(x)
#     return redirect('/Hating')
#
# # GET requests will be blocked
# @app.route('/update_sensor', methods=['POST'])
# def json_example():
#     global Temperature1
#     request_data=request.get_json()
#     # request_data = request.data
#     # str_request_data=request_data.decode('cp1251')
#     # str_request_data1=json.loads(str_request_data)
#     # Temperature1=float(str_request_data1["Temperature"])
#     Temperature1 = float(request_data["Temperature"])
#     if Manual==False:
#         upd_heat()
#     return "Ok"
# @app.route('/getChartData')
# def chart_info():
#     x = [Min_level, Max_level, time_buffer, temp_buffer]
#     return jsonify(x)
# # def gui():
# #     while True:
# #         print("Hello!")
# #         if(Temperature1>0):
# #             if(len(temp_buffer)<600):
# #                 time_buffer.append(datetime.today())
# #                 temp_buffer.append(Temperature1)
# #             else:
# #                 time_buffer.pop(0)
# #                 temp_buffer.pop(0)
# #                 time_buffer.append(datetime.today())
# #                 temp_buffer.append(Temperature1)
# #         time.sleep(10)
#
# if __name__ == "__main__":
#     # thr1 = threading.Thread(target=gui, daemon=True)
#     # thr1.start()
#     # t = Timer(10, gui)
#     # t.start()
#     # gui()
#     app.run(host = '0.0.0.0', port=5000)