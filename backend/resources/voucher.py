"""Voucher Resource."""
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request
from sqlalchemy.orm.exc import NoResultFound
from web3.exceptions import InvalidAddress

from backend.database.model import Voucher, VoucherUser, Institution
from backend.resources.helpers import auth_user, check_params_int, db_session_dec
from backend.smart_contracts.web3 import WEB3
from backend.smart_contracts.web3_voucher import add_voucher, redeem_voucher

BP = Blueprint('voucher', __name__, url_prefix='/api/vouchers')


@BP.route('/institution', methods=['PATCH'])
@db_session_dec
def voucher_patch_institution(session):
    """
    Handles PATCH for resource <base>/api/vouchers/institutions.

    :return: "{'status': 'ok'}", 200
    """
    inst_id = request.headers.get('idInstitution', default=None)
    voucher_id = request.headers.get('idVoucher', default=None)
    voucher_price = request.headers.get('priceVoucher', default=None)
    voucher_available = request.headers.get('availableVoucher', default=None)
    voucher_valid_time = request.headers.get('validTimeVoucher', default=None)

    if None in [inst_id, voucher_id]:
        return jsonify({'error': 'Missing parameter'}), 400

    try:
        check_params_int([voucher_id, inst_id, voucher_valid_time])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    voucher = session.query(Voucher).filter(Voucher.idVoucher == voucher_id).one_or_none()

    if voucher is None:
        return jsonify({'error': 'voucher does not exist'}), 400

    if int(voucher.institution_id) != int(inst_id):
        return jsonify({"error": "voucher does not belong to institution"}), 400

    if voucher_valid_time:
        if int(voucher_valid_time) < int(voucher.validTime):
            return jsonify({'error': 'new validTime has to be bigger than the old one'}), 400
        voucher.validTime = voucher_valid_time
    if voucher_price:
        voucher.priceVoucher = voucher_price
    if voucher_available:
        voucher.available = voucher_available

    session.commit()
    return jsonify({'status': 'Voucher wurde bearbeitet'}), 201


@BP.route('/institution', methods=['POST'])
@auth_user
@db_session_dec
def voucher_post_institution(session, user_inst):  # pylint:disable=unused-argument
    """
    Handles POST for resource <base>/api/voucher/institution .
    :return: json data result (success or failure)
    """
    institution_id = request.headers.get('idInstitution', default=None)
    voucher_price = request.headers.get('price', default=None)
    voucher_description = request.headers.get('subject', default=None)
    voucher_title = request.headers.get('title', default=None)
    voucher_valid_time = request.headers.get('validTime', default=2 * 31536000)

    if None in [voucher_title, voucher_description, voucher_price, institution_id]:
        return jsonify({'error': 'Missing parameter'}), 400

    if "" in [voucher_title, voucher_description]:
        return jsonify({'error': "Empty parameter"}), 400

    try:
        check_params_int([voucher_price, voucher_valid_time, institution_id])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    # ToDo: check institution_owner = user_inst

    res = session.query(Institution).filter(Institution.idInstitution == institution_id).one_or_none()
    if res is None:
        return jsonify({'status': 'Institution does not exist'}), 400

    voucher_inst = Voucher(titleVoucher=voucher_title,
                           descriptionVoucher=voucher_description,
                           priceVoucher=voucher_price,
                           validTime=voucher_valid_time,
                           institution_id=institution_id,
                           )

    # ToDo Blockchain

    session.add(voucher_inst)
    session.commit()
    return jsonify({'status': 'Voucher registered'}), 200


@BP.route('/institution', methods=['GET'])
@db_session_dec
def voucher_get(session):
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

    results = session.query(Voucher)

    if id_voucher is not None:
        results = results.filter(Voucher.idVoucher == id_voucher)
    if id_institution is not None:
        results = results.filter(Voucher.institution_id == id_institution)
    if available is not None:
        results = results.filter(Voucher.available.is_(bool(int(available))))

    json_data = []
    for voucher in results:
        json_data.append({
            'id': voucher.idVoucher,
            'amount': len(voucher.users),
            'institutionid': voucher.institution_id,
            'institutionName': voucher.institution.nameInstitution,
            'subject': voucher.descriptionVoucher,
            'title': voucher.titleVoucher,
            'validTime': voucher.validTime,
            'available': voucher.available,
            'price': voucher.priceVoucher,
            "picturePath": voucher.institution.picPathInstitution,
        })

    return jsonify(json_data), 200


@BP.route('/user', methods=['POST'])
@auth_user
@db_session_dec
def voucher_post(session, user):
    """
    Handles POST for resource <base>/api/voucher/user .
    :return: json data of projects
    """
    id_voucher = request.headers.get('idVoucher')
    if not id_voucher:
        return jsonify({'error': 'missing id'}), 400
    try:
        check_params_int([id_voucher])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    try:
        voucher = session.query(Voucher).filter(Voucher.idVoucher == id_voucher).one()
        balance = WEB3.eth.getBalance(user.publickeyUser)

        if balance < voucher.priceVoucher:  # ToDo: gas-cost?
            return jsonify({'error': 'not enough balance'}), 406
        if not voucher.available:
            return jsonify({'error': 'voucher not available'}), 406

        association = VoucherUser(usedVoucher=False,
                                  expires_unixtime=(datetime.now() + timedelta(0, 2 * 31536000)),
                                  voucher=voucher,
                                  user=user)

        inst: Institution = session.query(Institution).filter(Institution.idInstitution == voucher.institution_id).one()

        transaction = {
            'nonce': WEB3.eth.getTransactionCount(user.publickeyUser),
            'to': inst.publickeyInstitution,
            'value': voucher.priceVoucher,
            'gas': 200000,
            'gasPrice': WEB3.toWei('50', 'gwei')
        }
        signed_transaction = WEB3.eth.account.sign_transaction(transaction, user.privatekeyUser)
        WEB3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        association.index = add_voucher(
            user, inst, voucher.titleVoucher, abs(association.expires_unixtime - datetime.now()).days)

        session.add(voucher)
        session.add(association)
        session.commit()
    except InvalidAddress:
        return jsonify({'error': 'given publickey is not valid'}), 400
    except NoResultFound:
        return jsonify({'error': 'Voucher doesnt exist'}), 404

    return jsonify({'status': 'voucher bought'}), 200


@BP.route('/user', methods=['DELETE'])
@auth_user
@db_session_dec
def voucher_delete_user(session, user_inst):
    """
    Handles DELETE for resource <base>/api/voucher/user .
    :return: json data of projects
    """
    id_voucheruser = request.headers.get('id')

    if not id_voucheruser:
        return jsonify({'error': 'missing id'}), 400
    try:
        check_params_int([id_voucheruser])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    voucher_user = session.query(VoucherUser)
    try:
        voucher_user = voucher_user.filter(VoucherUser.idVoucherUser == id_voucheruser).filter(
            VoucherUser.id_user == user_inst.idUser).one()
        institution = session.query(Institution).filter(
            Institution.idInstitution == voucher_user.voucher.institution_id).one()
        redeem_voucher(user_inst, voucher_user.redeem_id, institution.scAddress)
    except NoResultFound:
        return jsonify({'error': 'No voucher found'}), 404

    voucher_user.usedVoucher = True
    session.commit()

    return jsonify({'status': 'Gutschein wurde eingelöst'}), 201


@BP.route('/user', methods=['GET'])
@db_session_dec
def voucher_get_user(session):
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
