import click
from flask import g, current_app
from flask.cli import with_appcontext

from .utils import MongoHandler


def get_db():
    """

    :return:
    """
    if 'db' not in g:
        g.db = MongoHandler(host=current_app.config['MONGO_HOST'], port=current_app.config['MONGO_PORT'])

    return g.db


def close_db(e=None):
    """

    :param e:
    :return:
    """
    db = g.pop('db', None)

    if db is not None:
        db.close_client()


def init_db():
    """

    :return:
    """
    pass


@click.command('init-db')
@with_appcontext
def init_db_command():
    """

    :return:
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """

    :param app:
    :return:
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
