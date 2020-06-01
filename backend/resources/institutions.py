"""Institution Resource."""
from flask import Blueprint, request, jsonify
from backend.database.db import DB_SESSION
from backend.database.model import Institution
from sqlalchemy import exc

BP = Blueprint('institutions', __name__, url_prefix='/api/institutions')  # set blueprint name and resource path


@BP.route('', methods=['GET'])
def institutions_get():
    """
    Handles GET for resource <base>/api/institutions .

    :return: json data of institutions
    """
    id_institution = request.args.get('id', type=int)

    session = DB_SESSION()
    results = session.query(Institution)
    if id_institution:
        results = results.filter(Institution.idInstitution == id_institution)

    json_data = []
    json_names = ["id", "name", "webpage"]
    for result in results:
        json_data.append(dict(zip(json_names, [
            result.idInstitution,
            result.nameInstitution,
            result.webpageInstitution,
        ])))

    return jsonify(json_data)

@BP.route('', methods=['POST'])
def institutions_post():
    """
    Handles POST for resource <base>/api/institutions .

    :return: json response
    """

    authToken = request.headers.get('authToken')
    name = request.headers.get('name')
    webpage = request.headers.get('webpage')

    session = DB_SESSION()
    results = session.query(Institution)

    #TODO real check
    #check if logged in
    if not authToken:
        return jsonify({'status': 'Nicht eingeloggt'}), 403

    #check if name is already taken
    for result in results:
        if(name == result.nameInstitution):
            return jsonify({'status': 'Name bereits vergeben'}), 403


   
    #TODO uuid refactor + smartcontract_id
    try:
        session.add(Institution(idInstitution = 5, nameInstitution = name, webpageInstitution = webpage ,smartcontract_id = "666"))
        session.commit()
    except exc.SQLAlchemyError:
        return jsonify({'status': 'Commit error'}), 400
    

    return jsonify({'status': 'Institution wurde erstellt'}), 200