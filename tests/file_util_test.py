#!/usr/bin/python3

from src.file_util import FileUtil
import unittest
import sys

sys.path.append('..')

class DownloaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.file_util = FileUtil()

    def test_get_path_string(self) -> None:
        self.assertIn('../generated/test', self.file_util.get_gen_path('test'))