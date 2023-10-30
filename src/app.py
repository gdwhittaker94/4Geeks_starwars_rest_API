"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os  # let's us import variables (e.g. variable at end of file!)
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
# swagger = to document and visualise our endpoints
from flask_swagger import swagger
# a way we can list from which source our API can be consulted
from flask_cors import CORS
# generates the API Live page
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Planets, Vehicles, Characters, Favorite_Characters, Favorite_Planets, Favorite_Vehicles
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


# ### HOME ENDPOINT "/" (home) ###

# Generates API Live page with all our endpoints #
@app.route('/')
def sitemap():
    # imported from utils -> lists urls and returns page content
    return generate_sitemap(app)


# ### ENDPOINTS "/users" ###

# GET 1 USER (DYNAMIC URL)
@app.route('/users/<int:user_id>', methods=['GET'])
def handle_oneUser(user_id):  # user_id = <int: user_id>
    # SQL Equiv. = SELECT * FROM Users where ID = 1
    user = Users.query.get(user_id)
    # Handle errors
    if user is None:
        return jsonify({'error': 'The user with id {} doesn\'t exist'.format(user_id)}), 400
    user_serialized = user.serialize()
    return jsonify({'msg': 'ok', 'info': user_serialized}), 200

# GET ALL USERS
@app.route('/users', methods=['GET'])
def handle_manyUsers():
    # SQL Equiv. = SELECT * FROM Users
    users = Users.query.all()
    users_serialized = list(map(lambda x: x.serialize(), users))
    return jsonify({'msg': 'ok', 'info': users_serialized})

    # FILTERING USERS
    # SQL Equiv = SELECT * FROM users WHERE ... = True:
    # filtered_users = Users.query.filter_by(is_active=True) -> would need to add this col to my table
    # filtered_users_serialize = list(map(lambda x: x.serialize(), users))
    # return jsonify({'msg': 'ok', 'info': filtered_users_serialize})

# POST (CREATE) 1 USER
@app.route('/users', methods=['POST'])
def create_user():
    # Extract JSON data
    body = request.get_json(silent=True)
    # Handle errors
    if body is None:
        return jsonify({'error': 'You must send information with the body'}), 400
    if 'name' not in body:
        return jsonify({'error': 'You must give the user a name'}), 400

    # Check: email must be unique
    if Users.query.filter_by(email=body['email']).first() is not None:
        return jsonify({'error': 'This email already exists'}), 400

    # SQL Equiv. = INSERT INTO planet(name, ...) VALUES ('example', ...)
    new_user = Users()
    new_user.name = body['name']
    new_user.country = body['country']
    new_user.birthday = body['birthday']
    new_user.email = body['email']
    new_user.password = body['password']

    db.session.add(new_user)  # adds new user to db
    db.session.commit()  # like git commit, saves changes

    return jsonify({'msg': 'ok'}), 200

# PUT (UPDATE) 1 USER
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    # SQL Equiv. = SELECT * FROM Users where ID = 1
    user = Users.query.get(user_id)
    # Handle errors
    if user is None:
        return jsonify({'error': 'The user with id {} doesn\'t exist'.format(user_id)}), 400

    # Extract JSON data
    body = request.get_json(silent=True)
    # Handle errors
    if body is None:
        return jsonify({'error': 'You must send information with the body'}), 400
    # Update relevant categories
    if "name" in body:
        user.name = body['name']
    if "country" in body:
        user.country = body['country']
    if "birthday" in body:
        user.birthday = body['birthday']
    if "email" in body:
        user.email = body['email']
    if "password" in body:
        user.password = body['password']

    db.session.commit()
    return jsonify({'msg': 'ok'}), 200

# DELETE 1 USER
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)

    # Handle errors
    if user is None:
        return jsonify({'error': 'The user with id {} doesn\'t exist'.format(user_id)}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'ok'}), 200


# ### ENDPOINTS "/planets" ###

# GET 1 PLANET (DYNAMIC URL)
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_onePlanet(planet_id):  # planet_id = <int: planet_id>
    # SQL Equiv. = SELECT * FROM Planets where ID = 1
    planet = Planets.query.get(planet_id)
    # Handle errors
    if planet is None:
        return jsonify({'error': 'The planet with id {} doesn\'t exist'.format(planet_id)}), 400
    planet_serialized = planet.serialize()
    return jsonify({'msg': 'ok', 'info': planet_serialized}), 200

