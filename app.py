from flask import Flask
from db import getDB
import json

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route("/")
def hello_world():
    with getDB(app.config) as db:
        cursor = db.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        return "test"