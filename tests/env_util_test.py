#!/usr/bin/python3

from src.env_util import EnvUtil
import unittest
import sys
from dotenv import load_dotenv

sys.path.append('..')

class EnvUtilTest(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv('.env.test')

    def test_parse_config_to_list(self) -> None:
        result = EnvUtil.parse_config_to_list('PARSE_FIELDS')
        self.assertEqual(['key', 'guid', 'pubDate', 'title', 'description'], result)

    def test_parse_config_to_list_with_custom_separator(self) -> None:
        result = EnvUtil.parse_config_to_list('TEST_FIELDS', ';')
        self.assertEqual(['one', 'two', 'three'], result)
