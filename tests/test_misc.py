"""Test Misc."""
import os

from click.testing import CliRunner
from backend.database import db

runner = CliRunner()


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
