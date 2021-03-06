import CSDGAN.utils.constants as cs
import CSDGAN.utils.db as db
import CSDGAN.utils.utils as cu

import logging
import os
import pickle as pkl
import pandas as pd
import numpy as np


def generate_tabular_data(run_id, username, title, aug=None):
    """
    Loads a tabular CGAN created by train_tabular_model.py. Generates data based on user specifications in pre-built gen_dict.pkl.
    :param aug: Whether this is part of the standard run or generating additional data
    """
    if aug is None:
        run_id = str(run_id)
        db.query_verify_live_run(run_id=run_id)

        cu.setup_run_logger(name='gen_func', username=username, title=title)
        logger = logging.getLogger('gen_func')

    try:
        if aug is None:
            db.query_set_status(run_id=run_id, status_id=cs.STATUS_DICT['Generating data'])

        # Check for objects created by train_tabular_model.py
        run_dir = os.path.join(cs.RUN_FOLDER, username, title)
        assert os.path.exists(os.path.join(run_dir, 'CGAN.pkl')), \
            "CGAN object not found"
        if aug:
            gen_dict_path = os.path.join(run_dir, cs.GEN_DICT_NAME + ' Additional Data ' + str(aug) + '.pkl')
        else:
            gen_dict_path = os.path.join(run_dir, cs.GEN_DICT_NAME + '.pkl')

        assert os.path.exists(gen_dict_path), "gen_dict object not found"

        # Load in CGAN and gen_dict
        CGAN = cu.get_CGAN(username=username, title=title)

        with open(gen_dict_path, 'rb') as f:
            gen_dict = pkl.load(f)

        if aug is None:
            logger.info('Successfully loaded in CGAN. Generating data...')

        # Generate data
        df = pd.DataFrame(columns=CGAN.data_gen.dataset.df_cols)
        for i, (dep_class, size) in enumerate(gen_dict.items()):
            if size > 0:
                stratify = np.eye(CGAN.nc)[i]
                tmp_df = CGAN.gen_data(size=size, stratify=stratify)
                tmp_df = tmp_df[df.columns.to_list()]
                df = pd.concat((df, tmp_df), axis=0)

        if aug is None:
            logger.info('Successfully generated data. Saving output to file...')

        # Output data
        if aug is not None:
            cu.export_tabular_to_zip(df=df, username=username, run_title=title, zip_title=title + ' Additional Data ' + str(aug))
        else:
            cu.export_tabular_to_zip(df=df, username=username, run_title=title, zip_title=title)

        if aug is None:
            db.query_set_status(run_id=run_id, status_id=cs.STATUS_DICT['Complete'])
            logger.info('Successfully completed generate_tabular_data function. Run complete.')

    except Exception as e:
        if aug is None:
            db.query_set_status(run_id=run_id, status_id=cs.STATUS_DICT['Error'])
            logger.exception('Error: %s', e)
        raise Exception("Intentionally failing process after broadly catching an exception. "
                        "Logs describing this error can be found in the run's specific logs file.")
