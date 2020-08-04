"""Project Resource."""
from flask import Blueprint, request, jsonify

from backend.database.model import Donation, User
from backend.database.model import Milestone
from backend.database.model import Project
from backend.resources.helpers import check_params_int, auth_user, db_session_dec
from backend.smart_contracts.web3 import WEB3
from backend.smart_contracts.web3_project import project_donate, project_donate_check, \
    project_donate_vote, project_donate_vote_check

BP = Blueprint('donations', __name__, url_prefix='/api/donations')


@BP.route('', methods=['GET'])
@db_session_dec
def donations_get(session):
    """
    Handles GET for resource <base>/api/donations .

    :return: json data of projects
    """
    id_donation = request.args.get('id')
    minamount_donation = request.args.get('minamount')
    maxamount_donation = request.args.get('maxamount')
    iduser_user = request.args.get('iduser')
    idmilestone_milestone = request.args.get('idmilestone')
    idproject_project = request.args.get('idproject')

    try:
        check_params_int([id_donation, minamount_donation, maxamount_donation, iduser_user, idmilestone_milestone,
                          idproject_project])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    results = session.query(Donation, Project)
    results = results.join(Milestone, Donation.milestone).join(Project)
    if id_donation:
        results = results.filter(Donation.idDonation == id_donation)
    if minamount_donation:
        results = results.filter(Donation.amountDonation >= minamount_donation)
    if maxamount_donation:
        results = results.filter(Donation.amountDonation <= maxamount_donation)
    if iduser_user:
        results = results.filter(Donation.user_id == iduser_user)
    if idmilestone_milestone:
        results = results.filter(Donation.milestone_id == idmilestone_milestone)
    if idproject_project:
        results = results.filter(Milestone.project_id == idproject_project)

    json_data = []
    for donation, project in results:
        json_data.append({
            'id': donation.idDonation,
            'amount': donation.amountDonation,
            'userid': donation.user_id,
            'milestoneid': donation.milestone_id,
            'projectid': project.idProject,
            'projectname': project.nameProject,
            'projectpic': project.picPathProject,
            'voted': donation.voted,
            'timeofdonation': donation.timeOfDonation,
            'voteEnabled': donation.voteDonation,
        })

    return jsonify(json_data)


@BP.route('', methods=['POST'])
@auth_user
@db_session_dec
def donations_post(session, user_inst):
    """
    Handles POST for resource <base>/api/donations .
    :return: "{'status': 'Spende wurde verbucht'}", 201
    """
    idproject = request.headers.get('idproject', default=None)
    amount = request.headers.get('amount', default=None)
    vote_enabled = request.headers.get('voteEnabled', default=None)

    if None in [idproject, amount, vote_enabled]:
        return jsonify({'error': 'Missing parameter'}), 400
    try:
        check_params_int([idproject, amount, vote_enabled])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    results: Project = session.query(Project).get(idproject)

    if results is None:
        return jsonify({'error': 'Project not found'}), 400

    if int(amount) <= 0:
        return jsonify({'error': 'amount cant be 0 or less'}), 400

    balance = WEB3.eth.getBalance(user_inst.publickeyUser)
    if balance < int(amount):  # ToDo: gas-cost?
        return jsonify({'error': 'not enough balance'}), 406

    try:
        # Add Donation
        donate_check = project_donate_check(results, user_inst, int(amount), bool(int(vote_enabled)))
        if donate_check:
            return jsonify({'error': 'sc error: ' + donate_check}), 400

        milestone_sc_index = project_donate(results, user_inst, int(amount), bool(int(vote_enabled)))

        # if this line fails, we have inconsitent data in the database!
        milestone = session.query(Milestone).filter(Milestone.project_id == int(idproject)).\
            filter(Milestone.milestone_sc_id == milestone_sc_index).one()

        donations_inst = Donation(
            amountDonation=int(amount),
            user=user_inst,
            milestone=milestone,
            voteDonation=bool(int(vote_enabled)),
        )

        session.add(donations_inst)
        session.commit()

        return jsonify({'status': 'Spende wurde verbucht'}), 201
    finally:
        session.rollback()
        session.close()


@BP.route('/vote', methods=['POST'])
@auth_user
@db_session_dec
def milestones_vote(session, user_inst: User):
    """
    Vote for milestone.

    :return: "{'status': 'ok'}", 200
    """
    donation_id = request.headers.get('id')
    vote = request.headers.get('vote')  # 1 = positive, 0 = negative

    if None in [donation_id, vote]:
        return jsonify({'error': 'Missing parameter'}), 400

    try:
        donation_id, vote = check_params_int([donation_id, vote])  # noqa
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    donation: Donation = session.query(Donation).filter(Donation.idDonation == donation_id).one_or_none()

    if donation is None:
        return jsonify({"error": "donation not found"}), 404

    if not donation.voteDonation:
        return jsonify({"error": "didn't register to vote"}), 400

    if donation.user_id != user_inst.idUser:
        return jsonify({"error": "unauthorized user"}), 401

    if donation.voted is not None:
        return jsonify({"error": "already voted"}), 400

    vote_check = project_donate_vote_check(session, user_inst, 0 if vote else 1, donation)
    if vote_check:
        return jsonify({'error': 'sc error: ' + vote_check}), 400

    donation.milestone.currentVotesMilestone += 1 if vote else (-1)

    tx_receipt = project_donate_vote(user_inst, 0 if vote else 1, donation)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")

    voted = 1 if vote else (-1)

    donations_milestone = session.query(Donation).join(Donation.milestone)\
        .filter(Donation.user == user_inst).\
        filter(Milestone.milestone_sc_id == donation.milestone.milestone_sc_id)  # noqa

    for don in donations_milestone:
        don.voted = voted
        session.add(don)

    session.commit()
    return jsonify({'status': 'ok'}), 200
