from unittest import TestCase
from mediamathclient.lineitem import LineItem
import os
import json
import config

class TestMediaMathLineItem(TestCase):

  def test_get_lineitem_by_id(self):
    line_item = LineItem(config.api_key, config.username, config.password)
    li = line_item.get_lineitem_by_id(1197492)
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  def test_get_lineitems_by_campaign(self):
    line_item = LineItem(config.api_key, config.username, config.password)
    li = line_item.get_lineitems_by_campaign(243821)
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  # def test_assign_sitelist_to_strategy(self):
  #   line_item = lineitem.LineItem()
  #   li = line_item.assign_sitelist_to_strategy(1197492, [117705, 117706])
  #   li = json.loads(li)
  #   self.assertIn(li['msg_type'], 'success')

  # def test_remove_sitelist_from_strategy(self):
  #   line_item = lineitem.LineItem()
  #   li = line_item.remove_sitelist_from_strategy(1197492, [117705, 117706])
  #   li = json.loads(li)
  #   self.assertIn(li['msg_type'], 'success')

  # def test_update_strategy_domain_restrictions(self):
  #   line_item = lineitem.LineItem()
  #   li = line_item.update_strategy_domain_restrictions(1197492, ['youtube.com'])
  #   li = json.loads(li)
  #   self.assertIn(li['msg_type'], 'success')

  # def test_set_deal_targeting_for_strategy(self):
  #   line_item = lineitem.LineItem()
  #   li = line_item.set_deal_targeting_for_strategy(1197492, [63505,79600])
  #   li = json.loads(li)
  #   self.assertIn(li['msg_type'], 'success')

  # def test_set_strategy_exchanges(self):
  #   line_item = lineitem.LineItem()
  #   li = line_item.set_strategy_exchanges(1197492, [159])
  #   li = json.loads(li)
  #   self.assertIn(li['msg_type'], 'success')

  def test_get_deals(self):
    line_item = LineItem(config.api_key, config.username, config.password, dsp_seat_id=101529)
    li = line_item.get_deals()
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  # def test_get_deals_by_advertiser(self):
  #   line_item = LineItem(config.api_key, config.username, config.password)
  #   li = line_item.get_deals_by_advertiser(100429)
  #   li = json.loads(li)
  #   self.assertIn(li['msg_type'], 'success')
