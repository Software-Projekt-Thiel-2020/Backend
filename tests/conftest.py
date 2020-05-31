import os
import tempfile
import pytest
from backend import create_app
from backend.database import db


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
