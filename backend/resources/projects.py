"""Project Resource."""
from flask import Blueprint, request, jsonify
from backend.util.db import get_db

BP = Blueprint('projects', __name__, url_prefix='/api/projects')


@BP.route('', methods=['GET'])
def projects_get():  # noqa
    """
    Handles GET for resource <base>/api/projects .

    :return: json data of projects
    """
    args = request.args
    id_project = args.get('id')
    id_institution = args.get('idinstitution')

    cursor = get_db().cursor()
    cursor.execute('use mydb')

    if id_project and id_institution:
        cursor.execute(
            'SELECT * FROM Project WHERE idProject = %s AND fkInstitutionProject = %s',
            (id_project, id_institution)
        )
    elif id_project:
        cursor.execute('SELECT * FROM Project WHERE idProject = %s', (id_project,))
    elif id_institution:
        cursor.execute('SELECT * FROM Project WHERE fkInstitutionProject = %s', (id_institution,))
    else:
        cursor.execute('SELECT * FROM Project')

    json_data = []
    json_names = ['id', 'name', 'webpage', 'idsmartcontract', 'idinstitution']
    for result in cursor:
        json_data.append(dict(zip(json_names, result)))

    return jsonify(json_data)


@BP.route('', methods=['POST'])
def projects_post():  # noqa
    """
    Handles POST for resource <base>/api/projects .

    :return: "{'status': 'ok'}", 200
    """

    # if not logged in:
    #   return jsonify({'error': 'not logged in'}), 403

    # ToDo: Implement POST /projects

    return jsonify({'status': 'ok'}), 200
