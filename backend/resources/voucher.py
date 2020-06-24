"""Voucher Resource."""
from flask import Blueprint, jsonify, request
from backend.database.db import DB_SESSION
from backend.database.model import Voucher,VoucherUser
from backend.resources.helpers import auth_user

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


@BP.route('', methods=['DELETE'])
def voucher_delete():
    """
    Handles DELETE for resource <base>/api/voucher .

    :return: json data of projects
    """
    return jsonify({'status': 'TODO: create route'})


@BP.route('', methods=['POST'])
def voucher_post():
    """
    Handles DELETE for resource <base>/api/voucher .

    :return: json data of projects
    """
    return jsonify({'status': 'TODO: create route'})


@BP.route('/user', methods=['DELETE'])
@auth_user
def voucher_delete_user(user_inst):
    """
    Handles DELETE for resource <base>/api/voucher/user .

    :return: json data of projects
    """
    id_voucher = request.args.get('id')

    if not id_voucher:
        return jsonify({'error': 'missing id'}), 400
    try:
        if id_voucher:
            int(id_voucher)
    except ValueError:
        return jsonify({'error': 'bad argument'}), 400

    session = DB_SESSION()
    voucher = session.query(VoucherUser)
    try:
        voucher = voucher.filter(VoucherUser.id_voucher == id_voucher).filter(VoucherUser.id_user == user_inst.idUser).first()
    except NoResultFound:
        return jsonify({'error': 'User has no vouchers'}), 404
   
    voucher.usedVoucher = True
    session.commit()

    return jsonify({'status': 'Gutschein wurde eingelöst'+str(voucher.id_user)}), 201
