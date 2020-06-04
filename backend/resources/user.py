"""User Resource."""
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from backend.database.db import DB_SESSION
from backend.database.model import User
from backend.resources.helpers import auth_user

BP = Blueprint('user', __name__, url_prefix='/api/users')


@BP.route('', methods=['GET'])
def users_get():
    """
    Handles GET for resource <base>/api/users .

    :return: json data of users
    """
    args = request.args
    name_user = args.get('username')

    session = DB_SESSION()
    results = session.query(User)

    if name_user:
        results = results.filter(User.usernameUser == name_user)  # ToDo: too narrow?
    else:
        return jsonify({'error': 'missing Argument'}), 400

    json_data = []
    for result in results:
        json_data.append({
            'id': result.idUser,
            'username': result.usernameUser,
            'firstname': result.firstnameUser,
            'lastname': result.lastnameUser,
            'email': result.emailUser,
            'publickey': result.publickeyUser.decode("utf-8").rstrip("\x00"),
        })

    return jsonify(json_data)


@BP.route('/<id>', methods=['GET'])
def user_id(id):    # noqa
    """
    Handles GET for resource <base>/api/users/<id> .
    :parameter id of a User
    :return: the User
    """
    id_user = id

    try:
        if id_user:
            int(id_user)
    except ValueError:
        return jsonify({"error": "bad argument"}), 400

    session = DB_SESSION()
    results = session.query(User)

    try:
        if id_user:
            results = results.filter(User.idUser == id_user).one()
    except NoResultFound:
        return jsonify(), 404
    except SQLAlchemyError:
        return jsonify(), 200

    json_data = {
        'id': results.idUser,
        'username': results.usernameUser,
        'firstname': results.firstnameUser,
        'lastname': results.lastnameUser,
        'email': results.emailUser,
        'publickey': results.publickeyUser.decode("utf-8").rstrip("\x00"),
    }

    return jsonify(json_data), 200


@BP.route('', methods=['PUT'])
@auth_user
def user_put(user_inst):
    """
    Handles POST for resource <base>/api/users .
    :return: "{'status': 'Daten wurden geändert'}", 200
    """
    args = request.args

    auth_token = args.get('authToken', default=None)
    firstname = args.get('firstname', default=None)
    lastname = args.get('lastname', default=None)
    email = args.get('email', default=None)

    if auth_token is None:
        return jsonify({'error': 'Not logged in'}), 403

    session = DB_SESSION()

    try:
        if firstname is not None:
            user_inst.firstnameUser = firstname
        if lastname is not None:
            user_inst.lastnameUser = lastname
        if email is not None:
            user_inst.emailUser = email
        session.commit()
    except SQLAlchemyError:
        return jsonify(), 200

    return jsonify('Daten wurden geändert'), 200
