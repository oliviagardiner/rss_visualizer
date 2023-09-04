#!/usr/bin/python3

from src.wordcloud_generator import WordcloudGenerator
import unittest
import sys

sys.path.append('..')

class WordcloudGeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wordcloud_generator = WordcloudGenerator()
