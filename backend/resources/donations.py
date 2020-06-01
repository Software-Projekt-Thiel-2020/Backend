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
    id_donation = request.args.get('id')
    minamount_donation = request.args.get('minamount')
    maxamount_donation = request.args.get('maxamount')
    iduser_user = request.args.get('iduser')
    idmilestone_milestone = request.args.get('idmilestone')
    idproject_project = request.args.get('idproject')

    try:
        if id_donation:
            int(id_donation)
        if minamount_donation:
            int(minamount_donation)
        if maxamount_donation:
            int(maxamount_donation)
        if iduser_user:
            int(iduser_user)
        if idmilestone_milestone:
            int(idmilestone_milestone)
        if idproject_project:
            int(idproject_project)
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
