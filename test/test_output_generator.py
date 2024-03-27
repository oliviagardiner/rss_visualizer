#!/usr/bin/python3

import os
from src.output_generator import OutputGenerator
import unittest
from dotenv import load_dotenv

class CsvParserTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ['TEMPLATE'] = 'Title: %%title%%\r\nPublished: %%pubDate%%\r\nDescription: %%description%%'
        os.environ['TEMPLATE_FIELDS'] = 'title,pubDate,description'
        os.environ['OUTPUT_INCLUDE_DAY'] = 'true'
        self.output_generator = OutputGenerator('rss_config_sample.json')

    def test_get_data_file_path(self) -> None:
        self.assertIn('/data/data.csv', self.output_generator.get_data_file_path())

    def test_parse_links(self) -> None:
        links = {
            'google': 'https://google.com',
            'bing': 'https://bing.com'
        }

        self.assertEqual('[Google](https://google.com) [Bing](https://bing.com)',
                         self.output_generator.parse_links(links))

    def test_parse_row_to_template(self) -> None:
        parsed = self.output_generator.parse_row_to_template(['My Fancy Title', '2023-09-07', 'Lorem ipsum dolor sit amet'])

        self.assertEqual(
            'Title: My Fancy Title\r\nPublished: 2023-09-07\r\nDescription: Lorem ipsum dolor sit amet', parsed)
