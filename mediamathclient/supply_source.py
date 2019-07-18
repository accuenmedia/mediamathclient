import json
import requests
import itertools

from mediamathclient.base import Base

class SupplySource(Base):

    def __init__(self, api_key, username, password, data=None):
        super().__init__(api_key, username, password, data)

    def get_supply_sources(self):
        url = self.generate_url("supply_sources")
        initial_response = requests.get(url, headers=self.headers)
        request_body = url, self.headers
        # calculate last page
        end = int(round(int(initial_response.json()['meta']['total_count']) / self.page_limit))
        page_data = []
        for i in range(-1, end):
            # offset is multiple of 100
            offset = (i + 1) * self.page_limit
            # use offset to get every page
            url = self.generate_url('supply_sources') + "/?page_offset={0}".format(offset)
            response = requests.get(url, headers=self.headers)
            page_data.append(response.json()['data'])
        page_data = list(itertools.chain.from_iterable(page_data))

        json_dict = {
            'data': page_data
        }

        response_json = self.generate_json_response(json_dict, initial_response, request_body)
        return json.dumps(response_json)

    def make_call(self, url, method_type, payload=None):

        if method_type == 'GET':
            response = requests.get(url, headers=self.headers, data=payload)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)

        if method_type == 'POST':
            response = requests.post(url, headers=self.headers, data=payload)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)
