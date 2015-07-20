import requests
import datetime
import json

# end point and client ids
groupon_api = 'https://partner-api.groupon.com/reporting/v2/order.json'
groupon_client = 'a607f14acb18ba3f1f224310055d085f70a2ad94'
grouponvp_client = 'ebdb3ee26916ca72cafea8562963cc63bdeb16bc'


# hits the api using the client and date range passed in the run-time args
def fetch(client, date_from='today', date_to='today'):
    client_id = get_client_id(client)
    d_today = datetime.date.today().strftime("%Y-%m-%d")
    date_from = d_today if date_from == 'today' else date_from
    date_to = d_today if date_to == 'today' else date_to
    url = '%s?clientId=%s&date=[%s&date=%s]' % (groupon_api, client_id, date_from, date_to) + '&group=order%7Cdate'
    d = requests.get(url)
    return json.loads(d.content)


# returns client id for a given client
def get_client_id(client):
    r = groupon_client if client == 'groupon' else grouponvp_client
    return r


# returns merchant id for a given client
def get_groupon_merchant_id(client):
    r = '122569' if client == 'groupon' else '373267'
    return r
