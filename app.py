from flask import Flask
from db import getDB
import json

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route("/")
def hello_world():
    db = getDB(app.config)
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    return json.dump(databases)