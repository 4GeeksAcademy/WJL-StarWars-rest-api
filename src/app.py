"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Vehicles, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints

@app.route('/')
def sitemap():
    return generate_sitemap(app)

#GET USERS

@app.route('/user', methods=['GET'])
def get_users():

    #Obtener todos los datos de una tabla/modelo en particular
    ##Fetch all records from a particular table/model
    users= User.query.all()

    # Crear una lista (de diccionarios) con los usuarios. El metodo serialize() convierte los objetos en diccionarios
    ## Create a list of dictionaries with the users. The serialize method converts the object to a dictionary
    users_list= [element.serialize() for element in users]

    return jsonify(users_list), 200

#GET CHARACTERS

@app.route('/characters', methods=['GET'])
def get_characters():

    allCharacters= Characters.query.all()
    characters_list= [element.serialize() for element in allCharacters]

    return jsonify(characters_list), 200

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_one_characters(characters_id):

    #Obtener solo un dato de una tabla basado en su llave primaria con ".query.get"
    ##Fetch one single record based on its primary key using ".query.get()"
    
    oneCharacter= Characters.query.get(characters_id)

    #Colocar "if condition" para evitar el error "AttributeError: 'NoneType'""
    ##Use "if condition" to avoid "AttributeError: 'NoneType' object has no attribute 'serialize'""
    
    if oneCharacter is None:
        return 'Character not found', 404
    return jsonify(oneCharacter.serialize()), 200

#GET PLANETS

@app.route('/planets', methods=['GET'])
def get_planets():

    allPlanets= Planets.query.all()
    planets_list= [element.serialize() for element in allPlanets]

    return jsonify(planets_list), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planets(planets_id):
    
    onePlanet= Planets.query.get(planets_id)
    
    if onePlanet is None:
        return 'Planet not found', 404
    return jsonify(onePlanet.serialize()), 200

#GET VEHICLES

@app.route('/vehicles', methods=['GET'])
def get_vehicles():

    allVehicles= Vehicles.query.all()
    vehicles_list= [element.serialize() for element in allVehicles]

    return jsonify(vehicles_list), 200

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_one_vehicles(vehicles_id):
    
    oneVehicle= Vehicles.query.get(vehicles_id)
    
    if oneVehicle is None:
        return 'Vehicle not found', 404
    return jsonify(oneVehicle.serialize()), 200

#GET FAVORITES

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():

    favoritos=Favorite.query.all()  
    favorite_list=[element.serialize() for element in favoritos]

    return jsonify(favorite_list), 200

#ADD FAVORITES
#FAVORITE PLANETS
@app.route('/favorites/planets/<int:planets_id>', methods=['POST'])
def add_favorite_planet(planets_id):
    body=request.json

    #Revisar si el planets_id existe en la tabla/modelo
    ##Check if the planets_id exists in the planets table
    planet = Planets.query.get(planets_id)
    if planet is None:
        return 'Planet not found', 404
    
    #Revisar si el user_id existe en la tabla/modelo
    ##Check if the user_id exists in the user table
    user = User.query.get(body["user_id"])
    if user is None:
        return 'User not found', 404
    
    new_favorite = Favorite(user_id=body["user_id"], favorite_planets=planets_id)

    db.session.add(new_favorite)
    db.session.commit()

    response_body={'msg':"Planeta has been added to Favorites"}

    return jsonify(response_body), 200

#FAVORITE CHARACTERS
@app.route('/favorites/characters/<int:characters_id>', methods=['POST'])
def add_favorite_character(characters_id):
    body=request.json

    #Revisar si el characters_id existe en la tabla/modelo
    ##Check if the characters_id exists in the planets table
    character = Characters.query.get(characters_id)
    if character is None:
        return 'Character not found', 404
    
    #Revisar si el user_id existe en la tabla/modelo
    ##Check if the user_id exists in the user table
    user = User.query.get(body["user_id"])
    if user is None:
        return 'User not found', 404
    
    new_favorite = Favorite(user_id=body["user_id"], favorite_characters=characters_id)

    db.session.add(new_favorite)
    db.session.commit()

    response_body={'msg':"Characters has been added to Favorites"}

    return jsonify(response_body), 200

#FAVORITE VEHICLES
@app.route('/favorites/vehicles/<int:vehicles_id>', methods=['POST'])
def add_favorite_vehicle(vehicles_id):
    body=request.json

    #Revisar si el vehicles_id existe en la tabla/modelo
    ##Check if the vehicles_id exists in the planets table
    vehicle = Vehicles.query.get(vehicles_id)
    if vehicle is None:
        return 'vehicle not found', 404
    
    #Revisar si el user_id existe en la tabla/modelo
    ##Check if the user_id exists in the user table
    user = User.query.get(body["user_id"])
    if user is None:
        return 'User not found', 404
    
    new_favorite = Favorite(user_id=body["user_id"], favorite_vehicles=vehicles_id)

    db.session.add(new_favorite)
    db.session.commit()

    response_body={'msg':"Characters has been added to Favorites"}

    return jsonify(response_body), 200

#DELETE FAVORITE PLANET
@app.route('/favorites/planets/<int:planets_id>', methods=['DELETE'])
def remove_favorite_planet(planets_id):
    body=request.json

    planet = Planets.query.get(planets_id)
    if planet is None:
        return 'Planet not found', 404
    
    user = User.query.get(body["user_id"])
    if user is None:
        return 'User not found', 404
    
    remove_favorite = Favorite.query.filter_by(
        user_id=body["user_id"], 
        favorite_planets=planets_id).first()
    
    if remove_favorite is None:
        return 'Favorite not found', 404
    
    db.session.add(remove_favorite)
    db.session.commit()

    response_body={'msg':"Planeta has been removed from Favorites"}

    return jsonify(response_body), 200

#DELETE CHARACTERS
@app.route('/favorites/characters/<int:characters_id>', methods=['DELETE'])
def remove_favorite_character(characters_id):
    body=request.json

    character = Characters.query.get(characters_id)
    if character is None:
        return 'character not found', 404
    
    user = User.query.get(body["user_id"])
    if user is None:
        return 'User not found', 404
    
    remove_favorite = Favorite.query.filter_by(
        user_id=body["user_id"], 
        favorite_characters=characters_id).first()
    
    if remove_favorite is None:
        return 'Favorite not found', 404
    
    db.session.add(remove_favorite)
    db.session.commit()

    response_body={'msg':"Character removed from Favorites"}

    return jsonify(response_body), 200

#DELETE VEHICLES
@app.route('/favorites/vehicles/<int:vehicles_id>', methods=['DELETE'])
def remove_favorite_vehicle(vehicles_id):
    body=request.json

    # vehicle = Vehicles.query.get(vehicles_id)
    # if vehicle is None:
    #     return 'vehicle not found', 404
    
    # user = User.query.get(body["user_id"])
    # if user is None:
    #     return 'User not found', 404
    
    remove_favorite = Favorite.query.filter_by(
        user_id=body["user_id"], 
        favorite_vehicles=vehicles_id).first()
    
    if remove_favorite is None:
        return 'Favorite not found', 404
    
    db.session.add(remove_favorite)
    db.session.commit()

    response_body={'msg':"Vehicle has been removed from Favorites"}

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
