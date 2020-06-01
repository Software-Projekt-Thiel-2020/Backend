"""Project Resource."""
from flask import Blueprint, request, jsonify
<<<<<<< refs/remotes/origin/api_projects
from backend.database.db import get_db
=======
from backend.database.db import DB_SESSION
from backend.database.model import Project
from backend.database.model import Milestone

>>>>>>> local

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


@BP.route('/<id>', methods=['GET'])
def projects_id(id):  # noqa
    """
    Handles GET for resource <base>/api/projects/<id> .

    :parameter ID of a project
    :return: Project and all it's milestones
    """

    id_project = id

    try:
        if id_project:
            int(id_project)
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    session = DB_SESSION()
    results = session.query(Project)

    if id_project:
        results = results.filter(Project.idProject == id_project).one()

    milestoneresults = session.query(Milestone).filter(Milestone.project_id == id_project)

    json_ms = []
    json_names = ['id', 'idProjekt', 'goal', 'requiredVotes', 'currentVotes', "until"]
    for row in milestoneresults:
        json_ms.append(dict(zip(json_names, [
            row.idMilestone,
            row.goalMilestone,
            row.requiredVotesMilestone,
            row.currentVotesMilestone,
            row.untilBlockMilestone,
        ])))

    json_data = []
    json_names = ['id', 'name', 'webpage', 'idsmartcontract', 'idinstitution', "milestones"]
    json_data.append(dict(zip(json_names, [
        results.idProject,
        results.nameProject,
        results.webpageProject,
        results.smartcontract_id,
        results.institution_id,
        json_ms
    ])))

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
