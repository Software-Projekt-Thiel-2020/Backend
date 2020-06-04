"""Institution Resource."""
from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from backend.database.db import DB_SESSION
from backend.database.model import Institution

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
    auth_token = request.headers.get('authToken')
    name = request.headers.get('name')
    web = request.headers.get('webpage')

    session = DB_SESSION()
    results = session.query(Institution)

    # check if logged in TODO real check
    if not auth_token:
        return jsonify({'status': 'Nicht eingeloggt'}), 403

    # check if name is already taken
    name_exist = session.query(Institution).filter(Institution.nameInstitution == name).first()
    if name_exist :
        return jsonify({'status': 'Name bereits vergeben'}), 200
  
    # Todo: idInstitution and smartcontract_id
    try:
        session.add(Institution(idInstitution=6, nameInstitution=name, webpageInstitution=web, smartcontract_id=666))
        session.commit()
    except exc.SQLAlchemyError:
        return jsonify({'status': 'Commit error'}), 400

    return jsonify({'status': 'Institution wurde erstellt'}), 200
