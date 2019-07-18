import json
import requests
import terminalone

class Base:
    def __init__(self, api_key, username, password, data=None):
        self.api_key = api_key
        self.username = username
        self.password = password
        self.data = data

        self.t1 = self.get_connection()
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded', 
            'Accept': 'application/vnd.mediamath.v1+json',
            'Cookie': 'adama_session=' + str(self.t1.session_id)
        }

    def get_connection(self):
        creds = {
            "username": self.username,
            "password": self.password,
            "api_key": self.api_key
        }

        return terminalone.T1(auth_method="cookie", **creds)

    def generate_url(self, obj):
        base_url = "https://" + self.t1.api_base + "/"
        service_url = self.t1._get_service_path(obj) + "/"
        constructed_url = self.t1._construct_url(obj, entity=None, child=None, limit=None)[0]
        
        url = base_url + service_url + constructed_url

        return url

    def call_mm_api(self, method, url, data=None):
        if method == 'GET':
            response = requests.get(url, headers=self.headers)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)

        if method == 'POST':
            response = requests.post(url, headers=self.headers, data=data)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)

    def generate_curl_command(self, url, headers):
        pass

    @staticmethod
    def generate_json_response(json_dict, response, request_body):
        response_json = {
            "response_code": response.status_code,
            "request_body": request_body
        }

        # error checking
        if 'errors' in json_dict:
            response_json['msg_type'] = 'error'
            response_json['msg'] = json_dict['errors']
            response_json['data'] = json_dict['errors']

        elif 'data' not in json_dict:
            response_json['data'] = json_dict
            response_json['msg_type'] = 'success'
            response_json['msg'] = ''

        else:
            response_json['data'] = json_dict['data']
            response_json['msg_type'] = 'success'
            response_json['msg'] = ''

        return response_json
