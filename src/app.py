"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os  # let's us import variables (e.g. variable at end of file!)
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger                # sirve para documentar y visualizar nuestros endpoints
from flask_cors import CORS                      # una manera en la que podemos listar desde qué fuente se puede consultar nuestra API
from utils import APIException, generate_sitemap # 
from admin import setup_admin
from models import db, Users 
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# MIGRATE 
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# ENDPOINT "/" (home) --> Generates API Live page with all our endpoints ###
@app.route('/')
def sitemap():
    return generate_sitemap(app) # imported from utils -> lists urls and returns page content 


### ENDPOINT "/user" ###
@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000)) # if PORT in .env file has a value, use that value, if not use 3000
    app.run(host='0.0.0.0', port=PORT, debug=False)
