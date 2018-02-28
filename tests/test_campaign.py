from unittest import TestCase
from mediamathclient.mediamathclient import campaign
import os
import json

class TestMediaMathCampaign(TestCase):

  def test_connection(self):
    c = campaign.Campaign()
    session_id = c.get_connection()
    self.assertIsNotNone(session_id)

  def test_get_campaigns_by_advertiser(self):
    c = campaign.Campaign()
    campaigns = c.get_campaigns_by_advertiser(100429)
    self.assertIn('"msg_type": "success"', campaigns)
