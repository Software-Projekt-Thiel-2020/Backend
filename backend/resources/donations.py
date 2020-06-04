"""Project Resource."""
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from backend.database.db import DB_SESSION
from backend.database.model import Donation
from backend.database.model import Milestone
from backend.resources.helpers import check_params_int, auth_user

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
    results = session.query(Donation)

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
        results = results.join(Donation.milestone).filter(Milestone.project_id == idproject_project)

    json_data = []
    for result in results:
        json_data.append({
            'id': result.idDonation,
            'amount': result.amountDonation,
            'userid': result.user_id,
            'milestoneid': result.milestone_id,
        })

    return jsonify(json_data)


@BP.route('', methods=['POST'])
@auth_user
def donations_post(user_inst):
    """
    Handles POST for resource <base>/api/donations .
    :return: "{'status': 'Spende wurde verbucht'}", 201
    """
    idmilestone = request.args.get('idmilestone', default=None)
    amount = request.args.get('amount', default=None)
    ether_account_key = request.args.get('etherAccountKey', default=None)  # ToDo: an web3.py ?

    if None in [idmilestone, amount, ether_account_key]:
        return jsonify({'error': 'Missing parameter'}), 403

    session = DB_SESSION()

    if session.query(Milestone).get(idmilestone) is None:
        return jsonify({'error': 'Milestone not found'}), 400

    try:
        donations_inst = Donation(
            amountDonation=amount,
            user=user_inst,
            milestone_id=idmilestone
        )

        session.add(donations_inst)
        session.commit()
    except SQLAlchemyError:
        return jsonify({'status': 'Database error'}), 400

    return jsonify({'status': 'Spende wurde verbucht'}), 201
