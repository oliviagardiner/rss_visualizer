#!/usr/bin/python3

import os
from src.env_util import EnvUtil
import unittest

class EnvUtilTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ['PARSE_FIELDS'] = 'key,guid,pubDate,title,description'
        os.environ['TEST_FIELDS'] = 'one|two|three'

    def test_parse_config_to_list(self) -> None:
        result = EnvUtil.parse_config_to_list('PARSE_FIELDS')
        self.assertEqual(['key', 'guid', 'pubDate', 'title', 'description'], result)

    def test_parse_config_to_list_with_custom_separator(self) -> None:
        result = EnvUtil.parse_config_to_list('TEST_FIELDS', '|')
        self.assertEqual(['one', 'two', 'three'], result)
