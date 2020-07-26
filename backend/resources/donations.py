"""Project Resource."""
from flask import Blueprint, request, jsonify

from backend.database.db import DB_SESSION
from backend.database.model import Donation, User
from backend.database.model import Milestone
from backend.database.model import Project
from backend.resources.helpers import check_params_int, auth_user, db_session_dec
from backend.smart_contracts.web3 import WEB3, PROJECT_JSON

BP = Blueprint('donations', __name__, url_prefix='/api/donations')


@BP.route('', methods=['GET'])
def donations_get():
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

    session = DB_SESSION()
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
        })

    return jsonify(json_data)


@BP.route('', methods=['POST'])
@auth_user
def donations_post(user_inst):
    """
    Handles POST for resource <base>/api/donations .
    :return: "{'status': 'Spende wurde verbucht'}", 201
    """
    idmilestone = request.headers.get('idmilestone', default=None)
    amount = request.headers.get('amount', default=None)
    vote_enabled = request.headers.get('voteEnabled', default=None)

    if None in [idmilestone, amount, vote_enabled]:
        return jsonify({'error': 'Missing parameter'}), 400
    try:
        check_params_int([idmilestone, amount, vote_enabled])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    session = DB_SESSION()

    results: Milestone = session.query(Milestone).get(idmilestone)

    if results is None:
        return jsonify({'error': 'Milestone not found'}), 400

    if int(amount) <= 0:
        return jsonify({'error': 'amount cant be 0 or less'}), 400

    donations_sc = WEB3.eth.contract(address=results.project.scAddress, abi=PROJECT_JSON["abi"])
    try:
        # Add Donation
        tx_hash = donations_sc.functions.register().buildTransaction({
            'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser),
            'from': user_inst.publickeyUser
        })
        signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=user_inst.privatekeyUser)
        tx_hash2 = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash2)
        if tx_receipt.status != 1:
            raise RuntimeError("SC Call failed!")
        tx_hash = donations_sc.functions.donate(bool(int(vote_enabled))) \
            .buildTransaction(
            {'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser),
             'from': user_inst.publickeyUser, 'value': int(amount)})
        signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=user_inst.privatekeyUser)
        tx_hash2 = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash2)
        if tx_receipt.status != 1:
            raise RuntimeError("SC Call failed!")
        donations_inst = Donation(
            amountDonation=amount,
            user=user_inst,
            milestone_id=idmilestone,
            voteDonation=bool(int(vote_enabled))
        )

        session.add(donations_inst)
        session.commit()

        return jsonify({'status': 'Spende wurde verbucht'}), 201
    finally:
        session.rollback()
        session.close()


def vote_transaction(user_inst: User, vote, donation: Donation):
    """Method to make the voting Transaction."""
    contract_address = WEB3.toChecksumAddress(donation.milestone.project.institution.scAddress)

    donation_sc = WEB3.eth.contract(
        address=contract_address,
        abi=PROJECT_JSON["abi"]
    )

    transaction = donation_sc.functions.vote(donation.milestone.idMilestone, vote)\
        .buildTransaction({'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser)})
    signed_transaction = WEB3.eth.account.sign_transaction(transaction, user_inst.privatekeyUser)

    WEB3.eth.sendRawTransaction(signed_transaction.rawTransaction)


@BP.route('/vote', methods=['PATCH'])
@auth_user
@db_session_dec
def milestones_vote(session, user_inst):
    """
    Vote for milestone.

    :return: "{'status': 'ok'}", 200
    """
    donation_id = request.headers.get('id')
    vote = request.headers.get('vote')  # 1 = positive, 0 = negative

    if None in [donation_id, vote]:
        return jsonify({'error': 'Missing parameter'}), 400

    try:
        donation_id, vote = check_params_int([donation_id, vote])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    donation = session.query(Donation).filter(Donation.idDonation == donation_id).one_or_none()

    if donation is None:
        return jsonify({"error": "milestone not found"}), 404

    donation.milestone.currentVotesMilestone += 1 if vote > 0 else (-1)
    vote_transaction(user_inst, vote, donation)
    session.commit()
    return jsonify({'status': 'ok'}), 201
