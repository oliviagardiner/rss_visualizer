#!/usr/bin/python3

from src.wordcloud_generator import WordcloudGenerator
import unittest

class WordcloudGeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wordcloud_generator = WordcloudGenerator()
