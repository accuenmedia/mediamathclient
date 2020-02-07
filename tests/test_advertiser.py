from unittest import TestCase
from mediamathclient.advertiser import Advertiser
import os
import json
import config

class TestMediaMathLineItem(TestCase):
    def test_get_advertisers_by_organization(self):
        advertisers = Advertiser(config.api_key, config.username, config.password)

        advertiser_response = advertisers.get_all(101529)
        advertiser_json = json.loads(advertiser_response)

        self.assertEqual(advertiser_json["response_code"], 200)

        # as of 2/6/20, AT&T has 15 advertisers
        self.assertEqual(len(advertiser_json["data"]), 15)

        # check the data, "name": "Activision", "id": 170866 should not be included
        for advertiser in advertiser_json["data"]:
            self.assertNotIn(170866, advertiser.values())

        print(advertiser_json)
