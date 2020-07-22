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
from backend.smart_contracts.web3 import WEB3, PROJECT_JSON

BP = Blueprint('projects', __name__, url_prefix='/api/projects')


def vote_transaction(milestone_id, vote, user_inst, project_id):
    """Method to make the voting Transaction."""
    session = DB_SESSION()
    project = session.query(Project).filter(Project.idProject == project_id).one()

    institution = session.query(Institution).filter(Institution.idInstitution == project.institution_id).one()

    contract_address = WEB3.toChecksumAddress(institution.scAddress)

    donation_sc = WEB3.eth.contract(
        address=contract_address,
        abi=PROJECT_JSON["abi"]
    )

    transaction = donation_sc.functions.vote(int(milestone_id),
                                             int(vote))\
        .buildTransaction({'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser)})
    signed_transaction = WEB3.eth.account.sign_transaction(transaction, user_inst.privatekeyUser)

    WEB3.eth.sendRawTransaction(signed_transaction.rawTransaction)


@BP.route('/vote', methods=['PATCH'])
@auth_user
def milestones_vote(user_inst):
    """
    Vote for milestone.

    :return: "{'status': 'ok'}", 200
    """
    vote = 0
    project_id = request.headers.get('projectId', default=None)
    milestone_id = request.headers.get('milestoneId', default=None)
    vote_position = request.headers.get('votePosition', default=None)  # n or p

    if None in [project_id, milestone_id, vote_position]:
        return jsonify({'error': 'Missing parameter'}), 400

    try:
        check_params_int([project_id, milestone_id])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    session = DB_SESSION()
    milestones = session.query(Milestone)

    if vote_position == 'n':
        vote = 1

    for milestone in milestones:

        if int(milestone.idMilestone) == int(milestone_id):

            if int(milestone.project_id) == int(project_id):
                if vote_position == 'p':
                    milestone.currentVotesMilestone += 1
                    session.commit()
                    vote_transaction(milestone_id, vote, user_inst, project_id)
                    return jsonify({'status': 'ok'}), 201
                if vote_position == 'n':
                    milestone.currentVotesMilestone -= 1
                    session.commit()
                    vote_transaction(milestone_id, vote, user_inst, project_id)
                    return jsonify({'status': 'ok'}), 201

    return jsonify({"error": "milestone not found"}), 404


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
            'description': result.descriptionProject,
            'latitude': result.latitude,
            'longitude': result.longitude,
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
        'longitude': results.longitude,
    }

    return jsonify(json_data), 200


@BP.route('', methods=['POST'])
@auth_user
def projects_post(user_inst):  # pylint:disable=unused-argument, too-many-locals
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

    if None in [name, goal, required_votes, until, id_institution]:
        return jsonify({'error': 'Missing parameter'}), 403
    try:
        check_params_int([id_institution, goal, required_votes, until])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    session = DB_SESSION()

    if id_institution and session.query(Institution).get(id_institution) is None:
        return jsonify({'error': 'Institution not found'}), 400

    if webpage and not validators.url(webpage):
        return jsonify({'error': 'webpage is not a valid url'}), 400

    # ToDo: sanity check milestones
    # ToDo: check user_inst permission

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
    result: Institution = session.query(Institution).get(id_institution)
    donations_sc = WEB3.eth.contract(address=result.scAddress, abi=PROJECT_JSON["abi"])
    try:
        milestones_inst: List[Milestone] = []
        for milestone in json.loads(milestones):
            tx_hash = donations_sc.functions.addMilestone(WEB3.toBytes(text=milestone['name']),
                                                          int(milestone['goal']),
                                                          int(milestone['until'])). \
                buildTransaction({'nonce': WEB3.eth.getTransactionCount(WEB3.eth.defaultAccount),
                                  'from': WEB3.eth.defaultAccount})
            # signed_tx = WEB3.eth.account.signTransaction(tx_hash, private_key=admin_account.key)
            # tx_hash = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_hash = WEB3.eth.sendTransaction(tx_hash)
            tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
            if tx_receipt.status != 1:
                raise RuntimeError("SC Call failed!")
            milestones_inst.append(Milestone(
                goalMilestone=milestone['goal'],
                requiredVotesMilestone=milestone['requiredVotes'],
                currentVotesMilestone=0,
                untilBlockMilestone=milestone['until'],
            ))

        project_inst.milestones.extend(milestones_inst)
        session.add_all(milestones_inst)
        session.add(project_inst)
        session.commit()
        return jsonify({'status': 'ok', 'id': project_inst.idProject}), 201
    except (KeyError, json.JSONDecodeError):
        return jsonify({'status': 'invalid json'}), 400
    finally:
        session.rollback()


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

    result: Institution = session.query(Institution).get(id)
    donations_sc = WEB3.eth.contract(address=result.scAddress, abi=PROJECT_JSON["abi"])
    try:
        milestones_inst: List[Milestone] = []
        for milestone in json.loads(milestones):
            tx_hash = donations_sc.functions.addMilestone(WEB3.toBytes(text=milestone['name']),
                                                          int(milestone['goal']), int(milestone['until'])). \
                buildTransaction({'nonce': WEB3.eth.getTransactionCount(WEB3.eth.defaultAccount),
                                  'from': WEB3.eth.defaultAccount})
            # signed_tx = WEB3.eth.account.signTransaction(tx_hash, private_key=admin_account.key)
            # tx_hash = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_hash = WEB3.eth.sendTransaction(tx_hash)
            tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
            if tx_receipt.status != 1:
                raise RuntimeError("SC Call failed!")
            milestones_inst.append(Milestone(
                goalMilestone=milestone['goal'],
                requiredVotesMilestone=milestone['requiredVotes'],
                currentVotesMilestone=0,
                untilBlockMilestone=milestone['until'],
            ))

        project_inst.milestones.extend(milestones_inst)
        session.add_all(milestones_inst)
        session.commit()
        return jsonify({'status': 'ok'}), 201
    except (KeyError, json.JSONDecodeError):
        return jsonify({'status': 'invalid json'}), 400
    finally:
        session.rollback()
        session.close()