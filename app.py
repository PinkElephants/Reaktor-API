from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32),  unique=True, nullable=False)
    
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
    query = db.session.query(User).order_by(User.id)
    return jsonify(json_list = [i.serialize for i in query.all()])