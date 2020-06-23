"""User Resource."""
import validators
from flask import Blueprint, request, jsonify
from jwt import DecodeError
from sqlalchemy.orm.exc import NoResultFound

from backend.blockstack_auth import BlockstackAuth
from backend.database.db import DB_SESSION
from backend.database.model import User
from backend.resources.helpers import auth_user

from web3 import Web3
from eth_account import Account
import web3.exceptions as web3_exceptions

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

    gnache_url = "HTTP://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(gnache_url))
    
    if not web3.isConnected():
        return jsonify({'error': 'cant connect to Blockchain'}), 400
    
    json_data = []
    for result in results:
        try:
            balance = web3.eth.getBalance(result.publickeyUser.decode("utf-8"))
            balance = float((web3.fromWei(balance, 'ether')))
        except web3_exceptions.InvalidAddress:
            balance = -1
            return jsonify({'error': 'given publickey is not valid'}), 400

        json_data.append({
            'id': result.idUser,
            'username': result.usernameUser,
            'firstname': result.firstnameUser,
            'lastname': result.lastnameUser,
            'email': result.emailUser,
            'publickey': result.publickeyUser.decode("utf-8"),
            'balance': balance,
        })

    return jsonify(json_data)


@BP.route('/<id>', methods=['GET'])
def user_id(id):  # pylint:disable=redefined-builtin,invalid-name
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

    session = DB_SESSION()
    results = session.query(User)

    try:
        if id_user:
            results = results.filter(User.idUser == id_user).one()
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404

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
        return jsonify({'error': 'email is not valid'}), 400

    if firstname is not None:
        user_inst.firstnameUser = firstname
    if lastname is not None:
        user_inst.lastnameUser = lastname
    if email is not None:
        user_inst.emailUser = email

    return jsonify({'status': 'changed'}), 200


@BP.route('', methods=['POST'])
def user_post():
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

    gnache_url = "HTTP://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(gnache_url))
    acc = Account.create('ssdasadsa asdsd as das dsad as')

    if not web3.isConnected():
        return jsonify({'error': 'cant connect to Blockchain'}), 400

    session = DB_SESSION()

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
                         publickeyUser=bytes(acc.address, encoding="utf-8"),
                         privatekeyUser=acc.key)
    except (KeyError, ValueError, DecodeError) as e:  # jwt decode errors
        print(e)
        return jsonify({'status': 'Invalid JWT'}), 400

    session.add(user_inst)
    session.commit()
    return jsonify({'status': 'User registered'}), 201
