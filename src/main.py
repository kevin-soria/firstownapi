"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route('/newuser', methods=['POST'])
def handle_person():
    # First we get the payload json
    body = request.get_json()
    user1 = Person(username=body['username'], email=body['email'])
    db.session.add(user1)
    db.session.commit()
    return "ok", 200


@app.route('/user', methods=['GET'])
def handle_users():
    if request.method == 'GET':
        users = Person.query.all()
        if not users:
            return jsonify({'msg':'User not found'}), 404
        return jsonify( [x.serialize() for x in users] ), 200
    return "Invalid Method", 404








@app.route("/newend")
def newest_function():
    response_body = {
            "msg": "hey whats up"
        }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
