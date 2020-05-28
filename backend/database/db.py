"""Handles the functionality for the database access."""
import configparser
import click
from flask.cli import with_appcontext
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from backend.database.model import BASE, add_sample_data

CFG_PARSER: configparser.ConfigParser = configparser.ConfigParser()
CFG_PARSER.read("backend_config.ini")

# Set the configuration of the database connection
DB_CONFIG: dict = {
    'user': CFG_PARSER["Database"]["USER"],
    'password': CFG_PARSER["Database"]["PASSWORD"],
    'host': CFG_PARSER["Database"]["HOST"],
}

# Create DB Engine
DB_URI: str = 'mysql+pymysql://' + DB_CONFIG['user'] + ':' + DB_CONFIG['password'] + '@' + DB_CONFIG['host'] + '/mydb'
ENGINE = create_engine(DB_URI)

# Bind engine to metadata of the BASE (our model)
BASE.metadata.bind = ENGINE

# Create DB Session
DB_SESSION: scoped_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))


def close_db(_):
    """
    Close the database session.
    :return: -
    """
    DB_SESSION()


def init_db():
    """
    Initiates the database from the ORM model.

    :return: -
    """
    BASE.metadata.drop_all(ENGINE)
    BASE.metadata.create_all(ENGINE)
    add_sample_data(DB_SESSION)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Defines the flask command for initializing the database.

    :return: -
    """
    init_db()
    click.echo('Initialized and cleared the database.')


def init_app(app):
    """
    Adds the commands and close context to the given app.

    :param app: the app the commands should registered to
    :return: -
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