# GET ALL PLANETS
@app.route('/planets', methods=['GET'])
def handle_manyPlanets():
    planets = Planets.query.all()  # SQL Equiv. = SELECT * FROM User
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify({'msg': 'ok', 'info': planets_serialized})

# POST (CREATE) 1 PLANET
@app.route('/planets', methods=['POST'])
def create_planet():
    # Extract JSON data
    body = request.get_json(silent=True)
    # Handle errors
    if body is None:
        return jsonify({'error': 'You must send information with the body'}), 400
    if 'name' not in body:
        return jsonify({'error': 'You must give the planet a name'}), 400

    # SQL Equiv. = INSERT INTO planet(name, ...) VALUES ('example', ...)
    new_planet = Planets()
    new_planet.name = body['name']
    new_planet.diameter = body['diameter']
    new_planet.rotation_period = body['rotation_period']
    new_planet.orbital_period = body['orbital_period']
    new_planet.population = body['population']
    new_planet.surface_water = body['surface_water']
    new_planet.climate = body['climate']
    new_planet.terrain = body['terrain']

    db.session.add(new_planet)  # adds new user to db
    db.session.commit()  # like git commit, saves changes

    return jsonify({'msg': 'ok'}), 200

# PUT (UPDATE) 1 PLANET
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):

    # SQL Equiv. = SELECT * FROM Planets where ID = 1
    planet = Planets.query.get(planet_id)
    # Handle errors
    if planet is None:
        return jsonify({'error': 'The planet with id {} doesn\'t exist'.format(planet_id)}), 400

    # Extract JSON data
    body = request.get_json(silent=True)
    # Handle errors
    if body is None:
        return jsonify({'error': 'You must send information with the body'}), 400
    # Update relevant categories
    if "name" in body:
        planet.name = body['name']
    if "diameter" in body:
        planet.diameter = body['diameter']
    if "rotation_period" in body:
        planet.rotation_period = body['rotation_period']
    if "orbital_period" in body:
        planet.orbital_period = body['orbital_period']
    if "population" in body:
        planet.population = body['population']
    if "surface_water" in body:
        planet.surface_water = body['surface_water']
    if "climate" in body:
        planet.climate = body['climate']
    if "terrain" in body:
        planet.terrain = body['terrain']

    db.session.commit()
    return jsonify({'msg': 'ok'}), 200

# DELETE 1 PLANET
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)

    # Handle errors
    if planet is None:
        return jsonify({'error': 'The planet with id {} doesn\'t exist'.format(planet_id)}), 400

    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg': 'ok'}), 200


# ### ENDPOINTS "/vehicles" ###

# GET 1 VEHICLE (DYNAMIC URL)
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def handle_oneVehicle(vehicle_id):  # vehicles_id = <int: vehicles_id>
    # SQL Equiv. = SELECT * FROM vehicles where ID = 1
    vehicles = Vehicles.query.get(vehicle_id)
    # Handle errors
    if vehicles is None:
        return jsonify({'error': 'The vehicles with id {} doesn\'t exist'.format(vehicle_id)}), 400
    vehicles_serialized = vehicles.serialize()
    return jsonify({'msg': 'ok', 'info': vehicles_serialized}), 200

# GET ALL VEHICLES
@app.route('/vehicles', methods=['GET'])
def handle_manyVehicles():
    vehicles = Vehicles.query.all()  # SQL Equiv. = SELECT * FROM User
    vehicles_serialized = list(map(lambda x: x.serialize(), vehicles))
    return jsonify({'msg': 'ok', 'info': vehicles_serialized})

# POST (CREATE) 1 VEHICLE
@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    # Extract JSON data
    body = request.get_json(silent=True)
    # Handle errors
    if body is None:
        return jsonify({'error': 'You must send information with the body'}), 400
    if 'name' not in body:
        return jsonify({'error': 'You must give the vehicle a name'}), 400

    # SQL Equiv. = INSERT INTO planet(name, ...) VALUES ('example', ...)
    new_vehicle = Vehicles()
    new_vehicle.name = body['name']
    new_vehicle.model = body['model']
    new_vehicle.vehicle_class = body['vehicle_class']
    new_vehicle.manufacturer = body['manufacturer']
    new_vehicle.consumables = body['consumables']
    new_vehicle.cost_in_credits = body['cost_in_credits']
    new_vehicle.crew = body['crew']
    new_vehicle.length = body['length']
    new_vehicle.max_atmosphering_speed = body['max_atmosphering_speed']
    new_vehicle.cargo_capacity = body['cargo_capacity']

    db.session.add(new_vehicle)  # adds new user to db
    db.session.commit()  # like git commit, saves changes

    return jsonify({'msg': 'ok'}), 200

