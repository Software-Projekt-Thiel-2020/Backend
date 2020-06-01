"""Institution Resource."""
from flask import Blueprint, request, jsonify
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
