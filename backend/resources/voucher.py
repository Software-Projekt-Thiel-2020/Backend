"""Voucher Resource."""
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
            'price': voucher.price,
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
    id_user = request.args.get('id')

    if not id_user:
        return jsonify({'error': 'missing id'}), 400
    try:
        if id_user:
            int(id_user)
    except ValueError:
        return jsonify({'error': 'bad argument'}), 400

    session = DB_SESSION()
    user = session.query(VoucherUser)
    try:
        if id_user:
            user = user.filter(VoucherUser.id_user == id_user).one()
    except NoResultFound:
        return jsonify({'error': 'User has no vouchers'}), 404

    voucher = session.query(Voucher, VoucherUser)
    voucher = voucher.join(VoucherUser,
                           Voucher.idVoucher == VoucherUser.id_voucher)
    voucher = voucher.filter(VoucherUser.id_user == id_user).all()

    json_data = []
    for vouch, vuser in voucher:
        json_data.append({
            "idVoucher": vouch.idVoucher,
            "idInstitution": vouch.institution_id,
            "titel": vouch.titleVoucher,
            "description": vouch.descriptionVoucher,
            "used": vuser.usedVoucher,
            "expires": vuser.expires_unixtime
        })

    return jsonify(json_data), 200
