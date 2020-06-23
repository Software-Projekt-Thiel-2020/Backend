"""Voucher Resource."""
from flask import Blueprint, jsonify, request
from sqlalchemy.orm.exc import NoResultFound
from backend.database.db import DB_SESSION
from backend.database.model import Voucher, User, BASE


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
    user = session.query(User)
    try:
        if id_user:
            user = user.filter(User.idUser == id_user).one()
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404

    voucher = session.query(Voucher)
    voucher = voucher.join(BASE.metadata.tables['VoucherUser'],
                           Voucher.idVoucher == BASE.metadata.tables['VoucherUser'].c.idVoucher)
    voucher = voucher.filter(BASE.metadata.tables['VoucherUser'].c.idUser == id_user).all()

    json_data = []
    for result in voucher:
        json_data.append({
            "idVoucher": result.idVoucher,
            "idInstitution": result.institution_id,
            "titel": result.titleVoucher,
            "description": result.descriptionVoucher,
            "used": result.usedVoucher,
            "untilBlocK": result.untilBlockVoucher
        })

    return jsonify(json_data), 200
