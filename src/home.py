from flask import (
    Blueprint, render_template, session, request, send_file
)
from src.utils.db import *
from src.auth import login_required
from src.utils.utils import *
import logging
from src.generate.generate_tabular_data import generate_tabular_data

bp = Blueprint('home', __name__)

setup_daily_logger(name=__name__, path=cs.LOG_FOLDER)
logger = logging.getLogger(__name__)


@bp.route('/')
def index():
    # TODO: Handle deleting while training is in progress
    if g.user:
        runs = query_all_runs(session['user_id'])
        if len(runs) > 0:
            return render_template('home/index.html', runs=runs, logged_in=True)
        else:
            return render_template('home/index.html', logged_in=True)
    else:
        return render_template('home/index.html', logged_in=False)


@bp.route('/delete_run', methods=['POST'])
@login_required
def delete_run():
    runs = query_all_runs(user_id=session['user_id'])
    run_id = int(runs[int(request.form['index']) - 1]['id'])
    query_delete_run(run_id=run_id)
    clean_run(run_id=run_id)
    username, title = query_username_title(run_id=run_id)
    logger.info('User #{} ({}) deleted Run #{} ({})'.format(session['user_id'], username, run_id, title))
    return ''


@bp.route('/refresh_status', methods=['POST'])
@login_required
def refresh_status():
    runs = query_all_runs(user_id=session['user_id'])
    run_id = int(runs[int(request.form['index']) - 1]['id'])
    status, update_time = query_check_status(run_id=run_id)
    return {'status': status, 'timestamp': update_time}


@bp.route('/download_data', methods=['POST'])
@login_required
def download_data():
    runs = query_all_runs(user_id=session['user_id'])
    run_id = int(runs[int(request.form['index']) - 1]['id'])
    username, title = query_username_title(run_id=run_id)
    file = os.path.join(current_app.root_path, os.path.basename(cs.OUTPUT_FOLDER), username, title + '.zip')
    logger.info('User #{} ({}) downloaded the originally generated data from Run #{} ({})'.format(session['user_id'], username, run_id, title))
    return send_file(file, mimetype='zip', as_attachment=True)


@bp.route('/gen_more_data', methods=['POST'])
@login_required
def gen_more_data():
    # TODO: Fill in get request inputs
    # TODO: Add more logging
    # TODO: Finish gen more data code
    if 'index' in request.form.keys():  # Entering page for the first time
        runs = query_all_runs(session['user_id'])
        session['run_id'] = int(runs[int(request.form['index']) - 1]['id'])
        session['title'] = runs[int(request.form['index']) - 1]['title']
        session['dep_var'] = runs[int(request.form['index']) - 1]['depvar']
        session['format'] = runs[int(request.form['index']) - 1]['format']
        dep_choices = parse_dep(directory=current_app.config['UPLOAD_FOLDER'], run_id=session['run_id'], dep_var=session['dep_var'])
        return render_template('home/gen_more_data.html', title=session['title'], dep_var=session['dep_var'],
                               dep_choices=dep_choices, max_examples_per_class='{:,d}'.format(cs.MAX_EXAMPLE_PER_CLASS))

    if 'download_button' in request.form.keys():  # User clicked Download
        aug = query_incr_augs(session['run_id'])
        username, title = query_username_title(run_id=session['run_id'])
        create_gen_dict(request_form=request.form, directory=cs.RUN_FOLDER, username=username, title=title, aug=aug)
        logger.info('User #{} ({}) downloaded additionally generated data ({}) from Run #{} ({})'.format(session['user_id'], username, str(aug), session['run_id'], title))
        if session['format'] == 'Tabular':
            generate_tabular_data(run_id=session['run_id'], username=username, title=title, aug=aug)
            file = os.path.join(current_app.root_path, os.path.basename(cs.OUTPUT_FOLDER), username, title + ' Additional Data ' + str(aug) + '.zip')
            return send_file(file, mimetype='zip', as_attachment=True)
        else:  # Image
            pass