# PUT (UPDATE) 1 VEHICLE
@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):

    # SQL Equiv. = SELECT * FROM Planets where ID = 1
    vehicle = Vehicles.query.get(vehicle_id)
    # Handle errors
    if vehicle is None:
        return jsonify({'error': 'The vehicle with id {} doesn\'t exist'.format(vehicle_id)}), 400

    # Extract JSON data
    body = request.get_json(silent=True)
    # Handle errors
    if body is None:
        return jsonify({'error': 'You must send information with the body'}), 400
    # Update relevant categories
    if "name" in body:
        vehicle.name = body['name']
    if "model" in body:
        vehicle.model = body['model']
    if "vehicles_class" in body:
        vehicle.vehicles_class = body['vehicles_class']
    if "manufacturer" in body:
        vehicle.manufacturer = body['manufacturer']
    if "consumables" in body:
        vehicle.consumables = body['consumables']
    if "cost_in_credits" in body:
        vehicle.cost_in_credits = body['cost_in_credits']
    if "crew" in body:
        vehicle.crew = body['crew']
    if "length" in body:
        vehicle.length = body['length']
    if "max_atmosphering_speed" in body:
        vehicle.max_atmosphering_speed = body['max_atmosphering_speed']
    if "cargo_capacity" in body:
        vehicle.cargo_capacity = body['cargo_capacity']

    db.session.commit()
    return jsonify({'msg': 'ok'}), 200

# DELETE 1 VEHICLE
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)

    # Handle errors
    if vehicle is None:
        return jsonify({'error': 'The vehicle with id {} doesn\'t exist'.format(vehicle_id)}), 400

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'msg': 'ok'}), 200


# ### ENDPOINTS "/characters" ###

# GET 1 CHARACTER (DYNAMIC URL)
@app.route('/characters/<int:character_id>', methods=['GET'])
def handle_oneCharacter(character_id):  # characters_id = <int: characters_id>
    # SQL Equiv. = SELECT * FROM characters where ID = 1
    characters = Characters.query.get(character_id)
    # Handle errors
    if characters is None:
        return jsonify({'error': 'The characters with id {} doesn\'t exist'.format(character_id)}), 400
    characters_serialized = characters.serialize()
    return jsonify({'msg': 'ok', 'info': characters_serialized}), 200

# GET ALL CHARACTERS
@app.route('/characters', methods=['GET'])
def handle_manyCharacter():
    characters = Characters.query.all()  # SQL Equiv. = SELECT * FROM User
    characters_serialized = list(map(lambda x: x.serialize(), characters))
    return jsonify({'msg': 'ok', 'info': characters_serialized})


# POST (CREATE) 1 CHARACTER
@app.route('/characters', methods=['POST'])
def create_character():
    # Extract JSON data
    body = request.get_json(silent=True)
    # Handle errors
    if body is None:
        return jsonify({'error': 'You must send information with the body'}), 400
    if 'name' not in body:
        return jsonify({'error': 'You must give the character a name'}), 400

    # SQL Equiv. = INSERT INTO character(name, ...) VALUES ('example', ...)
    new_character = Characters()
    new_character.name = body['name']
    new_character.gender = body['gender']
    new_character.height = body['height']
    new_character.mass = body['mass']
    new_character.hair_color = body['hair_color']
    new_character.eye_color = body['eye_color']
    new_character.birth_year = body['birth_year']

    db.session.add(new_character)  # adds new user to db
    db.session.commit()  # like git commit, saves changes

    return jsonify({'msg': 'ok'}), 200

