"""Project Resource."""
from flask import Blueprint, request, jsonify
from backend.database.db import get_db

BP = Blueprint('user', __name__, url_prefix='/api/user')


@BP.route('', methods=['GET'])
def user_get():  # noqa
    """
    Handles GET for resource <base>/api/user .

    :return: json data of projects
    """
    args = request.args
    name_user = args.get('username')
    id_user = args.get('id')

    cursor = get_db().cursor()
    cursor.execute('use mydb')

    if name_user:
        cursor.execute('SELECT idUser, usernameUser, firstnameUser, lastnameUser, emailUser, publickeyUser, privatekeyUser FROM user WHERE usernameUser = %s',(name_user,))
        data = cursor.fetchall()
    elif id_user:
        cursor.execute('SELECT idUser, usernameUser, firstnameUser, lastnameUser, emailUser, publickeyUser, privatekeyUser FROM user WHERE idUser = %s', (id_user,))
        data = cursor.fetchall()

    names = ["id", "username", "firstname", "lastname", "email", "publickey", "privateKey"]
    json_data = []
    for result in data:
        res = dict(zip(names, result))
        res["publickey"] = res["publickey"].decode("utf-8").rstrip("\x00")
        res["privateKey"] = res["privateKey"].decode("utf-8").rstrip("\x00")
        json_data.append(res)
    return jsonify(json_data)

