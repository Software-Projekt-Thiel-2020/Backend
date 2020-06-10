"""Project Resource."""
import json
from typing import List

import validators
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from backend.database.db import DB_SESSION
from backend.database.model import Milestone, Institution
from backend.database.model import Project
from backend.resources.helpers import auth_user, check_params_int

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
    for result in results:
        json_data.append({
            'id': result.idProject,
            'name': result.nameProject,
            'webpage': result.webpageProject,
            'idsmartcontract': result.smartcontract_id,
            'idinstitution': result.institution_id,
        })

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
    for row in milestoneresults:
        json_ms.append({
            'id': row.idMilestone,
            'idProjekt': row.project_id,
            'goal': row.goalMilestone,
            'requiredVotes': row.requiredVotesMilestone,
            'currentVotes': row.currentVotesMilestone,
            'until': row.untilBlockMilestone,
        })

    json_data = {
        'id': results.idProject,
        'name': results.nameProject,
        'webpage': results.webpageProject,
        'idsmartcontract': results.smartcontract_id,
        'idinstitution': results.institution_id,
        'milestones': json_ms
    }

    return jsonify(json_data), 200


@BP.route('', methods=['POST'])
@auth_user
def projects_post(user_inst):  # pylint:disable=unused-argument
    """
    Handles POST for resource <base>/api/projects .

    :return: "{'status': 'ok'}", 200
    """
    name = request.headers.get('name')
    webpage = request.headers.get('webpage')
    id_institution = request.headers.get('idInstitution')
    goal = request.headers.get('goal')
    required_votes = request.headers.get('requiredVotes')
    until = request.headers.get('until')
    milestones = request.headers.get('milestones', default="[]")

    if None in [name, goal, required_votes, until]:
        return jsonify({'error': 'Missing parameter'}), 403
    try:
        check_params_int([id_institution, goal, required_votes, until])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    session = DB_SESSION()

    if id_institution is not None and session.query(Institution).get(id_institution) is None:
        return jsonify({'error': 'Institution not found'}), 400

    if webpage is not None and not validators.url(webpage):
        return jsonify({'error': 'webpage is not a valid url'}), 400

    try:
        project_inst = Project(
            nameProject=name,
            webpageProject=webpage,
            smartcontract_id=1,
            institution_id=id_institution
            # ToDo: add user as project owner
        )
    except SQLAlchemyError:
        return jsonify({'status': 'Database error'}), 400

    try:
        milestones_inst: List[Milestone] = []
        for milestone in json.loads(milestones):
            milestones_inst.append(Milestone(
                goalMilestone=milestone['goal'],
                requiredVotesMilestone=milestone['requiredVotes'],
                currentVotesMilestone=0,
                untilBlockMilestone=milestone['until'],
            ))
    except SQLAlchemyError:
        return jsonify({'status': 'Database error!'}), 400
    except (KeyError, json.JSONDecodeError):
        return jsonify({'status': 'invalid json'}), 400

    try:
        project_inst.milestones.extend(milestones_inst)
        session.add_all(milestones_inst)
        session.add(project_inst)
        session.commit()
    except SQLAlchemyError:
        return jsonify({'status': 'Commit error!'}), 400

    return jsonify({'status': 'ok', 'id': project_inst.idProject}), 201


@BP.route('/<id>', methods=['PATCH'])
@auth_user
def projects_patch(user_inst, id):  # pylint:disable=invalid-name,redefined-builtin,unused-argument
    """
    Handles PATCH for resource <base>/api/projects/<id> .

    :return: "{'status': 'ok'}", 200
    """
    webpage = request.headers.get('webpage', default=None)
    milestones = request.headers.get('milestones', default="[]")
    # ToDo: is this user allowed to patch this project?

    session = DB_SESSION()
    project_inst: Project = session.query(Project).get(id)

    if project_inst is None:
        return jsonify({'error': 'Project doesnt exist'}), 404
    if webpage is not None and not validators.url(webpage):
        return jsonify({'error': 'webpage is not a valid url'}), 400

    try:
        if webpage is not None:
            project_inst.webpageProject = webpage
    except SQLAlchemyError:
        return jsonify({'status': 'Database error!'}), 400

    try:
        milestones_inst: List[Milestone] = []
        for milestone in json.loads(milestones):
            milestones_inst.append(Milestone(
                goalMilestone=milestone['goal'],
                requiredVotesMilestone=milestone['requiredVotes'],
                currentVotesMilestone=0,
                untilBlockMilestone=milestone['until'],
            ))
    except SQLAlchemyError:
        return jsonify({'status': 'Database error!'}), 400
    except (KeyError, json.JSONDecodeError):
        return jsonify({'status': 'invalid json'}), 400

    try:
        project_inst.milestones.extend(milestones_inst)
        session.add_all(milestones_inst)
        session.commit()
    except SQLAlchemyError:
        return jsonify({'status': 'Commit error!'}), 400
    return jsonify({'status': 'ok'}), 201
