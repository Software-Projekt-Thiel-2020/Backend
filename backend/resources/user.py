"""User Resource."""
import re
import validators
from flask import Blueprint, request, jsonify
from jwt import DecodeError
from sqlalchemy.orm.exc import NoResultFound

from backend.blockstack_auth import BlockstackAuth
from backend.database.model import User
from backend.resources.helpers import auth_user, db_session_dec, check_name_length
from backend.smart_contracts.web3 import WEB3

BP = Blueprint('user', __name__, url_prefix='/api/users')


@BP.route('', methods=['GET'])
@db_session_dec
def users_get(session):
    """
    Handles GET for resource <base>/api/users .

    :return: json data of users
    """
    args = request.args
    name_user = args.get('username')

    results = session.query(User)

    if name_user:
        results = results.filter(User.usernameUser.contains(name_user))
    else:
        return jsonify({'error': 'missing Argument'}), 400

    json_data = []
    for result in results:
        balance = WEB3.eth.getBalance(result.publickeyUser)

        json_data.append({
            'id': result.idUser,
            'username': result.usernameUser,
            'firstname': result.firstnameUser,
            'lastname': result.lastnameUser,
            'email': result.emailUser,
            'group': result.group,
            'publickey': result.publickeyUser,
            'balance': str(balance),
        })

    return jsonify(json_data)


@BP.route('/<id>', methods=['GET'])
@db_session_dec
def user_id(session, id):  # pylint:disable=redefined-builtin,invalid-name
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
        return jsonify({'error': 'bad argument'}), 400

    results = session.query(User)

    try:
        if id_user:
            results = results.filter(User.idUser == id_user).one()
            balance = WEB3.eth.getBalance(results.publickeyUser)
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404

    json_data = {
        'id': results.idUser,
        'username': results.usernameUser,
        'firstname': results.firstnameUser,
        'lastname': results.lastnameUser,
        'email': results.emailUser,
        'group': results.group,
        'publickey': results.publickeyUser,
        'balance': str(balance),
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
        return jsonify({'error': 'email is not valid'}), 400

    if None in [firstname, lastname, email]:
        return jsonify({'error': 'Missing parameter'}), 400

    if "" in [firstname, lastname, email]:
        return jsonify({'error': 'Empty parameter'}), 400

    if re.match("^[a-zA-ZäÄöÖüÜ ,.'-]+$", firstname) is None or re.match("^[a-zA-ZäÄöÖüÜ ,.'-]+$", lastname) is None:
        return jsonify({'error': 'Firstname and/or lastname must contain only alphanumeric characters'}), 400

    try:
        check_name_length(firstname, 44)
        check_name_length(lastname, 44)

    except ValueError:
        return jsonify({"error": "bad name argument"}), 400

    user_inst.firstnameUser = firstname
    user_inst.lastnameUser = lastname
    user_inst.emailUser = email

    return jsonify({'status': 'changed'}), 200


@BP.route('', methods=['POST'])
@db_session_dec
def user_post(session):
    """
    Handles POST for resource <base>/api/users .
    :return: "{'status': 'User registered'}", 200
    """
    username = request.headers.get('username', default=None)
    firstname = request.headers.get('firstname', default=None)
    lastname = request.headers.get('lastname', default=None)
    email = request.headers.get('email', default=None)
    auth_token = request.headers.get('authToken', default=None)

    if None in [username, firstname, lastname, email, auth_token]:
        return jsonify({'error': 'Missing parameter'}), 400

    if "" in [username, firstname, lastname, email, auth_token]:
        return jsonify({'error': "Empty parameter"}), 400

    if re.match("^[a-zA-ZäÄöÖüÜ ,.'-]+$", firstname) is None or re.match("^[a-zA-ZäÄöÖüÜ ,.'-]+$", lastname) is None:
        return jsonify({'error': 'Firstname and/or lastname must contain only alphanumeric characters'}), 400

    acc = WEB3.eth.account.create()

    try:
        check_name_length(firstname, 44)
        check_name_length(lastname, 44)
        check_name_length(username, 44)

    except ValueError:
        return jsonify({"error": "bad name argument"}), 400

    try:
        shortened_token = BlockstackAuth.short_jwt(auth_token)
        username_token = BlockstackAuth.get_username_from_token(shortened_token)
        if username_token != username:
            return jsonify({'error': 'username in token doesnt match username'}), 400

        res = session.query(User).filter(User.usernameUser == username).one_or_none()
        if res is not None:
            return jsonify({'status': 'User is already registered'}), 400

        user_inst = User(usernameUser=username,
                         firstnameUser=firstname,
                         lastnameUser=lastname,
                         emailUser=email,
                         authToken=shortened_token,
                         publickeyUser=acc.address,
                         privatekeyUser=acc.key)
    except (KeyError, ValueError, DecodeError):  # jwt decode errors
        return jsonify({'status': 'Invalid JWT'}), 400

    session.add(user_inst)
    session.commit()
    return jsonify({'status': 'User registered'}), 201
