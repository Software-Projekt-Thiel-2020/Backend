"""Handles the functionality for the database access."""
import configparser
import click
import mysql.connector as mariadb
from flask import current_app, g
from flask.cli import with_appcontext

CFG_PARSER = configparser.ConfigParser()
CFG_PARSER.read("backend_config.ini")

# set the configuration of the database connection
DB_CONFIG = {
    'user': CFG_PARSER["DB"]["USER"],
    'password': CFG_PARSER["DB"]["PASSWORD"],
    'host': CFG_PARSER["DB"]["HOST"],
}


def get_db():
    """
    Get the database.

    :return: the database object
    """
    if 'db' not in g:
        g.db = mariadb.connect(**DB_CONFIG)
    return g.db


def close_db(_):
    """
    Close the database.
    :return: -
    """
    try:
        g.pop('db', None).close()
    except AttributeError:
        pass


def init_db():
    """
    Initiates the database with the schema file.

    :return: -
    """
    cursor = get_db().cursor()
    with current_app.open_resource('sql_scripts/schema.sql') as sql_file:
        commands = sql_file.read().decode('utf-8').split(';')
        commands = commands[: len(commands) - 1]
        for command in commands:
            cursor.execute(command)


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
