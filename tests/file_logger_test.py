#!/usr/bin/python3

import unittest
import sys

sys.path.append('..')
from src.file_logger import FileLogger

class FileLoggerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.file_logger = FileLogger()

    def test_log_without_level_logs_info(self) -> None:
        teststr = 'Message'
        self.file_logger.log(teststr)
        self.file_logger.stream.seek(0)
        content = self.file_logger.stream.read()
        self.assertIn(self.file_logger.LEVEL_INFO.upper(), content)
        self.assertIn(teststr, content)

    def test_log_with_level_logs_correct_level(self) -> None:
        teststr = 'Message'
        self.file_logger.log(teststr, self.file_logger.LEVEL_ERROR)
        self.file_logger.stream.seek(0)
        content = self.file_logger.stream.read()
        self.assertIn(self.file_logger.LEVEL_ERROR.upper(), content)
        self.assertIn(teststr, content)

    def test_log_non_string_throws_exception(self) -> None:
        self.assertRaises(Exception, self.file_logger.log(2))

if __name__ == '__main__':
    unittest.main()
