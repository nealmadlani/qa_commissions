###
# script will query the gropuon api over a given date range (--to and --from args), for both 'groupon' and 'grouponvp'
# it will then query mugic_comms to check the data has been inserted correctly, will also check mugic_comms_history
###
import mugic


# test: checks the number of rows from the api for 'groupon' matches what we have in the database
def test_groupon_row_counts(db, api_groupon, rows_groupon):
    assert rows_groupon['id'].count() == len(api_groupon['records'])


# test: for each row we got from the api for 'groupon' check the data in the database is correct
def test_groupon_data_vs_api(db, api_groupon, rows_groupon):
    for api_row in api_groupon['records']:
        validate_row(db, api_row, rows_groupon, '122569')


# test: checks the number of rows from the api for 'grouponvp' matches what we have in the database
def test_grouponvp_row_counts(db, api_grouponvp, rows_grouponvp):
    assert rows_grouponvp['id'].count() == len(api_grouponvp['records'])


# test: for each row we got from the api for 'grouponvp' check the data in the database is correct
def test_grouponvp_data_vs_api(db, api_grouponvp, rows_grouponvp):
    for api_row in api_grouponvp['records']:
        validate_row(db, api_row, rows_grouponvp, '373267')


# method: looks for the specified row from the api (api_row) in the database (db_rows) and validates the data
def validate_row(db, api_row, db_rows, m_id):

    # find the row in the database
    db_row = mugic.get_row_from_mugic_comms(db_rows, api_row['group'][0]['informations']['BillingId'])

    if db_row is None:
        assert 'Row Found' == 'No DB Row Found for ' + api_row['group'][0]['informations']['BillingId'] + '!'
        return None

    # clean the date column that we get from groupon
    api_date = api_row['group'][1]['informations']['Datetime'].replace('T', ' ')[0:16]+':00'

    # the sid contains four values, seperated by an X, so we capture those in an array
    sid = api_row['group'][0]['informations']['Sid'][4:].split('X')

    # assert on the status field first, as there are some rules behind this
    if api_row['group'][0]['informations']['Status'] == 'VALID':
        if db_row['skimlinks_status'] == 1:
            assert db_row['skimlinks_status'] == 1
        elif db_row['skimlinks_status'] == 2:
            assert db_row['skimlinks_status'] == 1
        else:
            assert db_row['skimlinks_status'], '1 or 2'
    elif (api_row['group'][0]['informations']['Status'] == 'REFUNDED') or (api_row['group'][0]['informations']['Status'] == 'INVALID'):
        if(db_row['total_amount'] == 0):
            assert db_row['skimlinks_status'] == '5'
        else:
            assert db_row['skimlinks_status'] == '4'
    else:
        assert api_row['group'][0]['informations']['Status'] == 'VALID, REFUNDED or INVALID'

    # assert on the remaining data
    assert db_row['publisher_id'] == int(sid[0])
    assert db_row['network_transaction_id'] == api_row['group'][0]['informations']['BillingId']
    assert db_row['publisher_id'] == int(sid[0])
    assert db_row['domain_id'] == int(sid[1])
    assert db_row['unique_track'] == sid[2]
    assert str(db_row['transaction_date']) == api_date
    assert db_row['currency'] == api_row['group'][0]['informations']['Currency']
    assert round(db_row['order_amount'], 5) == round(api_row['measures']['SaleGrossAmount']*100, 5)
    assert round(db_row['total_amount'], 5) == round(api_row['measures']['LedgerAmount']*100, 5)
    assert db_row['items'] == api_row['measures']['NumberOfUnits']
    assert db_row['merchant_id'] == int(m_id)

    # secondary assertions to flag an odd data that we should check manually
    assert db_row['merchant_id'] != 30643
    assert db_row['publisher_id'] != 1
    assert db_row['domain_id'] != 2

    # now query mugic comms history for the same row
    mugic_history = mugic.get_mugic_comms_history_data(db, m_id, sid, db_row['network_transaction_id'])

    # can't predict how many history rows there will be, but there should be one at least
    assert mugic_history['id'].count() >= 1
