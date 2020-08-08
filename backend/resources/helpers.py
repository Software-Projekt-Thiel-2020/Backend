from functools import wraps
from typing import List

from flask import request, abort
from jwt import DecodeError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from backend.blockstack_auth import BlockstackAuth
from backend.database.db import DB_SESSION
from backend.database.model import User


def check_params_int(params: List) -> List[int]:
    """
    Checks a List of params if they are really castable to int.

    :except: ValueError if one of the Parameters isn't an int
    :return: -
    """
    ret = []
    for param in params:
        if param:
            ret.append(int(param) if param else param)
    return ret


def check_params_float(params: List) -> List[float]:
    """
    Checks a List of params if they are really castable to float.

    :except: ValueError if one of the Parameters isn't an float
    :return: -
    """
    ret = []
    for param in params:
        ret.append(float(param) if param else param)
    return ret


def db_session_dec(func):
    """
    Decorator for resources that need a DB-Session.

    :param func: function to decorate
    :return:
    """

    @wraps(func)
    def decorated_function(*args, **kws):
        sess: Session = None
        try:
            sess = DB_SESSION()
            return func(sess, *args, **kws)
        finally:
            if sess:
                sess.rollback()
                sess.close()

    return decorated_function


def auth_user(func):
    """
    Decorator for resources that need authentication.

    Verifys the given authToken belongs to a specific user, saves it to the DB (for "caching"),
    returns the User-instance it verifys

    :param func: function to decorate
    :return:
    """

    @wraps(func)
    @db_session_dec
    def decorated_function(session, *args, **kws):
        if 'authToken' not in request.headers:
            abort(401)

        try:
            shortened_token = BlockstackAuth.short_jwt(request.headers['authToken'])  # implicitly checks if its a token
            username = BlockstackAuth.get_username_from_token(shortened_token)

            user_inst: User = session.query(User).filter(User.usernameUser == username).one()

            # check if token matches "cached" token, if thats the case, we are done here... else:
            if shortened_token != user_inst.authToken:
                # verify token:
                if BlockstackAuth.verify_auth_response(shortened_token):
                    # token is valid, save it to DB
                    user_inst.authToken = shortened_token
                    session.commit()
                else:
                    # token invalid, abort
                    abort(401)

            else:  # token is valid
                pass
        except NoResultFound:
            # User needs to register
            abort(404)
        except (KeyError, ValueError, DecodeError):  # jwt decode errors
            abort(401)
        else:
            tmp = func(user_inst, *args, **kws)
            session.commit()  # if user_inst get's changed
            return tmp

    return decorated_function