# PUT (UPDATE) 1 CHARACTER
@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):

    # SQL Equiv. = SELECT * FROM Planets where ID = 1
    character = Characters.query.get(character_id)
    # Handle errors
    if character is None:
        return jsonify({'error': 'The character with id {} doesn\'t exist'.format(character_id)}), 400

    # Extract JSON data
    body = request.get_json(silent=True)
    # Handle errors
    if body is None:
        return jsonify({'error': 'You must send information with the body'}), 400
    # Update relevant categories
    if "name" in body:
        character.name = body['name']
    if "gender" in body:
        character.gender = body['gender']
    if "height" in body:
        character.height = body['height']
    if "mass" in body:
        character.mass = body['mass']
    if "hair_color" in body:
        character.hair_color = body['hair_color']
    if "eye_color" in body:
        character.eye_color = body['eye_color']
    if "birth_year" in body:
        character.birth_year = body['birth_year']

    db.session.commit()
    return jsonify({'msg': 'ok'}), 200

# DELETE 1 CHARACTER
@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Characters.query.get(character_id)

    # Handle errors
    if character is None:
        return jsonify({'error': 'The character with id {} doesn\'t exist'.format(character_id)}), 400

    db.session.delete(character)
    db.session.commit()
    return jsonify({'msg': 'ok'}), 200


# ### ENDPOINTS "/favorites" ###

# GET 1 USER FAVS
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def handle_userFavs(user_id):  # user_id = <int: user_id>

    # SQL Equiv. = SELECT * FROM Users where ID = 1
    user = Users.query.get(user_id)
    # Handle errors
    if user is None:
        return jsonify({'error': 'The user with id {} doesn\'t exist'.format(user_id)}), 400

    # SQL Equiv. = SELECT * FROM favorite_x where user_id = 1
    # Characters
    favorite_characters = db.session.query(Favorite_Characters, Characters).join(Characters).filter(Favorite_Characters.user_id == user_id).all()
    favorite_characters_serialized = []
    for favorite_item, character_item in favorite_characters:
        favorite_characters_serialized.append({'favorite_character_id': favorite_item.id,'character_info': character_item.serialize()})
    # Planets
    favorite_planets = db.session.query(Favorite_Planets, Planets).join(Planets).filter(Favorite_Planets.user_id == user_id).all()
    favorite_planets_serialized = []
    for favorite_item, planet_item in favorite_planets:
        favorite_planets_serialized.append({'favorite_planet_id': favorite_item.id,'planet_info': planet_item.serialize()})
    # Vehicles
    favorite_vehicles = db.session.query(Favorite_Vehicles, Vehicles).join(Vehicles).filter(Favorite_Vehicles.user_id == user_id).all()
    favorite_vehicles_serialized = []
    for favorite_item, vehicle_item in favorite_vehicles:
        favorite_vehicles_serialized.append({'favorite_vehicle_id': favorite_item.id,'vehicle_info': vehicle_item.serialize()})

    favorites_object = {"characters": favorite_characters_serialized,
                        "planets": favorite_planets_serialized,
                        "vehicles": favorite_vehicles_serialized}

    return jsonify({'msg': 'ok', 'user': user.serialize(), 'user_favorites': favorites_object}), 200

# GET ALL USER FAVS
@app.route('/users/favorites', methods=['GET'])
def handle_allUserFavs():  # user_id = <int: user_id>

    # SQL Equiv. = SELECT * FROM Users
    users = Users.query.all()
    users_favorites = []

    for user in users:  
        user_id = user.id
        user_favs = {
            'user_info': user.serialize(),
            'favorites': {
                'characters': [],
                'planets': [],
                'vehicles': []
            }
        }

     # SQL Equivalent = SELECT * FROM favorite_x where user_id = <user_id>
        favorite_characters = db.session.query(Favorite_Characters, Characters).join(Characters).filter(Favorite_Characters.user_id == user_id).all()
        for favorite_item, character_item in favorite_characters:
            user_favs['favorites']['characters'].append({
                'favorite_character_id': favorite_item.id,
                'character_info': character_item.serialize()
            })

        favorite_planets = db.session.query(Favorite_Planets, Planets).join(Planets).filter(Favorite_Planets.user_id == user_id).all()
        for favorite_item, planet_item in favorite_planets:
            user_favs['favorites']['planets'].append({
                'favorite_planet_id': favorite_item.id,
                'favorite_planet': planet_item.serialize()
            })

        favorite_vehicles = db.session.query(Favorite_Vehicles, Vehicles).join(Vehicles).filter(Favorite_Vehicles.user_id == user_id).all()
        for favorite_item, vehicle_item in favorite_vehicles:
            user_favs['favorites']['vehicles'].append({
                'favorite_vehicle_id': favorite_item.id,
                'vehicle_info': vehicle_item.serialize()
            })

        users_favorites.append(user_favs)

    return jsonify({'msg': 'ok', 'users_favorites': users_favorites}), 200

