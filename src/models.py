from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# 'unique=True' = has to be unique
# 'nullable=False' = can't be ignored 

# def __repr__(self): = what prints out in terminal + how table data is visualised in /admin 
# def serialize(self): = allows us to convert the query object we get from flask into 
#  a dictionary and then into a JSON object 


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50))
    birthday = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __repr__(self): 
        return '<id: {}, Name: {}>'.format(self.id, self.name) 

    # what we will see when we employ the serialize function (returns a dictionary) 
    def serialize(self):  # 'self' = this user 
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "birthday": self.birthday,
            "email": self.email,
            "password": self.password
            # do not serialize the password, its a security breach
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    model = db.Column(db.String(50))
    vehicle_class = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    consumables = db.Column(db.String(50))
    cost_in_credits = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    length = db.Column(db.Float)
    max_atmosphering_speed = db.Column(db.Integer)
    cargo_capacity = db.Column(db.Integer)

    def __repr__(self): 
        return '<id: {}, Name: {}>'.format(self.id, self.name)
    
    # what we will see when we employ the serialize function (returns a dictionary) 
    def serialize(self):  # 'self' = this table 
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "consumables": self.consumables,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "length": self.length,
            "crew": self.crew,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    population = db.Column(db.Integer)
    surface_water = db.Column(db.Integer)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))

    def __repr__(self): 
        return '<id: {}, Name: {}>'.format(self.id, self.name) 

    # what we will see when we employ the serialize function (returns a dictionary) 
    def serialize(self):  # 'self' = this table 
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "surface_water": self.surface_water,
            "climate": self.climate,
            "terrain": self.terrain
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(50))

    def __repr__(self): 
        return '<id: {}, Name: {}>'.format(self.id, self.name) 
    
    # what we will see when we employ the serialize function (returns a dictionary) 
    def serialize(self):  # 'self' = this table 
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
        }
    
class Favorite_Planets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship(Planets) # not a col, tells PC where to find col

    # what we will see when we employ the serialize function (returns a dictionary) 
    def serialize(self):  # 'self' = this table 
        return {
            "id": self.id,
            "user_id": self.user,
            "planet": self.planet,
        }

class Favorite_Characters(db.Model):
    __tablename__ = 'favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character = db.relationship(Characters) # not a col, tells PC where to find col
    
    # what we will see when we employ the serialize function (returns a dictionary) 
    def serialize(self):  # 'self' = this table 
        return {
            "id": self.id,
            "user_id": self.user,
            "character": self.character,
        }
    
class Favorite_Vehicles(db.Model):
    __tablename__ = 'favorite_vehicles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicle = db.relationship(Vehicles) # not a col, tells PC where to find col
    
    # what we will see when we employ the serialize function (returns a dictionary) 
    def serialize(self):  # 'self' = this table 
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle": self.vehicle,
        }

# DEFAULT 
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False) 
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     #a method for User table, what we put is what comes out in the terminal (every time we use print)
#     def __repr__(self): 
#         return '<User id {}>'.format(self.id) 
 
#     # returns a dictionary 
#     def serialize(self):  # 'self' = this user 
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }