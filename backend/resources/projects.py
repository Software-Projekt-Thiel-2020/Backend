"""Project Resource."""
import binascii
import json
import time
from base64 import b64decode

import validators
from flask import Blueprint, request, jsonify
from geopy import distance
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from backend.database.model import Milestone, Institution, Donation, User
from backend.database.model import Project
from backend.resources.helpers import auth_user, check_params_int, db_session_dec
from backend.smart_contracts.web3 import WEB3
from backend.smart_contracts.web3_project import project_constructor, project_add_milestone, \
    project_constructor_check, project_add_milestone_check


BP = Blueprint('projects', __name__, url_prefix='/api/projects')


@BP.route('', methods=['GET'])
@db_session_dec
def projects_get(session):
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
    username = request.args.get('username')

    try:
        check_params_int([id_project, id_institution])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    if None in [radius, latitude, longitude] and any([radius, latitude, longitude]):
        return jsonify({"error": "bad geo argument"}), 400

    results = session.query(Project).join(Project.institution).join(Institution.user)

    if id_project:
        results = results.filter(Project.idProject == id_project)
    if id_institution:
        results = results.filter(Project.institution_id == id_institution)
    if name_project:
        results = results.filter(Project.nameProject.ilike("%" + name_project + "%"))
    if username:
        results = results.filter(User.usernameUser == username)

    json_data = []
    for result in results:
        if radius and latitude and longitude:
            if result.latitude and result.longitude:
                if distance.distance((latitude, longitude),
                                     (result.latitude, result.longitude)).km > radius:
                    continue
            else:
                if distance.distance((latitude, longitude),
                                     (result.institution.latitude, result.institution.longitude)).km > radius:
                    continue
        json_data.append({
            'id': result.idProject,
            'name': result.nameProject,
            'webpage': result.webpageProject,
            'idinstitution': result.institution_id,
            'picturePath': result.picPathProject,
            'description': result.descriptionProject,
            'short': result.shortDescription,
            'latitude': result.latitude,
            'longitude': result.longitude,
            'until': result.until,
        })

    return jsonify(json_data)


@BP.route('/<id>', methods=['GET'])
@db_session_dec
def projects_id(session, id):  # noqa
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

    results = session.query(Project)

    try:
        if id_project:
            results = results.filter(Project.idProject == id_project).one()
    except NoResultFound:
        return jsonify(), 404

    milestoneresults = session.query(Milestone).filter(Milestone.project_id == id_project)

    json_ms = []
    total = 0
    for row in milestoneresults:
        donation_sum = session.query(func.sum(Donation.amountDonation)). \
            filter(Donation.milestone_id == row.idMilestone).group_by(Donation.milestone_id).scalar()
        donation_sum = donation_sum if donation_sum is not None else 0

        pos_votes = session.query(func.count(Donation.voted)). \
            filter(Donation.milestone_id == row.idMilestone). \
            filter(Donation.voted == 1). \
            group_by(Donation.milestone_id).scalar()
        pos_votes = pos_votes if pos_votes is not None else 0

        neg_votes = session.query(func.count(Donation.voted)). \
            filter(Donation.milestone_id == row.idMilestone). \
            filter(Donation.voted == -1). \
            group_by(Donation.milestone_id).scalar()
        neg_votes = neg_votes if neg_votes is not None else 0

        json_ms.append({
            'id': row.idMilestone,
            'idProjekt': row.project_id,
            'milestoneName': row.nameMilestone,
            'goal': str(row.goalMilestone),
            'until': row.untilBlockMilestone,
            'totalDonated': str(donation_sum),
            'positiveVotes': pos_votes,
            'negativeVotes': neg_votes,
        })
        total += donation_sum
    json_data = {
        'id': results.idProject,
        'name': results.nameProject,
        'webpage': results.webpageProject,
        'idinstitution': results.institution_id,
        'milestones': json_ms,
        'picturePath': results.picPathProject,
        'description': results.descriptionProject,
        'short': results.shortDescription,
        'latitude': results.latitude,
        'longitude': results.longitude,
        'address': results.institution.addressInstitution,
        'until': results.until,
        'goal': str(results.goal),
        'totalDonated': str(total),
    }
    return jsonify(json_data), 200


