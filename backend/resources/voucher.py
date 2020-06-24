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


@BP.route('/user', methods=['POST'])
@auth_user
def voucher_post(user):
    """
    Handles DELETE for resource <base>/api/voucher .

    :return: json data of projects
    """
    idVoucher = request.headers.get('idVoucher')

    session = DB_SESSION()
    voucher = session.query(Voucher).filter(Voucher.idVoucher == idVoucher).one_or_none()

    if voucher is None:
        return jsonify({'error': 'Voucher doesnt exist'})

    balance = -1
    try:
        balance = WEB3.eth.getBalance(user.publickeyUser)
    except InvalidAddress:
        return jsonify({'error': 'given publickey is not valid'}), 400

    if balance < voucher.priceVoucher:
        return jsonify({'error': 'not enough balance'})

    association = VoucherUser(usedVoucher=False,
                              expires_unixtime=datetime(2020, 12, 31))
    association.voucher = voucher
    user.append(association)
    
    # TODO - do blockchain transaction

    session.add(voucher)
    session.add(association)
    session.add(user)
    session.commit()

    return jsonify({'status': 'voucher bought'})
