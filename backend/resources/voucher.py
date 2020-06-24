"""Voucher Resource."""
from flask import Blueprint, jsonify, request
from backend.database.db import DB_SESSION
from backend.database.model import Voucher

BP = Blueprint('voucher', __name__, url_prefix='/api/voucher')


@BP.route('/institution', methods=['GET'])
def voucher_get():
    """
    Handles GET for resource <base>/api/voucher/institution .

    :return: json data of projects
    """
    id_inst = request.args.get('id', type=int)

    session = DB_SESSION()
    results = session.query(Voucher).filter(Voucher.institution_id == id_inst)

    json_data = []
    for voucher in results:
        json_data.append({
            'id': voucher.idVoucher,
            'title': voucher.titleVoucher,
            'description': voucher.descriptionVoucher,
            'untilBlock': voucher.untilBlockVoucher
        })

    return jsonify(json_data), 200


@BP.route('', methods=['POST'])
def voucher_post():
    """
    Handles DELETE for resource <base>/api/voucher .

    :return: json data of projects
    """
    return jsonify({'status': 'TODO: create route'})
