"""Project Resource."""
from flask import Blueprint, request, jsonify
from sqlalchemy import and_
from backend.database.db import get_session
from backend.database.alchemy_decl import Project


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

    session = get_session()
    result = None
    if id_project and id_institution:
        result = session.query(Project).filter(and_(Project.idProject==id_project, Project.fkInstitutionProject==id_institution))
    elif id_project:
        result = session.query(Project).filter(Project.idProject==id_project)
    elif id_institution:
        result = session.query(Project).filter(Project.fkInstitutionProject==id_institution)
    else:
        result = session.query(Project)

    json_data = []
    json_names = ['id', 'name', 'webpage', 'idsmartcontract', 'idinstitution']
    for r in result:
        json_data.append(dict(zip(json_names, [
            r.idProject, 
            r.nameProject, 
            r.webpageProject, 
            r.fkSmartContractProject,
            r.fkInstitutionProject])))

    return jsonify(json_data)


@BP.route('/<id>', methods=['GET'])
def projects_id(id):  # noqa
    """
    Handles GET for resource <base>/api/projects/<id> .
    :parameter ID of a project
    :return: Project and all it's milestones
    """

    return jsonify({'status': str(id)})


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
