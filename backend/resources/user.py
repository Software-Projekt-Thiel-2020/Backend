"""Project Resource."""
from flask import Blueprint, request, jsonify
from backend.database.db import DB_SESSION
from backend.database.model import User


BP = Blueprint('user', __name__, url_prefix='/api/user')


@BP.route('', methods=['GET'])
def user_get():
    """
    Handles GET for resource <base>/api/user .

    :return: json data of projects
    """
    args = request.args
    name_user = args.get('username')
    id_user = args.get('id')

    session = DB_SESSION()
    results = session.query(User)

    if name_user and id_user:
        return jsonify({'error': 'to many Arguments'}), 400

    if name_user:
        results = results.filter(User.usernameUser == name_user)
    elif id_user:
        results = results.filter(User.idUser == id_user)
    else:
        return jsonify({'error': 'missing Argument'}), 400

    json_data = []
    json_names = ['id', 'username', 'firstname', 'lastname', 'email', 'publickey']
    for result in results:
        json_data.append(dict(zip(json_names, [
            result.idUser,
            result.usernameUser,
            result.firstnameUser,
            result.lastnameUser,
            result.emailUser,
            result.publickeyUser.decode("utf-8").rstrip("\x00"),
        ])))

    return jsonify(json_data)
