"""Institution Resource."""
from datetime import datetime

import validators
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from backend.database.db import DB_SESSION
from backend.database.model import Institution, Transaction
from backend.resources.helpers import auth_user

BP = Blueprint('institutions', __name__, url_prefix='/api/institutions')  # set blueprint name and resource path


@BP.route('', methods=['GET'])
def institutions_get():
    """
    Handles GET for resource <base>/api/institutions .

    :return: json data of institutions
    """
    id_institution = request.args.get('id', type=int)

    session = DB_SESSION()
    results = session.query(Institution)

    json_data = []

    if id_institution:
        results = results.filter(Institution.idInstitution == id_institution)

    for result in results:
        json_data.append({
            "id": result.idInstitution,
            "name": result.nameInstitution,
            "webpage": result.webpageInstitution,
            "address": result.addressInstitution,
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

    if None in [name, address]:
        return jsonify({'error': 'Missing parameter'}), 400

    if webpage is not None and not validators.url(webpage):
        return jsonify({'error': 'webpage is not a valid url'}), 400

    session = DB_SESSION()

    # check if name is already taken
    name_exist = session.query(Institution).filter(Institution.nameInstitution == name).first()
    if name_exist:
        return jsonify({'error': 'name already exists'}), 400

    # Todo: smartcontract_id
    try:
        institution_inst = Institution(nameInstitution=name, webpageInstitution=webpage, addressInstitution=address,
                                       smartcontract_id=2)
        transaction_inst = Transaction(dateTransaction=datetime.now(), smartcontract_id=2, user=user_inst)

        session.add_all([institution_inst, transaction_inst])
        session.commit()

        return jsonify({'status': 'Institution wurde erstellt'}), 201
    except SQLAlchemyError:
        return jsonify({'error': 'Database error!'}), 400


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
    try:
        if name:
            institution.nameInstitution = name
        if address:
            institution.addressInstitution = address
        if webpage:
            institution.webpageInstitution = webpage

        session.commit()
        return jsonify({'status': 'Institution wurde bearbeitet'}), 201
    except SQLAlchemyError:
        return jsonify({'error': 'Database error!'}), 400
