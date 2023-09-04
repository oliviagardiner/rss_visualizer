#!/usr/bin/python3

from src.config_parser import ConfigParser
import unittest
import sys

sys.path.append('..')

class ConfigParserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config_parser = ConfigParser('rss_config_sample.json')

    def test_get_values_by_key(self) -> None:
        result = self.config_parser.get_values_by_key('url')
        self.assertEqual({'UID': 'https://sample.com/feed'}, result)

    def test_get_values_by_key_empty_result_on_invalid_key(self) -> None:
        result = self.config_parser.get_values_by_key('notexist')
        self.assertEqual({'UID': ''}, result)

    def test_get_settings_for_feed_key(self) -> None:
        result = self.config_parser.get_settings_for_feed_key('UID')
        self.assertEqual({'url': 'https://sample.com/feed', 'name': 'NAME', 'date_slice': 4}, result)
        
    def test_get_settings_for_feed_key_empty_resul_on_invalid_key(self) -> None:
        result = self.config_parser.get_settings_for_feed_key('notexist')
        self.assertEqual(None, result)
