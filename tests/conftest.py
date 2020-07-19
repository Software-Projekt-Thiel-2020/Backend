import os
import tempfile

import pytest

from backend import create_app
from backend.database import db
from backend.smart_contracts.web3 import WEB3

evm_snapshot_global = None


@pytest.hookimpl()
def pytest_sessionstart(session):
    global evm_snapshot_global
    evm_snapshot_global = WEB3.provider.make_request("evm_snapshot", [])
    print("pytest_sessionstart", evm_snapshot_global)


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    WEB3.provider.make_request("evm_revert", [int(evm_snapshot_global['result'], 16), ])
    print("pytest_sessionfinish", evm_snapshot_global)


@pytest.fixture
def client_w_eth():
    db.init_db()

    db_fd, tmpfile = tempfile.mkstemp()
    conf = {
        "DATABASE": tmpfile,
        "TESTING": True
    }

    app = create_app(conf)

    evm_snapshot = WEB3.provider.make_request("evm_snapshot", [])
    WEB3.eth.sendTransaction({'from': WEB3.eth.accounts[9],
                              'to': '0x865fefF6a8503405f8a316e53039dc8332a5A60b',  # sw2020testuser1.id.blockstack
                              'value': 1 * 10 ** 18})
    WEB3.eth.sendTransaction({'from': WEB3.eth.accounts[9],
                              'to': '0x7Dca2Ba711f089C608ABe8C6F59Fe7B5F84fced8',  # sw2020testuser2.id.blockstack
                              'value': 1 * 10 ** 18})

    with app.test_client() as client:
        yield client

    WEB3.provider.make_request("evm_revert", [int(evm_snapshot['result'], 16), ])
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def client():
    db.init_db()

    db_fd, tmpfile = tempfile.mkstemp()
    conf = {
        "DATABASE": tmpfile,
        "TESTING": True
    }

    app = create_app(conf)

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
