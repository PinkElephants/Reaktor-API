import mysql.connector as mysql



def getDB(config):
    db = mysql.connect(
        host=config['HOST'],
        port=config['PORT'],
        user=config['USER'],
        password=config['PASSWORD'], 
        database =config['DATABASE'],
    )
    return db