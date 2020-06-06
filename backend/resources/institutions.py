"""Institution Resource."""
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
    json_names = ["id", "name", "webpage"]

    if id_institution:
        institution = results.filter(Institution.idInstitution == id_institution).first()
        if not institution:
            return jsonify({'error': 'Institution does not exist'}), 400

        json_data.append(dict(zip(json_names, [
            institution.idInstitution,
            institution.nameInstitution,
            institution.webpageInstitution,
        ])))
        return jsonify(json_data)

    for result in results:
        json_data.append(dict(zip(json_names, [
            result.idInstitution,
            result.nameInstitution,
            result.webpageInstitution,
        ])))

    return jsonify(json_data)


@BP.route('', methods=['POST'])
@auth_user
def institutions_post(user_inst):  # pylint:disable=unused-argument
    """
    Handles POST for resource <base>/api/institutions .
    :return: json response
    """
    name = request.headers.get('name')
    web = request.headers.get('webpage')

    session = DB_SESSION()

    # check if name is already taken
    name_exist = session.query(Institution).filter(Institution.nameInstitution == name).first()
    if name_exist:
        return jsonify({'error': 'name already exists'}), 400

    # Todo: smartcontract_id
    try:
        session.add(Institution(nameInstitution=name, webpageInstitution=web, smartcontract_id=1))
        session.commit()
    except SQLAlchemyError:
        return jsonify({'error': 'Database error!'}), 400

    return jsonify({'status': 'Institution wurde erstellt'}), 201


@BP.route('', methods=['PATCH'])
@auth_user
def institutions_patch(user_inst):  # pylint:disable=unused-argument
    """
    Handles PATCH for resource <base>/api/institutions .
    :return: json response
    """
    name = request.headers.get('name')
    web = request.headers.get('webpage')
    institution_id = request.headers.get('id')

    if web is None and name is None:
        return jsonify({'error': 'missing patch argument'}), 400

    session = DB_SESSION()

    # check user permission
    owner = session.query(Institution)
    owner = owner.join(Transaction, Institution.smartcontract_id == Transaction.smartcontract_id)
    owner = owner.filter(Transaction.user_id == user_inst.idUser, Institution.idInstitution == institution_id).first()

    if owner:
        # check if name is already taken
        name_exist = session.query(Institution).filter(Institution.nameInstitution == name).first()

        institution = session.query(Institution).get(institution_id)
        if institution is None:
            return jsonify({'error': 'Institution does not exist'}), 404

        try:
            if web is not None:
                institution.webpageInstitution = web
            if not name_exist:
                institution.nameInstitution = name
            else:
                return jsonify({'error': 'name already exists'}), 400

            session.commit()
            return jsonify({'status': 'Institution wurde bearbeitet'}), 201

        except SQLAlchemyError:
            return jsonify({'error': 'Database error!'}), 400

    return jsonify({'error': 'no permission'}), 404
