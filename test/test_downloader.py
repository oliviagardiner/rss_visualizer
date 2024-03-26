#!/usr/bin/python3

from src.downloader import Downloader
import unittest

class DownloaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.downloader = Downloader()

    def test_get_data_throws_exception_if_response_is_not_200(self) -> None:
        with self.assertRaises(Exception):
            url = 'http://httpstat.us/201'
            self.downloader.get_data(url)
            
    def test_get_data_returns_string_if_response_is_200(self) -> None:
        url = 'http://httpstat.us/200'
        result = self.downloader.get_data(url)
        self.assertIn('200', str(result))

if __name__ == '__main__':
    unittest.main()
