## @package backend.util.db
#  @author Sebastian Steinmeyer
#  Handles the functionality for the database access
import mysql.connector as mariadb
import click
from flask import current_app, g
from flask.cli import with_appcontext

## Get the database.
#  @return the database object
def get_db():
    if 'db' not in g:
        conn = mariadb.connect(
            user='root',
            password='softwareprojekt2020',
            host="localhost",
            database='mydb'
        )
        g.db = conn.cursor()
    return g.db

## Close the database.
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

## Initiates the database with the schema file.
def init_db():
    conn = mariadb.connect(
        user='root',
        password='softwareprojekt2020',
        host="localhost")
    db = conn.cursor()
    with current_app.open_resource('sql_scripts/test_schema.sql') as f:
        commands = f.read().decode('utf-8').split(';')
        for command in commands:
            db.execute(command)
        

## Defines the flask command for initializing the database.
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized and cleared the database.')

## Adds the commands and close context to the given app.
#  @param app the app to register the commands in
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
