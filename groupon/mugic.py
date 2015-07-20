import sqlalchemy
import pandas as pd
import os


def get_mugic_comms_data(dbcon, mid, from_date, to_date):
    sql = """SELECT * FROM mugic_comms
             WHERE merchant_id=%s
             AND transaction_date >= '%s 00:00:00'
             AND transaction_date <= '%s 23:59:59'""" % (mid, from_date, to_date)
    return pd.read_sql(sql, dbcon)


def get_mugic_comms_history_data(dbcon, mid, sid, billing_id):
    sql = """SELECT * FROM mugic_comms_history
             WHERE merchant_id=%s
             AND unique_track = '%s'
             AND domain_id = %s
             AND publisher_id = %s
             AND currency = 'GBP'
             AND network_transaction_id = '%s'""" % (mid, sid[2], sid[1], sid[0], billing_id)
    return pd.read_sql(sql, dbcon)


def get_row_from_mugic_comms(rows, billing_id):
    for db_index, db_row in rows.iterrows():
        if db_row['network_transaction_id'] == billing_id:
            return db_row


def connect():
    return sqlalchemy.create_engine('mysql+mysqldb://%s:%s@galvatron.skimlinks.com:3306/mugic' % (os.environ.get('GALVATRON_USER'), os.environ.get('GALVATRON_PASS')))
