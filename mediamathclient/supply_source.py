import json
import requests
import itertools

from mediamathclient.base import Base

class SupplySource(Base):

    page_limit = 100

    def get_supply_sources(self):
        url = self.generate_url("supply_sources")
        initial_response = requests.get(url, headers=self.headers)
        request_body = url, self.headers
        # calculate last page
        end = int(round(int(initial_response.json()['meta']['total_count']) / self.page_limit))
        page_data = []
        for i in range(0, end + 1):
            # offset is multiple of 100
            offset = i * self.page_limit
            # use offset to get every page
            url = self.generate_url('supply_sources') + "/?page_offset={0}".format(offset)
            response = requests.get(url, headers=self.headers)
            page_data.append(response.json()['data'])
        page_data = list(itertools.chain.from_iterable(page_data))

        json_dict = {
            'data': page_data
        }

        curl_command = self.generate_curl_command('GET', url, self.headers)
        response_json = self.generate_json_response(json_dict, initial_response, curl_command)

        return json.dumps(response_json)
