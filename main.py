from flask import Flask, render_template, request, redirect
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

# Параметры подключения к PostgreSQL
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}
# DB_CONFIG = {
#     "dbname": "button_db",
#     "user": "postgres",
#     "password": "postgres",
#     "host": "localhost",
#     "port": "5432"
# }

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
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

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", clicks=None)

@app.route("/add_click", methods=["POST"])
def add_click():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO button_clicks (click_time) VALUES (%s)",
        (datetime.now(),)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/show_clicks", methods=["POST"])
def show_clicks():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, click_time FROM button_clicks ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", clicks=rows)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)