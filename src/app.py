"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os  # let's us import variables (e.g. variable at end of file!)
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger                       # swagger = to document and visualise our endpoints 
from flask_cors import CORS                             # a way we can list from which source our API can be consulted
from utils import APIException, generate_sitemap        # generates the API Live page  
from admin import setup_admin
from models import db, Users, Planets, Vehicles, Characters  
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


### HOME ENDPOINT "/" (home) 

# Generates API Live page with all our endpoints #
@app.route('/')
def sitemap():
    return generate_sitemap(app) # imported from utils -> lists urls and returns page content 


### USERS ENDPOINT "/users" 

# GET 1 USER (DYNAMIC URL)
@app.route('/users/<int:user_id>', methods=['GET'])
def handle_oneUser(user_id): # user_id = <int: user_id> 
    user = Users.query.get(user_id) # SQL Equiv. = SELECT * FROM Users where ID = 1
    # Handle errors
    if user is None:
        return jsonify({'error': 'The user with id {} doesn\'t exist'.format(user_id)}), 400
    user_serialize = user.serialize()
    return jsonify({'msg': 'ok', 'info': user_serialize}), 200

# GET MULTIPLE USERS
@app.route('/users', methods=['GET'])
def handle_manyUsers(): 
    users = Users.query.all() # SQL Equiv. = SELECT * FROM User
    users_serialize = list(map(lambda x: x.serialize(), users))
    return jsonify({'msg': 'ok', 'info': users_serialize})

    # FILTERING USERS 
    # SQL Equiv = SELECT * FROM users WHERE ... = True: 
    # filtered_users = Users.query.filter_by(is_active=True) -> would need to add this col to my table 
    # filtered_users_serialize = list(map(lambda x: x.serialize(), users))
    # return jsonify({'msg': 'ok', 'info': filtered_users_serialize})
    

### ENDPOINT "/planets" 

# GET 1 PLANET (DYNAMIC URL)
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_onePlanet(planet_id): # planet_id = <int: planet_id> 
    planet = Planets.query.get(planet_id) # SQL Equiv. = SELECT * FROM Planets where ID = 1
    # Handle errors
    if planet is None:
        return jsonify({'error': 'The planet with id {} doesn\'t exist'.format(planet_id)}), 400
    planet_serialize = planet.serialize()
    return jsonify({'msg': 'ok', 'info': planet_serialize}), 200

# GET MULTIPLE PLANETS
@app.route('/planets', methods=['GET'])
def handle_manyPlanets(): 
    planets = Planets.query.all() # SQL Equiv. = SELECT * FROM User
    planets_serialize = list(map(lambda x: x.serialize(), planets))
    return jsonify({'msg': 'ok', 'info': planets_serialize})












# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000)) # if PORT in .env file has a value, use that value, if not use 3000
    app.run(host='0.0.0.0', port=PORT, debug=False)
