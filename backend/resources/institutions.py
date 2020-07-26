"""Institution Resource."""
from datetime import datetime

import validators
from flask import Blueprint, request, jsonify
from geopy import distance

from backend.database.db import DB_SESSION
from backend.database.model import Institution, Transaction, User
from backend.resources.helpers import auth_user, check_params_int, check_params_float
from backend.smart_contracts.web3 import WEB3, PROJECT_JSON
from backend.smart_contracts.contract_calls.web3_voucher import voucher_constructor

BP = Blueprint('institutions', __name__, url_prefix='/api/institutions')  # set blueprint name and resource path


@BP.route('', methods=['GET'])
def institutions_get():
    """
    Handles GET for resource <base>/api/institutions .

    :return: json data of institutions
    """
    id_institution = request.args.get('id')
    radius = request.args.get('radius')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    name_institution = request.args.get('name')
    has_vouchers = request.args.get('has_vouchers')
    username = request.args.get('username')

    try:
        check_params_int([id_institution, radius, has_vouchers])
        # pylint: disable=unbalanced-tuple-unpacking
        radius, latitude, longitude = check_params_float([radius, latitude, longitude])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400
    if None in [radius, latitude, longitude] and any([radius, latitude, longitude]):
        return jsonify({"error": "bad geo argument"}), 400

    session = DB_SESSION()
    results = session.query(Institution).join(User)

    json_data = []

    if username:
        results = results.filter(User.usernameUser == username)
    if id_institution:
        results = results.filter(Institution.idInstitution == id_institution)
    if name_institution:
        results = results.filter(Institution.nameInstitution.ilike("%" + name_institution + "%"))
    if has_vouchers is not None:
        if int(has_vouchers) == 1:
            results = results.filter(Institution.vouchers.any())
        else:
            results = results.filter(~Institution.vouchers.any())

    for result in results:
        result: Institution = result
        if radius and latitude and longitude and \
                distance.distance((latitude, longitude), (result.latitude, result.longitude)).km > radius:
            continue
        json_data.append({
            "id": result.idInstitution,
            "name": result.nameInstitution,
            "webpage": result.webpageInstitution,
            "address": result.addressInstitution,
            "picturePath": result.picPathInstitution,
            "longitude": result.longitude,
            "latitude": result.latitude,
            "publickey": result.publickeyInstitution,
            "description": result.descriptionInstitution,
            "username": result.user.usernameUser,
        })

    return jsonify(json_data)


@BP.route('', methods=['POST'])
@auth_user
def institutions_post(user_inst):  # pylint:disable=unused-argument
    """
    Handles POST for resource <base>/api/institutions .
    :return: json response
    """
    name = request.headers.get('name')
    webpage = request.headers.get('webpage')
    address = request.headers.get('address')
    username = request.headers.get('username')
    publickey = request.headers.get('publickey')
    description = request.headers.get('description')
    latitude = request.headers.get('latitude')
    longitude = request.headers.get('longitude')

    if not user_inst.group == "support":
        return jsonify({'error': 'Forbidden'}), 403
    if None in [name, address, latitude, longitude, publickey]:
        return jsonify({'error': 'Missing parameter'}), 400

    try:
        # pylint: disable=unbalanced-tuple-unpacking
        latitude, longitude = check_params_float([latitude, longitude])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    if webpage is not None and not validators.url(webpage):
        return jsonify({'error': 'webpage is not a valid url'}), 400

    session = DB_SESSION()
    owner_inst: User = session.query(User).filter(User.usernameUser == username).one_or_none()
    if owner_inst is None:
        return jsonify({'error': 'username not found'}), 400

    # check if name is already taken
    if session.query(Institution).filter(Institution.nameInstitution == name).first():
        return jsonify({'error': 'name already exists'}), 400

    try:
        # web3 default account is used for this:
        donations_contract = WEB3.eth.contract(abi=PROJECT_JSON["abi"], bytecode=PROJECT_JSON["bytecode"])
        ctor = donations_contract.constructor(publickey, WEB3.eth.defaultAccount, 80,
                                              WEB3.toBytes(text="donations sc"), 100000, 20)
        transaction = ctor.transact()
        transaction = WEB3.eth.waitForTransactionReceipt(transaction)
        if transaction.status != 1:
            raise RuntimeError("SC Call failed!")

        voucher_sc_address = voucher_constructor(publickey)

        session.add_all([
            Institution(
                nameInstitution=name,
                webpageInstitution=webpage,
                addressInstitution=address,
                smartcontract_id=2,
                publickeyInstitution=publickey,
                descriptionInstitution=description,
                latitude=latitude,
                longitude=longitude,
                scAddress=transaction.contractAddress,
                scAddress_voucher=voucher_sc_address,
                user=owner_inst,
            ),
            Transaction(dateTransaction=datetime.now(), smartcontract_id=2, user=owner_inst)
        ])
        session.commit()
        return jsonify({'status': 'Institution wurde erstellt'}), 201
    finally:
        session.rollback()
        session.close()


@BP.route('', methods=['PATCH'])
@auth_user
def institutions_patch(user_inst):  # pylint:disable=too-many-branches
    """
    Handles PATCH for resource <base>/api/institutions .
    :return: json response
    """
    institution_id = request.headers.get('id')
    name = request.headers.get('name')
    webpage = request.headers.get('webpage')
    address = request.headers.get('address')
    description = request.headers.get('description')
    latitude = request.headers.get('latitude')
    longitude = request.headers.get('longitude')

    if institution_id is None:
        return jsonify({'error': 'Missing parameter'}), 400

    try:
        check_params_int([institution_id])
        check_params_float([latitude, longitude])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400
    if None in [latitude, longitude] and any([latitude, longitude]):
        return jsonify({"error": "bad geo argument"}), 400

    session = DB_SESSION()
    try:
        if name:  # check if name is already taken
            if session.query(Institution).filter(Institution.nameInstitution == name).one_or_none():
                return jsonify({'error': 'name already exists'}), 400

        institution = session.query(Institution).get(institution_id)
        if institution is None:
            return jsonify({'error': 'Institution does not exist'}), 404

        # check user permission
        owner = session.query(Institution)
        owner = owner.join(Transaction, Institution.smartcontract_id == Transaction.smartcontract_id)
        owner = owner.filter(Transaction.user_id == user_inst.idUser,
                             Institution.idInstitution == institution_id).first()

        if owner is None:
            return jsonify({'error': 'no permission'}), 403

        if name:
            institution.nameInstitution = name
        if address:
            institution.addressInstitution = address
        if webpage:
            institution.webpageInstitution = webpage
        if description:
            institution.descriptionInstitution = description
        if latitude and longitude:
            institution.latitude = latitude
            institution.longitude = longitude

        session.commit()
        return jsonify({'status': 'Institution wurde bearbeitet'}), 201
    finally:
        session.rollback()
        session.close()
