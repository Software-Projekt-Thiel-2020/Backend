"""Test Misc."""
import os
import pytest

from click.testing import CliRunner

from backend.blockstack_auth import BlockstackAuth
from backend.database import db
from backend.database.model import User
from backend.resources.helpers import auth_user
from backend.database.db import DB_SESSION
from tests.test_blockstackauth import TOKEN_1, TOKEN_2, TOKEN_3, TOKEN_INVALID_EXP, TOKEN_INVALID_IAT, TOKEN_INVALID_ISS, TOKEN_INVALID_ISS2, TOKEN_INVALID_PK, TOKEN_INVALID_USER

runner = CliRunner()


@pytest.fixture
def testclient(client):

    @client.application.route('/test')
    @auth_user
    def test(user_inst):  # noqa
        return 'OK!', 200
    yield client


def test_init_db_command():
    # save old env-variables
    env_before_app = os.environ.get('FLASK_APP')
    env_before_env = os.environ.get('FLASK_ENV')

    os.environ['FLASK_APP'] = "backend"  # set them to our values
    os.environ['FLASK_ENV'] = "development"

    response = runner.invoke(db.init_db_command, [])

    if env_before_app:
        os.environ['FLASK_APP'] = env_before_app  # reset env variables
    else:
        os.environ.pop('FLASK_APP')
    if env_before_app:
        os.environ['FLASK_ENV'] = env_before_env  # reset env variables
    else:
        os.environ.pop('FLASK_ENV')

    assert response.exit_code == 0
    assert "Initialized and cleared the database." in response.output


def test_auth_user_no_token1(testclient):
    headers = {}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 401


def test_auth_user_no_token2(testclient):
    headers = {"authToken": ""}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 401


def test_auth_user_no_token3(testclient):
    headers = {"authToken": "test"}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 401


def test_auth_user_valid1(testclient):
    headers = {"authToken": TOKEN_1}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 200


def test_auth_user_valid2(testclient):
    headers = {"authToken": TOKEN_2}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 200


def test_auth_user_valid3(testclient):
    session = DB_SESSION()
    res = session.query(User).filter(User.idUser == 6).one()
    res.authToken = ""
    session.commit()

    headers = {"authToken": TOKEN_1}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 200

    res = session.query(User).filter(User.idUser == 6).one()
    assert res.authToken == BlockstackAuth.short_jwt(TOKEN_1)
    session.rollback()
    session.close()


def test_auth_user_not_registered1(testclient):
    headers = {"authToken": TOKEN_3}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 404


def test_auth_user_not_registered2(testclient):
    headers = {"authToken": TOKEN_INVALID_USER}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 404


def test_auth_user_invalid1(testclient):
    headers = {"authToken": TOKEN_INVALID_EXP}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 401


def test_auth_user_invalid2(testclient):
    headers = {"authToken": TOKEN_INVALID_IAT}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 401


def test_auth_user_invalid3(testclient):
    headers = {"authToken": TOKEN_INVALID_ISS}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 401


def test_auth_user_invalid4(testclient):
    headers = {"authToken": TOKEN_INVALID_ISS2}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 401


def test_auth_user_invalid5(testclient):
    headers = {"authToken": TOKEN_INVALID_PK}
    res = testclient.get('/test', headers=headers)
    assert res._status_code == 401
