"""User Resource."""
import validators
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

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
        results = results.filter(User.usernameUser.contains(name_user))
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
def user_id(id):  # noqa
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
    Handles PUT for resource <base>/api/users .
    :return: "{'status': 'Daten wurden geändert'}", 200
    """
    firstname = request.headers.get('firstname', default=None)
    lastname = request.headers.get('lastname', default=None)
    email = request.headers.get('email', default=None)

    if email is not None and not validators.email(email):
        return jsonify({'error': 'email is not a valid email'}), 400

    try:
        if firstname is not None:
            user_inst.firstnameUser = firstname
        if lastname is not None:
            user_inst.lastnameUser = lastname
        if email is not None:
            user_inst.emailUser = email
    except SQLAlchemyError:
        return jsonify({'error': 'Database error'}), 500

    return jsonify({'status': 'Daten wurden geändert'}), 200


@BP.route('', methods=['POST'])
@auth_user
def user_post(user_inst):
    """
    Handles POST for resource <base>/api/users .
    :return: "{'status': 'User registered'}", 200
    """
    username = request.headers.get('username', default=None)
    firstname = request.headers.get('firstname', default=None)
    lastname = request.headers.get('lastname', default=None)
    email = request.headers.get('email', default=None)
    publickey = request.headers.get('publickey', default=None)
    privatekey = request.headers.get('privatekey', default=None)
    auth_token = request.headers.get('authToken', default=None)

    if None in [username, firstname, lastname, email, publickey, privatekey]:
        return jsonify({'error': 'Missing parameter'}), 403

    session = DB_SESSION()
    results = session.query(func.max(User.idUser).label("max_id"))

    id_user = int(results.one().max_id)

    try:
        user_inst = User(idUser=id_user + 1,
            usernameUser=username,
            firstnameUser=firstname,
            lastnameUser=lastname,
            emailUser=email,
            publickeyUser=bytes(publickey, encoding="utf-8"),
            privatekeyUser=bytes(privatekey, encoding="utf-8"),
            authToken=auth_token)
    except SQLAlchemyError:
        return jsonify({'status': 'Database error'}), 400

    try:
        session.add(user_inst)
        session.commit()
    except SQLAlchemyError:
        return jsonify({'status': 'Commit error!'}), 400

    return jsonify({'status': 'User registered'}), 201
