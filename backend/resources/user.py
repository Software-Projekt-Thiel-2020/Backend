"""User Resource."""
from flask import Blueprint, request, jsonify
from backend.database.db import DB_SESSION
from backend.database.model import User


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
