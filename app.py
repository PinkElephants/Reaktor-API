from flask import Flask, jsonify, request, abort, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import json


app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(90),  unique=True, nullable=False)

    startJob = db.Column(db.DateTime, nullable=True)
    finishJob = db.Column(db.DateTime, nullable=True)
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'         : self.id,
           'uuid'       : self.uuid,
           'start_job'  : self.startJob,
           'finish_job' : self.finishJob,           
       }

class MusicMood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(90), nullable=False)
    played_at = db.Column(db.DateTime, nullable=False)
    major_sum = db.Column(db.Float, nullable=False)
    minor_sum = db.Column(db.Float, nullable=False)
    unconf_sum = db.Column(db.Float, nullable=False)
    happyness_index = db.Column(db.Float, nullable=False)
    sadness_indes = db.Column(db.Float, nullable=False)


    def serialize(self, user_uuid):
       """Return object data in easily serializable format"""
       return {
           'id'         : self.id,
           'user_uuid'  : user_uuid,
           'played_at'  : self.played_at,
           'major_sum'  : self.major_sum,
           'minor_sum'  : self.minor_sum,     
           'unconf_sum'  : self.unconf_sum,
           'happyness_index'  : self.happyness_index,    
           'sadness_indes'  : self.sadness_indes,       
       }


with app.app_context():
    db.create_all()
    db.session.query(MusicMood).delete()
    db.session.commit()
    
    db.session.add(MusicMood(
        id = 1,
        user_uuid = "861B760D-EE8A-4906-BAF3-DCEBA08C6243",
        played_at = datetime.datetime.fromtimestamp(1667260800),
        major_sum = 0,
        minor_sum = 3,
        unconf_sum = 1,
        happyness_index = 0.0,
        sadness_indes = 0.75,
    ))
    db.session.add(MusicMood(
        id = 2,
        user_uuid = "861B760D-EE8A-4906-BAF3-DCEBA08C6243",
        played_at = datetime.datetime.fromtimestamp(1667347200),
        major_sum = 2,
        minor_sum = 0,
        unconf_sum = 0,
        happyness_index = 1,
        sadness_indes = 0,
    ))
    db.session.add(MusicMood(
        id = 3,
        user_uuid = "861B760D-EE8A-4906-BAF3-DCEBA08C6243",
        played_at = datetime.datetime.fromtimestamp(1667433600),
        major_sum = 12,
        minor_sum = 12,
        unconf_sum = 3,
        happyness_index = 0.4444444444,
        sadness_indes = 0.4444444444,
    ))
    db.session.add(MusicMood(
        id = 4,
        user_uuid = "861B760D-EE8A-4906-BAF3-DCEBA08C6243",
        played_at = datetime.datetime.fromtimestamp(1667520000),
        major_sum = 1,
        minor_sum = 1,
        unconf_sum = 0,
        happyness_index = 0.5,
        sadness_indes = 0.5,
    ))
    db.session.add(MusicMood(
        id = 5,
        user_uuid = "861B760D-EE8A-4906-BAF3-DCEBA08C6243",
        played_at = datetime.datetime.fromtimestamp(1667606400),
        major_sum = 5,
        minor_sum = 8,
        unconf_sum = 2,
        happyness_index = 0.3333333333,
        sadness_indes = 0.533333,
    ))
    db.session.commit()

@app.route("/")
def hello_world():
    return jsonify(status = "I am working")

@app.route("/user/<string:uuid_request>", methods = ['POST', 'GET'])
def user_profile(uuid_request):
    user = db.session.query(User).filter(User.uuid==uuid_request).first()

    if request.method == 'POST':
        jsonData = request.get_json()
        app.logger.info('POST body %s', jsonData)
        
        if "start_job" not in jsonData:
            jsonData["start_job"] = "09:00"
        if "finish_job" not in jsonData:
            jsonData["finish_job"] = "18:00"
            
        start_job = datetime.datetime.strptime(jsonData["start_job"], '%H:%M')
        finish_job = datetime.datetime.strptime(jsonData["finish_job"], '%H:%M')

        if user is None:
            user = User(
                uuid = uuid_request, 
                startJob = start_job, 
                finishJob=finish_job, 
                )
            db.session.add(user)
        else:
            user.startJob = start_job
            user.finishJob = finish_job

        db.session.commit()
        return Response("OK", 200)

    if user is None:
        abort(Response("User not found", 404))

    music = db.session.query(MusicMood).all()
    userData = user.serialize
    userData["music_mood"] = [mm.serialize(uuid_request) for mm in music]
    return jsonify(userData)