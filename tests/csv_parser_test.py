#!/usr/bin/python3

from src.csv_parser import CsvParser
import unittest
import sys
from dotenv import load_dotenv

sys.path.append('..')

class CsvParserTest(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv('.env.test')
        self.csv_parser = CsvParser('rss_config_sample.json', ['key', 'guid',
                                    'pubDate', 'title', 'description'], 'key')

    def test_create_row_from_key(self) -> None:
        row = self.csv_parser.create_row_from_key('test')
        self.assertEqual({'key': 'test', 'guid': None, 'pubDate': None, 'title': None, 'description': None}, row)

    def test_clean_simple_html_from_text(self) -> None:
        cleaned = self.csv_parser.clean_html_from_text('<body>Test</body>')
        self.assertEqual('Test', cleaned)

    def test_clean_nested_html_from_text(self) -> None:
        cleaned = self.csv_parser.clean_html_from_text('<body><div>Test</div></body>')
        self.assertEqual('Test', cleaned)

    def test_parse_rss_string_to_date(self) -> None:
        parsed = self.csv_parser.parse_rss_string_to_date(
            'Thu, 31 Aug 2023 07:14:43 GMT', 'UID')
        self.assertEqual('31 Aug 2023 07:14:43', parsed)

    def test_fill_empty_guid_with_unique_value(self) -> None:
        testrow = {'guid': '', 'foo': 'bar'}
        self.assertEqual({'guid': 'bar', 'foo': 'bar'}, self.csv_parser.fill_empty_guid_with_unique_value(testrow))
