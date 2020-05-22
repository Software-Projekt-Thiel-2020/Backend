"""
Handles the register ressources.
See rest api documentation for further information.
"""
from flask import Blueprint
from backend.util.db import get_db

BP = Blueprint('sample', __name__, url_prefix='/sample')  # set blueprint name and resource path


@BP.route('', methods=['GET'])
def register_get():  # noqa
    """
    Handles GET for resource <base>/api/sample .

    :return: DB version
    """
    cursor = get_db().cursor()

    cursor.execute('SELECT VERSION()')  # execute statemant
    version = cursor.fetchone()  # fetch database response | see fetchmany(size=x) and fetchall()

    return version[0], 200


@BP.route('', methods=['POST'])
def register_post():  # noqa
    """
    Handles POST for resource <base>/api/sample .

    :return: ""
    """
    # do stuff
    return "", 201
