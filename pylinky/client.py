import base64
import datetime
import json
import requests
import re
import sys
if ((3, 0) <= sys.version_info <= (3, 9)):
    import urllib.parse as urlparse
elif ((2, 0) <= sys.version_info <= (2, 9)):
    import urlparse 

from .exceptions import (PyLinkyAccessException, PyLinkyEnedisException,
                         PyLinkyException, PyLinkyMaintenanceException,
                         PyLinkyWrongLoginException)

AUTHORIZE_URL_SANDBOX           = "https://gw.hml.api.enedis.fr/dataconnect/v1/oauth2/authorize"
ENDPOINT_TOKEN_URL_SANDBOX      = "https://gw.hml.api.enedis.fr/v1/oauth2/token"
METERING_DATA_BASE_URL_SANDBOX  = "https://gw.hml.api.enedis.fr"

AUTHORIZE_URL_PROD              = "https://gw.prd.api.enedis.fr/dataconnect/v1/oauth2/authorize"
ENDPOINT_TOKEN_URL_PROD         = "https://gw.prd.api.enedis.fr/v1/oauth2/token"
METERING_DATA_BASE_URL_PROD     = "https://gw.prd.api.enedis.fr"

SCOPE = {
"ADDRESSES": "/v3/customers/usage_points/addresses",
"CONSUMPTION_LOAD_CURVE": "/v4/metering_data/consumption_load_curve", 
"CONTRACTS": "/v3/customers/usage_points/contracts",
"CONTACT_DATA": "/v3/customers/contact_data", 
"DAILY_CONSUMPTION": "/v4/metering_data/daily_consumption", 
"DAILY_CONSUMPTION_MAX_POWER": "/v4/metering_data/daily_consumption_max_power", 
"IDENTITY": "/v3/customers/identity"
}

class LinkyClient(object):
    
    def __init__(self,  id, secret, redirect_url, authorize_duration="P4M", state = "LREO45H1"):
        """Initialize the client object."""
        self.id = id
        self.secret = secret
        self.redirect_url = redirect_url
        self.authorize_duration = authorize_duration
        self.state = state
        self.callback_authorize_code = None
        self.callback_usage_point_id = None
        self.callback_state = None
        self.token = None
        self._data = {}

    def _pretty_print_request(self,req):
        print('{}\n{}\n{}\n{}\n{}\n'.format(
            '-----------REQ START-----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
            '-----------REQ STOP-----------',))

    def login(self):
        req_params = {
             'client_id': self.id,
             'response_type': 'code',
             #'redirect_uri': self.redirect_url,
             'state': self.state,
             'duration': self.authorize_duration
            }

        try:
            http_request = requests.Request("GET", AUTHORIZE_URL_SANDBOX, params=req_params)
            http_request_prepared = http_request.prepare()
            http_session = requests.Session()
            http_return = http_session.send(http_request_prepared)

            callback_found = re.findall(r'var url = \".*\"', http_return.text)
            callback_url = callback_found[0].split('\"')[1]
            callback_url_parsed = urlparse.urlparse(callback_url)
            self.callback_authorize_code = urlparse.parse_qs(callback_url_parsed.query, True)['code'][0]
            self.callback_state = urlparse.parse_qs(callback_url_parsed.query, True)['state'][0]
            self.callback_usage_point_id = urlparse.parse_qs(callback_url_parsed.query, True)['usage_point_id'][0]
            #print ("callback auth_code = ", self.callback_authorize_code)
            #print ("callback state = ", self.callback_state)
            #print ("callback usage_point_id = ", self.callback_usage_point_id)

        except OSError:
            raise PyLinkyAccessException("Can not obtain Enedis code")
        
        self.token = self._get_token()
        return True

    def _get_token(self):
        """Get Token."""
        
        req_head = {
           'Content-Type': 'application/x-www-form-urlencoded',
           'Accept': 'text/html'
           }
        req_params = {
                    'redirect_uri': self.redirect_url,
                    }
        req_data = {
                'grant_type': 'authorization_code',
                'client_id': self.id,
                'client_secret': self.secret,
                'code': self.callback_authorize_code
                }

        try:
            # Forge and print request
            http_request = requests.Request("POST", ENDPOINT_TOKEN_URL_SANDBOX, headers=req_head, params=req_params, data=req_data)
            http_request_prepared = http_request.prepare()
            #self._pretty_print_request(http_request_prepared)

            # Send request
            http_session = requests.Session()
            http_return = http_session.send(http_request_prepared)

            # Print request result
            #print(http_return.status_code)
            #print(http_return.text)
            #print(http_return.json)

            # Parse request result
            endpoint_token_returned_json = json.loads(http_return.text)

        except OSError:
            raise PyLinkyAccessException("Can not obtain token")
        return endpoint_token_returned_json

    def get_data(self, scope = None, start_date=None, end_date=None):
        """Get data."""

        metering_data_api_path = SCOPE[scope]
        request_url = METERING_DATA_BASE_URL_SANDBOX + metering_data_api_path
        token_type = self.token['token_type']
        token = self.token['access_token']

        req_head = {
                'Accept': 'application/json',
                'Authorization': token_type + ' ' + token
                }

        req_params = {
                'start': start_date,
                'end': end_date,
                'usage_point_id':self.callback_usage_point_id
                }

        try:
            http_request = requests.Request("GET", request_url, headers=req_head, params=req_params)
            http_request_prepared = http_request.prepare()
            http_session = requests.Session()
            http_return = http_session.send(http_request_prepared)
            #print(http_return.status_code)
            #print(http_return.text)
        except OSError as e:
            raise PyLinkyAccessException("Could not access enedis.fr: " + str(e))

        return json.loads(http_return.text)
