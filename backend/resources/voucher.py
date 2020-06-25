"""Voucher Resource."""
from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy.orm.exc import NoResultFound

from backend.database.db import DB_SESSION
from backend.database.model import Voucher, VoucherUser
from backend.resources.helpers import auth_user, check_params_int

BP = Blueprint('voucher', __name__, url_prefix='/api/vouchers')


@BP.route('/institution', methods=['GET'])
def voucher_get():
    """
    Handles GET for resource <base>/api/voucher/institution .

    :return: json data of projects
    """
    id_voucher = request.args.get('id')
    id_institution = request.args.get('idInstitution')
    available = request.args.get('available')

    try:
        check_params_int([id_voucher, id_institution, available])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    session = DB_SESSION()
    results = session.query(Voucher)

    if id_voucher is not None:
        results = results.filter(Voucher.idVoucher == id_voucher)
    if id_institution is not None:
        results = results.filter(Voucher.institution_id == id_institution)
    if available is not None:
        results = results.filter(Voucher.available.is_(available))

    json_data = []
    for voucher in results:
        json_data.append({
            'id': voucher.idVoucher,
            'amount': len(voucher.users),
            'institutionid': voucher.institution_id,
            'subject': voucher.descriptionVoucher,
            'title': voucher.titleVoucher,
            'validTime': voucher.validTime,
            'available': voucher.available,
            'price': voucher.priceVoucher,
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
        voucher = voucher.filter(VoucherUser.id_voucher == id_voucher).filter(
            VoucherUser.id_user == user_inst.idUser).first()
    except NoResultFound:
        return jsonify({'error': 'No voucher found'}), 404

    voucher.usedVoucher = True
    session.commit()

    return jsonify({'status': 'Gutschein wurde eingelöst'}), 201


@BP.route('/user', methods=['GET'])
def voucher_get_user():
    """
    Handles GET for resource <base>/api/voucher/user .
    :return: json data of projects
    """
    id_voucheruser = request.args.get('id')
    id_voucher = request.args.get('idVoucher')
    id_user = request.args.get('idUser')
    id_institution = request.args.get('idInstitution')
    used = request.args.get('used')
    expired = request.args.get('expired')

    try:
        check_params_int([id_voucher, id_user, id_institution, used, expired])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    session = DB_SESSION()

    results = session.query(Voucher, VoucherUser).join(Voucher, VoucherUser.id_voucher == Voucher.idVoucher)

    if id_voucheruser is not None:
        results = results.filter(VoucherUser.idVoucherUser == id_voucheruser)
    if id_voucher is not None:
        results = results.filter(Voucher.idVoucher == id_voucher)
    if id_user is not None:
        results = results.filter(VoucherUser.id_user == id_user)
    if id_institution is not None:
        results = results.filter(Voucher.institution_id == id_institution)
    if used is not None:
        results = results.filter(VoucherUser.usedVoucher.is_(used))
    if expired is not None:
        if int(expired) >= 1:
            results = results.filter(VoucherUser.expires_unixtime < datetime.now())
        else:
            results = results.filter(VoucherUser.expires_unixtime >= datetime.now())

    json_data = []
    for vouch, vuser in results:
        json_data.append({
            "id": vuser.idVoucherUser,
            "userid": vuser.id_user,
            "idvoucher": vuser.id_voucher,
            "idinstitution": vouch.institution_id,
            "titel": vouch.titleVoucher,
            "description": vouch.descriptionVoucher,
            "used": vuser.usedVoucher,
            "untilTime": vuser.expires_unixtime.timestamp(),
            "price": vouch.priceVoucher,
        })

    return jsonify(json_data), 200
