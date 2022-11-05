from flask import Flask, jsonify, request, abort, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32),  unique=True, nullable=False)
    startJob = db.Column(db.DateTime, nullable=True)
    finishJob = db.Column(db.DateTime, nullable=True)
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'         : self.id,
           'uuid'       : self.uuid,
           'start_job'  : self.finishJob,
           'finish_job' : self.finishJob,           
       }

with app.app_context():
    db.create_all()
    # db.session.add(User(uuid="example"))
    # db.session.commit()

    

@app.route("/")
def hello_world():
    return jsonify(status = "I am working")

@app.route("/user/<string:uuid_request>", methods = ['POST', 'GET'])
def user_profile(uuid_request):
    user = db.session.query(User).filter(User.uuid==uuid_request).first()
    if user is None:
        abort(Response("User not found", 404))

    if request.method == 'POST':
        data = request.get_json()
        return "NOT READY YET"


    return jsonify(user.serialize)