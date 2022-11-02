import unittest
from sardine.sequences.LexerParser.ListParser import ListParser


class TestPatternParsing(unittest.TestCase):

    def test_number_pattern(self):
        parser = ListParser(None, None, None)
        pattern = "1, 2, 3"
        result = parser.parse(pattern)
        expected = [1, 2, 3]
        self.assertEqual(len(result), len(expected))
        self.assertTrue(all([x == y for x, y in zip(result, expected)]))
