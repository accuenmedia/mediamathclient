import json
import requests
import os
import terminalone
import itertools

from mediamathclient.base import Base


class LineItem(Base):

    page_limit = 100

    def get_lineitem_by_id(self, lineitem_id):
        url = self.generate_url('strategies') + "/" + str(lineitem_id)
        return self.call_mm_api('GET', url)

    def get_lineitems_by_campaign(self, campaign_id):
        campaign_id = int(campaign_id)
        url = self.generate_url('strategies') + "/limit/campaign={0}/?full=*".format(str(campaign_id))
        return self.call_mm_api('GET', url)

    def create_lineitem(self, payload):
        url = self.generate_url('strategies')
        return self.call_mm_api('POST', url, payload)

    # updates existing line items
    def update_lineitem(self, payload, lineitem_id):
        url = self.generate_url('strategies') + "/" + str(lineitem_id)
        return self.call_mm_api('POST', url, payload)

    def assign_sitelist_to_strategy(self, lineitem_id, sitelist_ids):
        url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/site_lists"
        payload = {}
        for idx, sitelist_id in enumerate(sitelist_ids):
            index = 'site_lists.{0}.id'.format(str(idx + 1))
            assigned = 'site_lists.{0}.assigned'.format(str(idx + 1))
            payload[index] = sitelist_id
            payload[assigned] = int(True)

        return self.call_mm_api('POST', url, payload)

    def remove_sitelist_from_strategy(self, lineitem_id, sitelist_ids):
        url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/site_lists"
        payload = {}

        for idx, sitelist_id in enumerate(sitelist_ids):
            index = 'site_lists.{0}.id'.format(str(idx + 1))
            assigned = 'site_lists.{0}.assigned'.format(str(idx + 1))
            payload[index] = sitelist_id
            payload[assigned] = int(False)

        return self.call_mm_api('POST', url, payload)

    def update_strategy_domain_restrictions(self, lineitem_id, domains):
        url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/domain_restrictions"
        payload = {}

        for idx, domain in enumerate(domains):
            index_domain = 'domains.{0}.domain'.format(str(idx + 1))
            index_restriction = 'domains.{0}.restriction'.format(str(idx + 1))
            payload[index_domain] = domain
            payload[index_restriction] = "INCLUDE"

        return self.call_mm_api('POST', url, payload)

    def set_deal_targeting_for_strategy(self, lineitem_id, deal_ids):
        url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/deals"
        payload = {}

        for idx, deal in enumerate(deal_ids):
            index = 'deal.{0}.id'.format(str(idx + 1))
            payload[index] = str(deal)

        payload["all_pmp"] = 0
        payload["all_exchanges"] = 0

        return self.call_mm_api('POST', url, payload)

    def set_strategy_exchanges(self, lineitem_id, exchange_ids):
        lineitem_id = int(lineitem_id)
        url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/supplies"
        payload = {}

        for idx, exchange_id in enumerate(exchange_ids):
            index = 'supply_source.{0}.id'.format(str(idx + 1))
            payload[index] = str(exchange_id)

        payload["all_pmp"] = 0
        payload["all_exchanges"] = 0

        return self.call_mm_api('POST', url, payload)

    # TODO: this should be its own class
    def get_deals(self):

        # make an initial request to pull all deals so we get the initial page/total_count info
        url = self.generate_url('deals') + "/?owner.organization_id={0}&full=*".format(self.organization_id)
        initial_response = requests.get(url, headers=self.headers)
        request_body = self.generate_curl_command('GET', url, self.headers)

        if 'errors' in initial_response.json():
            response_json = self.generate_json_response(initial_response.json(), initial_response, request_body)
            return json.dumps(response_json)
        else:
            # iterate through each page with the page_offset being a multiple of 100 since page_limit is 100
            # calculate last page
            end = int(round(int(initial_response.json()['meta']['total_count']) / self.page_limit))
            page_data = []
            url = self.generate_url('deals') + "/?owner.organization_id={0}&page_offset=0".format(self.organization_id)
            response = requests.get(url, headers=self.headers)
            page_data.append(response.json()['data'])
            for i in range(0, end):
                # offset is multiple of 100
                offset = (i + 1) * self.page_limit
                # use offset to get every page
                url = self.generate_url('deals') + "/?owner.organization_id={0}&page_offset={1}".format(self.organization_id, offset)
                response = requests.get(url, headers=self.headers)
                page_data.append(response.json()['data'])
                print("on loop number {0}".format(i))
            page_data = list(itertools.chain.from_iterable(page_data))

            json_dict = {
                'data': page_data
            }

            response_json = self.generate_json_response(json_dict, initial_response, request_body)
            return json.dumps(response_json)

    def get_deals_by_advertiser(self, advertiser_id):

        # make an initial request to pull all deals with advertiser_id perms so we get the initial page/total_count info
        url = self.generate_url('deals') + "/?permissions.advertiser_id={0}".format(advertiser_id)
        initial_response = requests.get(url, headers=self.headers)
        request_body = self.generate_curl_command('GET', url, self.headers)

        if 'errors' in initial_response.json():
            response_json = self.generate_json_response(initial_response.json(), initial_response, request_body)
            return json.dumps(response_json)
        else:
            end = int(round(int(initial_response.json()['meta']['total_count']) / self.page_limit)) + self.page_limit
            page_data = []
            url = self.generate_url('deals') + "/?permissions.advertiser_id={0}&page_offset=0".format(advertiser_id)
            response = requests.get(url, headers=self.headers)
            page_data.append(response.json()['data'])
            for i in range(0, end):
                # offset is multiple of 100
                offset = (i + 1) * self.page_limit
                # use offset to get every page
                url = self.generate_url('deals') + "/?permissions.advertiser_id={0}&page_offset={1}".format(advertiser_id, offset)
                response = requests.get(url, headers=self.headers)
                page_data.append(response.json()['data'])
            page_data = list(itertools.chain.from_iterable(page_data))

            json_dict = {
                'data': page_data
            }

            response_json = self.generate_json_response(json_dict, initial_response, request_body)
            return json.dumps(response_json)
