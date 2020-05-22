"""Institution Resource."""
from flask import Blueprint, request, jsonify
from backend.util.db import get_db

BP = Blueprint('institutions', __name__, url_prefix='/api/institutions')  # set blueprint name and resource path


@BP.route('', methods=['GET'])
def institutions_get():  # noqa
    """Handles GET for resource <base>/api/institutions .

    :return: json data of institutions
    """
    id_institution = request.args.get('id', default=0, type=int)

    cursor = get_db().cursor()
    cursor.execute('use mydb;')

    if id_institution == 0:
        cursor.execute('SELECT idInstitution, nameInstitution, webpageInstitution FROM Institution;')
        data = cursor.fetchall()
    else:
        cursor.execute(
            'SELECT idInstitution, nameInstitution, webpageInstitution FROM Institution WHERE idInstitution = %s',
            (id_institution,)
        )
        data = cursor.fetchall()

    names = ["id", "name", "webpage"]
    json_data = []
    for result in data:
        json_data.append(dict(zip(names, result)))

    return jsonify(json_data)
