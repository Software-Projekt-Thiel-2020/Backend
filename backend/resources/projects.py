"""Project Resource."""
import json

from flask import Blueprint, request, jsonify
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from backend.database.db import DB_SESSION
from backend.database.model import Milestone
from backend.database.model import Project

BP = Blueprint('projects', __name__, url_prefix='/api/projects')


@BP.route('', methods=['GET'])
def projects_get():
    """
    Handles GET for resource <base>/api/projects .

    :return: json data of projects
    """
    id_project = request.args.get('id')
    id_institution = request.args.get('idinstitution')

    try:
        if id_project:
            int(id_project)
        if id_institution:
            int(id_institution)
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

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
def projects_id(id):  # noqa
    """
    Handles GET for resource <base>/api/projects/<id> .

    :parameter id of a project
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

    try:
        if id_project:
            results = results.filter(Project.idProject == id_project).one()
    except NoResultFound:
        return jsonify(), 404
    except SQLAlchemyError:
        return jsonify(), 200

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

    return jsonify(json_data), 200


@BP.route('', methods=['POST'])
def projects_post():
    """
    Handles POST for resource <base>/api/projects .

    :return: "{'status': 'ok'}", 200
    """
    # if not logged in:
    #   return jsonify({'error': 'not logged in'}), 403

    # ToDo: Implement POST /projects

    auth_token = request.headers.get('authToken', default=None)
    name = request.headers.get('name', default=None)
    webpage = request.headers.get('webpage', default=None)
    id_institution = request.headers.get('idInstitution', default=None)
    goal = request.headers.get('goal', default=None)
    required_votes = request.headers.get('requiredVotes', default=None)
    until = request.headers.get('until', default=None)
    milestones = request.headers.get('milestones', default="[]")

    if auth_token is None:
        return jsonify({'error': 'Not logged in'}), 403

    if name is None or goal is None or required_votes is None or until is None:
        return jsonify({'error': 'Missing parameter'}), 403

    session = DB_SESSION()

    max_ms_v = int(session.query(func.max(Milestone.idMilestone)).one()[0])
    max_pr_v = int(session.query(func.max(Project.idProject)).one()[0])

    try:
        session.add(Project(
            idProject=(max_pr_v + 1),
            nameProject=name,
            webpageProject=webpage,
            smartcontract_id=1,  # ToDo: ist das immer 1?
            institution_id=id_institution
        ))
        session.commit()
    except SQLAlchemyError:
        return jsonify({'status': 'Commit error - Project'}), 400

    ms_json = json.loads(milestones)
    try:
        for milestone in ms_json:
            max_ms_v += 1
            session.add(Milestone(
                idMilestone=max_ms_v,
                goalMilestone=milestone['goal'],
                requiredVotesMilestone=milestone['requiredVotes'],
                currentVotesMilestone=0,
                untilBlockMilestone=milestone['until'],
                project_id=max_pr_v + 1
            ))
        session.commit()
    except SQLAlchemyError:
        return jsonify({'status': 'Database error!'}), 400
    except KeyError:
        return jsonify({'status': 'Unknown Key'}), 400

    return jsonify({'status': 'ok'}), 201


@BP.route('/<id>', methods=['PATCH'])
def projects_patch(id):  # pylint:disable=invalid-name,redefined-builtin
    """
    Handles PATCH for resource <base>/api/projects/<id> .

    :return: "{'status': 'ok'}", 200
    """
    # if not logged in:
    #   return jsonify({'error': 'not logged in'}), 403

    # ToDo: Implement POST /projects

    auth_token = request.headers.get('authToken', default=None)
    webpage = request.headers.get('webpage', default=None)
    milestones = request.headers.get('milestones', default="")

    if auth_token is None:
        return jsonify({'error': 'Not logged in'}), 403

    session = DB_SESSION()

    idexists = session.query(func.count(Project.idProject)).one()[0]

    if idexists == 0:
        return jsonify({'error': 'Project doesnt exist'}), 403

    # TODO uuid refactor + smartcontract_id

    try:
        if webpage is not None:
            session.query(Project).filter(Project.idProject == id).update({Project.webpageProject: webpage})
            session.commit()
    except SQLAlchemyError:
        return jsonify({'status': 'Commit error - Milestone'}), 400

    max_ms_v = int(session.query(func.max(Milestone.idMilestone)).one()[0])

    ms_json = json.loads(milestones)
    try:
        for milestone in ms_json:
            max_ms_v += 1
            session.add(Milestone(
                idMilestone=max_ms_v,
                goalMilestone=milestone['goal'],
                requiredVotesMilestone=milestone['requiredVotes'],
                currentVotesMilestone=0,
                untilBlockMilestone=milestone['until'],
                project_id=id
            ))
        session.commit()
    except SQLAlchemyError:
        return jsonify({'status': 'Commit error - Milestone'}), 400
    except KeyError:
        return jsonify({'status': 'Unknown Key'}), 400

    return jsonify({'status': 'ok'}), 201
