import mysql.connector as mysql
from app import app


def getDB(config):
    db = mysql.connect(
        host=app.config['HOST'],
        user=app.config['USER'],
        password=app.config['PASSWORD'], 
        database = app.config['DATABASE'],
    )
    return db