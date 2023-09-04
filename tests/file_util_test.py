#!/usr/bin/python3

from src.file_util import FileUtil
import unittest
import sys

sys.path.append('..')

class DownloaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.file_util = FileUtil()

    def test_get_abs_path_sring(self) -> None:
        self.assertIn('test', self.file_util.get_abs_path('test'))
        self.assertNotIn('generated', self.file_util.get_abs_path('test'))

    def test_get_gen_path_string(self) -> None:
        self.assertIn('test', self.file_util.get_gen_path('test'))
        self.assertIn('generated', self.file_util.get_gen_path('test'))
