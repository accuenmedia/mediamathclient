import json
import requests
import os
import terminalone
import datetime

from mediamathclient.base import Base


class Campaign(Base):

    def get_campaign_by_id(self, campaign_id):
        campaign_id = int(campaign_id)
        url = self.generate_url("campaigns") + "/" + str(campaign_id)
        return self.call_mm_api('GET', url)

    def get_campaigns_by_advertiser(self, advertiser_id):
        advertiser_id = int(advertiser_id)
        url = self.generate_url("campaigns") + "/limit/advertiser={0}".format(advertiser_id)
        return self.call_mm_api('GET', url)

    def create_campaign(self, payload):
        url = self.generate_url("campaigns")
        return self.call_mm_api('POST', url, payload)

    # updates existing campaigns
    def update_campaign(self, payload, campaign_id):
        campaign_id = int(campaign_id)
        url = self.generate_url("campaigns") + "/" + str(campaign_id)
        return self.call_mm_api('POST', url, payload)

    def get_budget_flights(self, campaign_id):
        campaign_id = int(campaign_id)
        url = self.generate_url("campaigns") + "/" + str(campaign_id) + "/budget_flights?full=*"
        return self.call_mm_api('GET', url)
