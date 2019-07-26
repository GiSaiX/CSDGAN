import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def query_init_run(title, user_id, format, filesize):
    """Insert rows into db for a run and the initial status"""
    db = get_db()
    # run table
    db.execute(
        'INSERT INTO run ('
        'title, user_id, format, filesize)'
        'VALUES'
        '(?, ?, ?, ?)',
        (title, user_id, format, filesize)
    )
    db.commit()
    # retrieve run id
    run_id = db.execute(
        'SELECT max(id) FROM run'
    ).fetchone()
    # status table
    db.execute(
        'INSERT INTO status ('
        'run_id, status_id)'
        'VALUES'
        '(?, ?)',
        (run_id[0], 1)
    )
    db.commit()
    return run_id[0]


def query_next_status(run_id):
    """Updates status table with the next status"""
    db = get_db()
    current_status = db.execute(
        'SELECT max(status_id) FROM status WHERE run_id = ?', (run_id,)
    ).fetchone()
    db.execute(
        'INSERT INTO status ('
        'run_id, status_id)'
        'VALUES'
        '(?, ?)',
        (run_id, current_status[0] + 1)
    )
    db.commit()


def query_run_failed(run_id):
    """Updates status table with failure"""
    db = get_db()
    # max status is always the fail status
    max_status = db.execute(
        'SELECT max(id) FROM status_info'
    ).fetchone()
    db.execute(
        'INSERT INTO status ('
        'run_id, status_id)'
        'VALUES'
        '(?, ?)',
        (run_id, max_status[0])
    )
    db.commit()


def query_title(run_id):
    """Retrieves the title associated with the specified run_id"""
    db = get_db()
    title = db.execute(
        'SELECT title FROM run WHERE id = ?', (run_id,)
    ).fetchone()
    return title[0]


def query_all_runs(user_id):
    """Retrieves information on all runs associated with the specified user_id"""
    db = get_db()
    result = db.execute(
        'SELECT run.title, run.start_time, run.format, status.update_time, status_info.descr '
        'FROM run '
        'LEFT JOIN ('
        '   SELECT a.run_id, a.status_id, a.update_time FROM status as a '
        '   INNER JOIN ('
        '       SELECT run_id, max(status_id) as status_id FROM status GROUP BY run_id'
        '   ) as b on a.run_id = b.run_id and a.status_id = b.status_id'
        ') as status on run.id = status.run_id '
        'LEFT JOIN status_info on status.status_id = status_info.id '
        'WHERE run.user_id = ?',
        (user_id,)
    ).fetchall()
    return result