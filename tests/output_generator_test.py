#!/usr/bin/python3

from src.output_generator import OutputGenerator
import unittest
import sys
from dotenv import load_dotenv

sys.path.append('..')

class CsvParserTest(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv('.env.test')
        self.output_generator = OutputGenerator('rss_config_sample.json', '2023-09-04')

    def test_get_data_file_path(self) -> None:
        self.assertIn('/data/2023-09-04-data.csv', self.output_generator.get_data_file_path())

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