@BP.route('', methods=['POST'])
@auth_user
@db_session_dec
# pylint:disable=unused-argument, too-many-locals, too-many-branches, too-many-statements
def projects_post(session, user_inst: User):
    """
    Handles POST for resource <base>/api/projects .

    :return: "{'status': 'ok'}", 200
    """
    name = request.headers.get('name')
    webpage = request.headers.get('webpage')
    id_institution = request.headers.get('idInstitution')
    goal_raw = request.headers.get('goal')
    until_raw = request.headers.get('until')
    milestones = request.headers.get('milestones', default="[]")
    description = request.headers.get('description')
    latitude = request.headers.get('latitude')
    longitude = request.headers.get('longitude')
    short = request.headers.get('short')

    if None in [name, goal_raw, until_raw, id_institution, description, short]:
        return jsonify({'error': 'Missing parameter'}), 403
    try:
        id_institution, goal, until = check_params_int([id_institution, goal_raw, until_raw])  # noqa
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    try:
        description = b64decode(description).decode("latin-1")  # noqa
    except (TypeError, binascii.Error):
        return jsonify({"error": "bad base64 encoding"}), 400

    if id_institution and session.query(Institution).get(id_institution) is None:
        return jsonify({'error': 'Institution not found'}), 400

    if webpage and not validators.url(webpage):
        return jsonify({'error': 'webpage is not a valid url'}), 400

    if until < int(time.time()):
        return jsonify({'error': 'until value is in the past'}), 400

    if until > 2 ** 64:
        return "until value is not a valid date... or is it after the 04.12.219250468 15:30:07 already?!"

    try:
        short = b64decode(str(short)).decode("latin-1")
    except (TypeError, binascii.Error):
        return jsonify({"error": "bad base64 encoding"}), 400

    result = session.query(Institution) \
        .filter(Institution.idInstitution == id_institution).filter(Institution.user == user_inst).one_or_none()
    if result is None:
        return jsonify({'error': 'User has no permission to create projects for this institution'}), 403

    project_inst = Project(
        nameProject=name,
        webpageProject=webpage,
        institution_id=id_institution,
        descriptionProject=description,
        latitude=latitude,
        longitude=longitude,
        until=until,
        goal=goal,
        shortDescription=short
    )

    try:
        price_sum = 0
        milestones_json = json.loads(milestones)
        if len(milestones_json) == 0:
            return jsonify({'error': 'Missing milestone'}), 403

        ctor_check, price = project_constructor_check(user_inst, str(str(description)[0:32]), goal)
        if ctor_check:
            return jsonify({'error': 'sc error: ' + ctor_check}), 400
        price_sum += price

        owner_balance = WEB3.eth.getBalance(user_inst.publickeyUser)
        if price_sum > owner_balance:
            return jsonify({'error': 'milestone error: not enough balance to create project'}), 400

        for milestone in milestones_json:
            mile_check, price = project_add_milestone_check(session, project_inst, user_inst, milestone['name'],
                                                            int(milestone['goal']), int(milestone['until']))
            if mile_check:
                return jsonify({'error': 'milestone error: ' + mile_check}), 400
            price_sum += price

        if price_sum > owner_balance:
            return jsonify({'error': 'milestone error: not enough balance to create all milestones'}), 400

        project_inst.scAddress = project_constructor(user_inst, str(str(description)[0:32]), goal)
        session.add(project_inst)

        for milestone in sorted(milestones_json, key=lambda x: x['goal']):
            sc_id = project_add_milestone(project_inst, user_inst, milestone['name'],
                                          int(milestone['goal']), int(milestone['until']))
            milestones_inst = Milestone(
                nameMilestone=milestone['name'],
                goalMilestone=int(milestone['goal']),
                untilBlockMilestone=milestone['until'],
                milestone_sc_id=sc_id,
            )
            project_inst.milestones.append(milestones_inst)
            session.add(project_inst)
            session.add(milestones_inst)
        session.commit()
        return jsonify({'status': 'ok', 'id': project_inst.idProject}), 201
    except (ValueError, KeyError, json.JSONDecodeError):
        return jsonify({'error': 'invalid json'}), 400
    finally:
        session.rollback()


@BP.route('/<id>', methods=['PATCH'])
@auth_user
@db_session_dec
# pylint:disable=invalid-name,redefined-builtin,too-many-locals, too-many-branches
def projects_patch(session, user_inst, id):
    """
    Handles PATCH for resource <base>/api/projects/<id> .

    :return: "{'status': 'ok'}", 200
    """
    webpage = request.headers.get('webpage', default=None)
    milestones = request.headers.get('milestones', default="[]")
    description = request.headers.get('description')
    short = request.headers.get('short')
    latitude = request.headers.get('latitude')
    longitude = request.headers.get('longitude')

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
        try:
            description = b64decode(description).decode("latin-1")
        except (TypeError, binascii.Error):
            return jsonify({"error": "bad base64 encoding"}), 400
        project_inst.descriptionProject = description

    if short is not None:
        try:
            short = b64decode(short).decode("latin-1")
        except (TypeError, binascii.Error):
            return jsonify({"error": "bad base64 encoding"}), 400
        project_inst.shortDescription = short

    result = session.query(Institution) \
        .filter(Institution.idInstitution == project_inst.institution_id) \
        .filter(Institution.user == user_inst).one_or_none()
    if result is None:
        return jsonify({'error': 'User has no permission to create projects for this institution'}), 403

    try:
        price_sum = 0
        milestones_json = json.loads(milestones)
        for milestone in milestones_json:
            mile_check, price = project_add_milestone_check(session, project_inst, user_inst, milestone['name'],
                                                            int(milestone['goal']), int(milestone['until']))
            if mile_check:
                return jsonify({'error': 'milestone error: ' + mile_check}), 400
            price_sum += price
        if price_sum > WEB3.eth.getBalance(user_inst.publickeyUser):
            return jsonify({'error': 'milestone error: not enough balance to create all milestones'}), 400

        for milestone in sorted(milestones_json, key=lambda x: x['goal']):
            sc_id = project_add_milestone(project_inst, user_inst,
                                          milestone['name'], int(milestone['goal']), int(milestone['until']))
            milestones_inst = Milestone(
                nameMilestone=milestone['name'],
                goalMilestone=int(milestone['goal']),
                untilBlockMilestone=milestone['until'],
                milestone_sc_id=sc_id,
            )

            project_inst.milestones.append(milestones_inst)
            session.add(project_inst)
            session.add(milestones_inst)
        session.add(project_inst)
        session.commit()
        return jsonify({'status': 'ok'}), 201
    except (KeyError, json.JSONDecodeError):
        return jsonify({'status': 'invalid json'}), 400
    finally:
        session.rollback()
        session.close()
