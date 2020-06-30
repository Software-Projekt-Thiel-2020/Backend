"""Institution Resource."""
from datetime import datetime

import validators
from flask import Blueprint, request, jsonify
from geopy import distance

from backend.database.db import DB_SESSION
from backend.database.model import Institution, Transaction, User
from backend.resources.helpers import auth_user, check_params_int

BP = Blueprint('institutions', __name__, url_prefix='/api/institutions')  # set blueprint name and resource path


@BP.route('', methods=['GET'])
def institutions_get():
    """
    Handles GET for resource <base>/api/institutions .

    :return: json data of institutions
    """
    id_institution = request.args.get('id', type=int)
    radius = request.args.get('radius', type=int)
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    name_institution = request.args.get('name')
    has_vouchers = request.args.get('has_vouchers')

    try:
        check_params_int([id_institution, radius, has_vouchers])
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    if None in [radius, latitude, longitude] and any([radius, latitude, longitude]):
        return jsonify({"error": "bad geo argument"}), 400

    session = DB_SESSION()
    results = session.query(Institution)

    json_data = []

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
            "description": result.descriptionInstitution
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

    if not user_inst.group == "support":
        return jsonify({'error': 'Forbidden'}), 403

    if None in [name, address]:  # or publickey is None:
        return jsonify({'error': 'Missing parameter'}), 400

    if webpage is not None and not validators.url(webpage):
        return jsonify({'error': 'webpage is not a valid url'}), 400

    session = DB_SESSION()
    owner_inst: User = session.query(User).filter(User.usernameUser == username).one_or_none()
    if owner_inst is None:
        return jsonify({'error': 'username not found'}), 400

    # check if name is already taken
    name_exist = session.query(Institution).filter(Institution.nameInstitution == name).first()
    if name_exist:
        return jsonify({'error': 'name already exists'}), 400

    # Todo: smartcontract_id
    institution_inst = Institution(nameInstitution=name, webpageInstitution=webpage, addressInstitution=address,
                                   smartcontract_id=2, publickeyInstitution=publickey, descriptionInstitution=description)
    transaction_inst = Transaction(dateTransaction=datetime.now(), smartcontract_id=2, user=owner_inst)

    session.add_all([institution_inst, transaction_inst])
    session.commit()

    return jsonify({'status': 'Institution wurde erstellt'}), 201


@BP.route('', methods=['PATCH'])
@auth_user
def institutions_patch(user_inst):
    """
    Handles PATCH for resource <base>/api/institutions .
    :return: json response
    """
    institution_id = request.headers.get('id')
    name = request.headers.get('name')
    webpage = request.headers.get('webpage')
    address = request.headers.get('address')
    description = request.headers.get('description')

    if institution_id is None:
        return jsonify({'error': 'Missing parameter'}), 400

    session = DB_SESSION()

    if name:  # check if name is already taken
        name_exist = session.query(Institution).filter(Institution.nameInstitution == name).one_or_none()
        if name_exist:
            return jsonify({'error': 'name already exists'}), 400

    institution = session.query(Institution).get(institution_id)
    if institution is None:
        return jsonify({'error': 'Institution does not exist'}), 404

    # check user permission
    owner = session.query(Institution)
    owner = owner.join(Transaction, Institution.smartcontract_id == Transaction.smartcontract_id)
    owner = owner.filter(Transaction.user_id == user_inst.idUser, Institution.idInstitution == institution_id).first()

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

    session.commit()
    return jsonify({'status': 'Institution wurde bearbeitet'}), 201
