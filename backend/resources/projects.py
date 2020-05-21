from flask import Blueprint, request, jsonify
from backend.util.db import get_db

bp = Blueprint('projects', __name__, url_prefix='/api/projects')


@bp.route('', methods=['GET'])
def projects():
    """
    Handles the resource <base>/api/projects with GET.

    :return: json data of projects
    """
    args = request.args
    id_project = args.get('id')
    id_institution = args.get('idinstitution')

    cursor = get_db().cursor()
    cursor.execute('use mydb')

    if id_project and id_institution:
        cursor.execute('select * from Project where idProject = %s and fkInstitutionProject = %s', (id_project, id_institution))
    elif id_project:
        cursor.execute('select * from Project where idProject = %s', (id_project,))
    elif id_institution:
        cursor.execute('select * from Project where fkInstitutionProject = %s', (id_institution,))
    else:
        cursor.execute('select * from Project')

    json_data = []
    json_names = ['id', 'name', 'webpage', 'idsmartcontract', 'idinstitution']
    for result in cursor:
        json_data.append(dict(zip(json_names, result)))

    return jsonify(json_data)


@bp.route('', methods=['POST'])
def projects():
    """
    Handles the resource <base>/api/projects with POST.

    :return:
    """

    # if not logged in:
    #   return jsonify({'error': 'not logged in'}), 403

    # ToDo: Implement POST /projects

    return "ToDo"