# POST (CREATE) NEW USER FAV CHARACTER
@app.route('/users/<int:user_id>/favorites/character', methods=['POST'])
def handle_addCharToUserFavs(user_id):  # user_id = <int: user_id>

    # 1. Dealing with incoming JSON
    body = request.get_json(silent=True)
    # Handle Errors
    if body is None:
        return jsonify({'error': 'You must include a body in the request'}), 400
    if 'character_name' not in body:
        return jsonify({'error': 'You must specify the "character_name" to add to this users favorites'}), 400

    # 2. Check User is Correct
    # SQL Equiv. = SELECT * FROM Users where ID = 1
    user = Users.query.get(user_id)
    # Handle errors
    if user is None:
        return jsonify({'error': 'You must specify an exisiting user'}), 400

    # 3. Check Character is Correct
    # SQL Equiv. = SELECT * FROM Characters where character name = body['character_name']
    favorite_character = Characters.query.filter_by(name=body['character_name']).first()
    if favorite_character is None:
        return jsonify({'error': 'You must specify an exisiting character'}), 400
    
    # once checked, now need to get character's id in order to add it to Favorite_Characters table
    favorite_character_id = favorite_character.id

    # 4. Now all is correct, add this character to user's list of favorite characters 
    new_fav_character = Favorite_Characters()
    new_fav_character.user_id = user_id
    new_fav_character.character_id = favorite_character_id

    db.session.add(new_fav_character)  # adds to db
    db.session.commit()  # like git commit, saves changes
    
    # For JSON Reply
    favorite_characters = db.session.query(Favorite_Characters, Characters).join(Characters).filter(Favorite_Characters.user_id == user_id).all()
    favorite_characters_serialized = []
    for favorite_item, character_item in favorite_characters:
        favorite_characters_serialized.append({'favorite_character_id': favorite_item.id,'character_info': character_item.serialize()})

    return jsonify({'msg': 'Favorite added', 'Favorite_Characters': favorite_characters_serialized}), 200
   
# POST (CREATE) NEW USER FAV PLANET
@app.route('/users/<int:user_id>/favorites/planet', methods=['POST'])
def handle_addPlanetToUserFavs(user_id):  # user_id = <int: user_id>

    # 1. Dealing with incoming JSON
    body = request.get_json(silent=True)
    # Handle Errors
    if body is None:
        return jsonify({'error': 'You must include a body in the request'}), 400
    if 'planet_name' not in body:
        return jsonify({'error': 'You must specify the "planet_name" to add to this users favorites'}), 400

    # 2. Check User is Correct
    # SQL Equiv. = SELECT * FROM Users where ID = 1
    user = Users.query.get(user_id)
    # Handle errors
    if user is None:
        return jsonify({'error': 'You must specify an exisiting user'}), 400

    # 3. Check Planet is Correct
    # SQL Equiv. = SELECT * FROM Planets where planet name = body['planet_name']
    favorite_planet = Planets.query.filter_by(name=body['planet_name']).first()
    if favorite_planet is None:
        return jsonify({'error': 'You must specify an exisiting planet'}), 400
    
    # once checked, now need to get planet's id in order to add it to Favorite_Planets table
    favorite_planet_id = favorite_planet.id

    # 4. Now all is correct, add this planet to user's list of favorite planets 
    new_fav_planet = Favorite_Planets()
    new_fav_planet.user_id = user_id
    new_fav_planet.planet_id = favorite_planet_id

    db.session.add(new_fav_planet)  # adds to db
    db.session.commit()  # like git commit, saves changes
    
    # For JSON Reply
    favorite_planets = db.session.query(Favorite_Planets, Planets).join(Planets).filter(Favorite_Planets.user_id == user_id).all()
    favorite_planets_serialized = []
    for favorite_item, planet_item in favorite_planets:
        favorite_planets_serialized.append({'favorite_planet_id': favorite_item.id,'planet_info': planet_item.serialize()})

    return jsonify({'msg': 'Favorite added', 'Favorite_Planets': favorite_planets_serialized}), 200
   
