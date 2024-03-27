#!/usr/bin/python3

import os
from src.wordcloud_generator import WordcloudGenerator
import unittest

class WordcloudGeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ['GEN_DIR'] = '../test/'
        os.environ['CSV_SUBDIR'] = 'fixture'
        os.environ['OUTPUT_INCLUDE_DAY'] = 'false'
        self.wordcloud_generator = WordcloudGenerator('rss_config_sample.json')

    def test_get_text_from_source_retrieves_text_from_specified_field(self) -> None:
        txt = self.wordcloud_generator.get_text_from_source('texttwo', 'description')
        self.assertEqual('Lorem ipsum dolor sit amet?', txt)

    def test_get_text_from_source_removes_duplications_by_default(self) -> None:
        txt = self.wordcloud_generator.get_text_from_source('keytext', 'description')
        self.assertEqual('Lorem ipsum dolor sit amet.', txt)

    def test_get_text_from_source_can_allow_duplications(self) -> None:
        txt = self.wordcloud_generator.get_text_from_source('keytext', 'description', True)
        self.assertEqual('Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet.', txt)