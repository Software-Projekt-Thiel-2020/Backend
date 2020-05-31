"""Project Resource."""
from flask import Blueprint, request, jsonify
from backend.database.db import DB_SESSION
from backend.database.model import Donation
from backend.database.model import Milestone


BP = Blueprint('donations', __name__, url_prefix='/api/donations')


@BP.route('', methods=['GET'])
def donations_get():
    """
    Handles GET for resource <base>/api/donations .

    :return: json data of projects
    """
    args = request.args
    id_donation = args.get('id')
    minamount_donation = args.get('minamount')
    maxamount_donation = args.get('maxamount')
    iduser_user = args.get('iduser')
    idmilestone_milestone = args.get('idmilestone')
    idproject_project = args.get('idproject')

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
        subresults = session.query(Milestone.idMilestone)
        subresults = subresults.filter(Milestone.project_id == idproject_project)
        results = results.filter(Donation.milestone_id.in_(subresults))
    json_data = []
    json_names = ['id', 'amount', 'userid', 'milestoneid']
    for result in results:
        json_data.append(dict(zip(json_names, [
            result.idDonation,
            result.amountDonation,
            result.user_id,
            result.milestone_id,
        ])))

    return jsonify(json_data)
