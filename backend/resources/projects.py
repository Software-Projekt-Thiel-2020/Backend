"""Project Resource."""
import json
from typing import List

import validators
from flask import Blueprint, request, jsonify
from geopy import distance
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
    radius = request.args.get('radius', type=int)
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    name_project = request.args.get('name')

    try:
        check_params_int([id_project, id_institution])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    if None in [radius, latitude, longitude] and any([radius, latitude, longitude]):
        return jsonify({"error": "bad geo argument"}), 400

    session = DB_SESSION()
    results = session.query(Project)

    if id_project:
        results = results.filter(Project.idProject == id_project)
    if id_institution:
        results = results.filter(Project.institution_id == id_institution)
    if name_project:
        results = results.filter(Project.nameProject.ilike("%" + name_project + "%"))

    json_data = []
    for result in results:

        if radius and latitude and longitude and \
                distance.distance((latitude, longitude), (result.institution.latitude, result.institution.longitude)) \
                        .km > radius:
            continue
        json_data.append({
            'id': result.idProject,
            'name': result.nameProject,
            'webpage': result.webpageProject,
            'idsmartcontract': result.smartcontract_id,
            'idinstitution': result.institution_id,
            'picturePath': result.picPathProject,
            'description': result.descriptionProject
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
        'milestones': json_ms,
        'picturePath': results.picPathProject,
        'description': results.descriptionProject,
        'latitude': results.latitude,
        'longitude': results.longitude
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
    description = request.headers.get('description')
    latitude = request.headers.get('latitude')
    longitude = request.headers.get('longitude')

    if None in [name, goal, required_votes, until]:
        return jsonify({'error': 'Missing parameter'}), 403
    try:
        check_params_int([id_institution, goal, required_votes, until])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    if latitude and longitude is not None:
        try:
            float(latitude)
            float(longitude)
        except ValueError:
            return jsonify({'error': 'not a valid geolocation'}), 400

    session = DB_SESSION()

    if id_institution and session.query(Institution).get(id_institution) is None:
        return jsonify({'error': 'Institution not found'}), 400

    if webpage and not validators.url(webpage):
        return jsonify({'error': 'webpage is not a valid url'}), 400

    project_inst = Project(
        nameProject=name,
        webpageProject=webpage,
        smartcontract_id=1,
        institution_id=id_institution,
        descriptionProject=description,
        latitude=latitude,
        longitude=longitude
        # ToDo: add user as project owner
    )

    try:
        milestones_inst: List[Milestone] = []
        for milestone in json.loads(milestones):
            milestones_inst.append(Milestone(
                goalMilestone=milestone['goal'],
                requiredVotesMilestone=milestone['requiredVotes'],
                currentVotesMilestone=0,
                untilBlockMilestone=milestone['until'],
            ))
    except (KeyError, json.JSONDecodeError):
        return jsonify({'status': 'invalid json'}), 400

    project_inst.milestones.extend(milestones_inst)
    session.add_all(milestones_inst)
    session.add(project_inst)
    session.commit()
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
    description = request.headers.get('description')
    latitude = request.headers.get('latitude')
    longitude = request.headers.get('longitude')
    # ToDo: is this user allowed to patch this project?

    session = DB_SESSION()
    project_inst: Project = session.query(Project).get(id)

    if project_inst is None:
        return jsonify({'error': 'Project doesnt exist'}), 404
    if webpage is not None and not validators.url(webpage):
        return jsonify({'error': 'webpage is not a valid url'}), 400
    if latitude and longitude is not None:
        try:
            float(latitude)
            float(longitude)
            project_inst.latitude = latitude
            project_inst.longitude = longitude
        except ValueError:
            return jsonify({'error': 'not a valid geolocation'}), 400

    if webpage is not None:
        project_inst.webpageProject = webpage
    if description is not None:
        project_inst.descriptionProject = description

    try:
        milestones_inst: List[Milestone] = []
        for milestone in json.loads(milestones):
            milestones_inst.append(Milestone(
                goalMilestone=milestone['goal'],
                requiredVotesMilestone=milestone['requiredVotes'],
                currentVotesMilestone=0,
                untilBlockMilestone=milestone['until'],
            ))
    except (KeyError, json.JSONDecodeError):
        return jsonify({'status': 'invalid json'}), 400

    project_inst.milestones.extend(milestones_inst)
    session.add_all(milestones_inst)
    session.commit()
    return jsonify({'status': 'ok'}), 201
