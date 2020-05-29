"""Project Resource."""
from flask import Blueprint, request, jsonify
from backend.database.db import DB_SESSION
from backend.database.model import Project


BP = Blueprint('projects', __name__, url_prefix='/api/projects')


@BP.route('', methods=['GET'])
def projects_get():
    """
    Handles GET for resource <base>/api/projects .

    :return: json data of projects
    """
    args = request.args
    id_project = args.get('id', type=int)
    id_institution = args.get('idinstitution')

    session = DB_SESSION()
    results = session.query(Project)

    if id_project:
        results = results.filter(Project.idProject == id_project)
    if id_institution:
        results = results.filter(Project.institution_id == id_institution)

    json_data = []
    json_names = ['id', 'name', 'webpage', 'idsmartcontract', 'idinstitution']
    for result in results:
        json_data.append(dict(zip(json_names, [
            result.idProject,
            result.nameProject,
            result.webpageProject,
            result.smartcontract_id,
            result.institution_id,
        ])))

    return jsonify(json_data)


@BP.route('/<id>', methods=['GET'])
def projects_id(id):  # pylint:disable=invalid-name,redefined-builtin
    """
    Handles GET for resource <base>/api/projects/<id> .

    :param id: id of a project
    :return: Project and all it's milestones
    """
    # ToDo: Implement GET /projects/<id>

    return jsonify({'status': str(id)})


@BP.route('', methods=['POST'])
def projects_post():
    """
    Handles POST for resource <base>/api/projects .

    :return: "{'status': 'ok'}", 200
    """
    # if not logged in:
    #   return jsonify({'error': 'not logged in'}), 403

    # ToDo: Implement POST /projects

    return jsonify({'status': 'ok'}), 200
