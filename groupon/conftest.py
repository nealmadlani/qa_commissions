import pytest
import mugic
import groupon_api
import datetime


# defines the command line args, namely the to and from dates, which both default to today
def pytest_addoption(parser):
    d_today = datetime.date.today().strftime("%Y-%m-%d")
    parser.addoption('--from', action='store', default=d_today, help='From date')
    parser.addoption('--to', action='store', default=d_today, help='To date')


# this will establish a connection to the database
@pytest.fixture(scope='session')
def db(request):
    d = mugic.connect()

    def teardown():
        d.dispose()

    request.addfinalizer(teardown)
    return d


# this will query the groupon api for the date range we are interested in
@pytest.fixture(scope='session')
def api_groupon(request):
    return groupon_api.fetch('groupon', request.config.getoption("--from"), request.config.getoption("--to"))


# this will query the groupon api for the date range we are interested in
@pytest.fixture(scope='session')
def api_grouponvp(request):
    return groupon_api.fetch('grouponvp', request.config.getoption("--from"), request.config.getoption("--to"))


# this fixture will query mugic comms for the grouon data for the specified date range
@pytest.fixture(scope='session')
def rows_groupon(db, request):
    return mugic.get_mugic_comms_data(db, '122569', request.config.getoption("--from"), request.config.getoption("--to"))


# this fixture will query mugic comms for the grouon data for the specified date range
@pytest.fixture(scope='session')
def rows_grouponvp(db, request):
    return mugic.get_mugic_comms_data(db, '373267', request.config.getoption("--from"), request.config.getoption("--to"))
