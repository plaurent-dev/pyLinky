import unittest

# Our test case class
import requests
from pylinky import LinkyClient
import json
from .support.assertions import assert_valid_schema

class LinkyClientTestCase(unittest.TestCase):
    def setUp(self):
        super(LinkyClientTestCase, self).setUp()
        self.id = "your_id"
        self.secret = "your_sms"
        self.redirect_uri = "your_site"


    def test_LinkyClient(self):
        client = LinkyClient(self.id, self.secret, self.redirect_uri)
        assert client.id == self.id
        assert client.secret == self.secret
        assert client.redirect_url == self.redirect_uri

    def test_LinkyClient_Identity(self):
        client = LinkyClient(self.id, self.secret, self.redirect_uri)
        client.login()
        response = client.get_data(scope='IDENTITY')
        assert_valid_schema(response[0], 'identity.json')

    def test_LinkyClient_Addresses(self):
        client = LinkyClient(self.id, self.secret, self.redirect_uri)
        client.login()
        response = client.get_data(scope='ADDRESSES')
        assert_valid_schema(response[0], 'addresses.json')
     
    def test_LinkyClient_Contracts(self):
        client = LinkyClient(self.id, self.secret, self.redirect_uri)
        client.login()
        response = client.get_data(scope='CONTRACTS')
        assert_valid_schema(response[0], 'contracts.json')

    def test_LinkyClient_ContactData(self):
        client = LinkyClient(self.id, self.secret, self.redirect_uri)
        client.login()
        response = client.get_data(scope='CONTACT_DATA')
        assert_valid_schema(response[0], 'contact.json')

    def test_LinkyClient_Consumption(self):
        client = LinkyClient(self.id, self.secret, self.redirect_uri)
        client.login()
        response = client.get_data(scope='CONSUMPTION_LOAD_CURVE',start_date='2020-04-08',end_date='2020-04-09')
        assert_valid_schema(response, 'consumption.json')

    def test_LinkyClient_DailyConsumption(self):
        client = LinkyClient(self.id, self.secret, self.redirect_uri)
        client.login()
        response = client.get_data(scope='DAILY_CONSUMPTION',start_date='2020-04-08',end_date='2020-04-09')
        assert_valid_schema(response, 'consumption.json')
    
    def test_LinkyClient_DailyConsumptionMaxPower(self):
        client = LinkyClient(self.id, self.secret, self.redirect_uri)
        client.login()
        response = client.get_data(scope='DAILY_CONSUMPTION_MAX_POWER',start_date='2020-04-08',end_date='2020-04-09')
        assert_valid_schema(response, 'consumption.json')
if __name__ == "__main__":
    unittest.main()