# POST (CREATE) NEW USER FAV VEHICLE
@app.route('/users/<int:user_id>/favorites/vehicle', methods=['POST'])
def handle_addVehicleToUserFavs(user_id):  # user_id = <int: user_id>

    # 1. Dealing with incoming JSON
    body = request.get_json(silent=True)
    # Handle Errors
    if body is None:
        return jsonify({'error': 'You must include a body in the request'}), 400
    if 'vehicle_name' not in body:
        return jsonify({'error': 'You must specify the "vehicle_name" to add to this users favorites'}), 400

    # 2. Check User is Correct
    # SQL Equiv. = SELECT * FROM Users where ID = 1
    user = Users.query.get(user_id)
    # Handle errors
    if user is None:
        return jsonify({'error': 'You must specify an exisiting user'}), 400

    # 3. Check Vehicle is Correct
    # SQL Equiv. = SELECT * FROM Planets where vehicle name = body['vehicle_name']
    favorite_vehicle = Vehicles.query.filter_by(name=body['vehicle_name']).first()
    if favorite_vehicle is None:
        return jsonify({'error': 'You must specify an exisiting vehicle'}), 400
    
    # once checked, now need to get vehicle's id in order to add it to Favorite_Planets table
    favorite_vehicle_id = favorite_vehicle.id

    # 4. Now all is correct, add this vehicle to user's list of favorite vehicles 
    new_fav_vehicle = Favorite_Vehicles()
    new_fav_vehicle.user_id = user_id
    new_fav_vehicle.vehicle_id = favorite_vehicle_id

    db.session.add(new_fav_vehicle)  # adds to db
    db.session.commit()  # like git commit, saves changes
    
    # For JSON Reply
    favorite_vehicles = db.session.query(Favorite_Vehicles, Vehicles).join(Vehicles).filter(Favorite_Vehicles.user_id == user_id).all()
    favorite_vehicles_serialized = []
    for favorite_item, vehicle_item in favorite_vehicles:
        favorite_vehicles_serialized.append({'favorite_vehicle_id': favorite_item.id,'vehicle_info': vehicle_item.serialize()})

    return jsonify({'msg': 'Favorite added', 'Favorite_Vehicles': favorite_vehicles_serialized}), 200

# DELETE USER FAV CHARACTER
@app.route('/users/<int:user_id>/favorites/character', methods=['DELETE'])
def deleteUserFavChar(user_id):

    # 1. Dealing with incoming JSON
    body = request.get_json(silent=True)
    # Handle Errors
    if body is None:
        return jsonify({'error': 'You must include a body in the request'}), 400
    if 'character_name' not in body:
        return jsonify({'error': 'You must specify the "character_name" to delete from this users favorites'}), 400

    # 2. Check User is Correct
    # SQL Equiv. = SELECT * FROM Users where ID = 1
    user = Users.query.get(user_id)
    # Handle errors
    if user is None:
        return jsonify({'error': 'You must specify an exisiting user'}), 400

    # 3. Check Character is Correct
    # SQL Equiv. = SELECT * FROM Characters where character name = body['character_name']
    character_to_delete = Characters.query.filter_by(name=body['character_name']).first()
    if character_to_delete is None:
        return jsonify({'error': 'You must specify an exisiting character'}), 400
    
    # 4. Check this user has previously favorited that Character
    fav_character = Favorite_Characters.query.filter_by(user_id=user_id, character_id=character_to_delete.id).first()
    if fav_character is None:
        return jsonify({'error': 'This user didnt favorite this character before'}), 400

    # 4. Now all is correct, delete this character from user's list of favorite characters 
    db.session.delete(fav_character)
    db.session.commit()

    # For JSON Reply
    favorite_characters = db.session.query(Favorite_Characters, Characters).join(Characters).filter(Favorite_Characters.user_id == user_id).all()
    favorite_characters_serialized = []
    for favorite_item, character_item in favorite_characters:
        favorite_characters_serialized.append({'favorite_character_id': favorite_item.id,'character_info': character_item.serialize()})

    user_name = Users.query.filter_by(id=user_id).first().name

    return jsonify({'msg': 'This character has been deleted from the users favorite characters list',
                    'user': user_name,
                    'Favorite_Characters': favorite_characters_serialized}), 200






# --------- END OF FILE -----------
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    # if PORT in .env file has a value, use that value, if not use 3000
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
