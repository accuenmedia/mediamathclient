import json
import requests
import os
import terminalone
import datetime



class Campaign:

    def __init__(self, api_key, username, password, data=None, omg_campaign=None):
        self.api_key = api_key
        self.username = username
        self.password = password
        self.data = data
        self.omg_campaign = omg_campaign

        self.t1 = get_connection()
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded', 
            'Accept': 'application/vnd.mediamath.v1+json',
            'Cookie': 'adama_session=' + str(self.t1.session_id)
        }

        self.base_url = "https://" + t1.api_base + "/"
        self.service_url = self.t1._get_service_path('campaigns') + "/"
        self.constructed_url = self.t1._construct_url("campaigns", entity=None, child=None, limit=None)[0]
        self.url = self.base_url + self.service_url + self.constructed_url

    def get_connection(self):
        creds = {
            "username": self.username,
            "password": self.password,
            "api_key": self.api_key
        }
        return terminalone.T1(auth_method="cookie", **creds)

    def generate_json_response(self, json_dict, response, request_body):
        response_json = {
            "response_code": response.status_code,
            "request_body": request_body
        }

        # error checking
        if 'errors' in json_dict:
            response_json['msg_type'] = 'error'
            response_json['msg'] = json_dict['errors']
            response_json['data'] = json_dict['errors']

        else:
            response_json['data'] = json_dict['data']
            response_json['msg_type'] = 'success'
            response_json['msg'] = ''

        return response_json

    def generate_url(self):
        base_url = "https://" + self.t1.api_base + "/"
        service_url = self.t1._get_service_path('campaigns') + "/"
        constructed_url = self.t1._construct_url("campaigns", entity=None, child=None, limit=None)[0]
        url = base_url + service_url + constructed_url
        return url

    def get_campaign_by_id(self, campaign_id):
        campaign_id = int(campaign_id)
        url = self.generate_url() + "/" + str(campaign_id)
        return self.call_mm_api('GET', url)

    def get_campaigns_by_advertiser(self, advertiser_id):
        advertiser_id = int(advertiser_id)
        url = self.generate_url() + "/limit/advertiser={0}".format(advertiser_id)
        return self.call_mm_api('GET', url)

    def create_campaign(self, payload):
        url = self.generate_url()
        return self.call_mm_api('POST', url, payload)

    # updates existing campaigns
    def update_campaign(self, payload, campaign_id):
        campaign_id = int(campaign_id)
        url = self.generate_url() + "/" + str(campaign_id)
        return self.call_mm_api('POST', url, payload)

    def get_budget_flights(self, campaign_id):
        campaign_id = int(campaign_id)
        url = self.generate_url() + "/" + str(campaign_id) + "/budget_flights?full=*"
        return self.call_mm_api('GET', url)

    def call_mm_api(self, obj_type, url, data=None):
        if obj_type == 'GET':
            response = requests.get(url, headers=self.headers)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)

        if obj_type == 'POST':
            response = requests.post(url, headers=self.headers, data=data)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)
