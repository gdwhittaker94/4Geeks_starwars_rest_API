from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# unique=True = has to be unique
# nullable=False = can't be ignored 

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50))
    birthday = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)

    def __repr__(self): 
        return '<id: {}, Name: {}>'.format(self.id, self.name) 

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
    crew = db.Column(db.Integer)
    max_atmosphering_speed = db.Column(db.Integer)
    cargo_capacity = db.Column(db.Integer)

    def __repr__(self): 
        return '<id: {}, Name: {}>'.format(self.id, self.name)

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

    
class Favorite_Planets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet_relationship = db.relationship(Planets)                 # not a col, tells PC where to find col
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_relationship = db.relationship(Users)

class Favorite_Characters(db.Model):
    __tablename__ = 'favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character_relationship = db.relationship(Characters)              # not a col, tells PC where to find col
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_relationship = db.relationship(Users)


class Favorite_Vehicles(db.Model):
    __tablename__ = 'favorite_vehicles'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicle_relationship = db.relationship(Vehicles)                 # not a col, tells PC where to find col
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_relationship = db.relationship(Users)

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