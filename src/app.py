"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# AQUI VA EL CODIGO DE LLAMAR A LOS MIEMBROS
@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200


# AQUI VA EL CODIGO DE AGREGAR UN MIEMBRO
@app.route('/add-members', methods=['POST'])
def add_member():
    # this is how you can use the Family datastructure by calling its methods
    member = {
        "id": request.json.get("id"),
        "first_name": request.json.get("first_name"),
        "age": request.json.get("age"),
        "lucky_numbers": request.json.get("lucky_numbers")
    }

    response = jackson_family.add_member(member)
    return jsonify("Usuario Creado"), 200



@app.route('/member/<int:id>', methods=['DELETE'])

def deleteOneMember(id):
    estado = jackson_family.delete_member(id)
     
    if estado == True:
        return jsonify({"done": True}), 200
    else:
        return jsonify("Ocurrió un error al eliminar el miembro"), 400



@app.route('/member/<int:id>', methods=['GET'])
def getOneMember(id):
    member = jackson_family.get_member(id)
    return member

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)