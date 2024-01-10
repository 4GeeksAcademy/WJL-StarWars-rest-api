from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorites = db.relationship("Favorite", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

##CHARACTERS MODEL
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    homeworld = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String, nullable=False)
    eye_color = db.Column(db.String, nullable=False)

    planets = db.relationship("Planets", back_populates="characters")
    favorites = db.relationship("Favorite", back_populates="characters")

    def __repr__(self):
        return '<Characters %r>' % self.name
    
    def serialize(self):
        return {
           "id": self.id,
           "name": self.name,
           "homeworld": self.homeworld,
           "birth_year": self.birth_year,
           "height": self.height,
           "weight": self.weight,
           "hair_color": self.hair_color,
           "eye_color": self.eye_color
        }
    
##PLANETS MODEL
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)

    characters = db.relationship("Characters", back_populates="planets")
    favorites = db.relationship("Favorite", back_populates="planets")

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
           "id": self.id,
           "name": self.name,
           "climate": self.climate,
           "gravity": self.gravity,
           "population": self.population,
           "orbital_period": self.orbital_period
        }
    
##VEHICLES MODEL
class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    max_passengers = db.Column(db.Integer, nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    max_speed = db.Column(db.Integer)

    favorites = db.relationship("Favorite", back_populates="vehicles")

    def __repr__(self):
        return '<Vehicles %r>' % self.name
    
    def serialize(self):
        return {
           "id": self.id,
           "name": self.name,
           "max_passengers": self.max_passengers,
           "cost_in_credits": self.cost_in_credits,
           "max_speed": self.max_speed
        }
    
##FAVORITES MODEL
class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    #ForeignKey debe ser definida con el nombre de la tabla y el atributo a usar
    #ForeignKey DEBE SER la primary_key en la otra tabla
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    favorite_characters = db.Column(db.Integer, db.ForeignKey("characters.id"))
    favorite_planets = db.Column(db.Integer, db.ForeignKey("planets.id"))
    favorite_vehicles = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    
    user = db.relationship("User", back_populates="favorites")
    characters = db.relationship("Characters", back_populates="favorites")
    planets = db.relationship("Planets", back_populates="favorites")
    vehicles = db.relationship("Vehicles", back_populates="favorites")

    def __init__(self,user_id,favorite_characters=None,favorite_planets=None):
        self.user_id=user_id
        self.favorite_characters=favorite_characters
        self.favorite_planets=favorite_planets


    def __repr__(self):
        return '<Favorite %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
    }