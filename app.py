from flask import Flask, jsonify
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
           'uuid': self.uuid,
       }

with app.app_context():
    db.create_all()

    # db.session.add(User(uuid="example"))
    # db.session.commit()

    

@app.route("/")
def hello_world():
    return jsonify(status = "I am working")



@app.route("/user")
def user_profile():
    query = db.session.query(User).order_by(User.id)
    return jsonify(json_list = [i.serialize for i in query.all()])