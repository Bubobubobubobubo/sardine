import unittest
from sardine.sequences.LexerParser.ListParser import ListParser


class TestPatternParsing(unittest.TestCase):

    def test_number_pattern(self):
        """
        Test parsing several patterns composed of numbers and simple math operations.
        """
        parser = ListParser(None, None, None)
        patterns = [
            ".5",
            "1, 2, 3",
            "1+1, 2*3, 4-1, 5/2"
        ]
        expected = [
            [.5],
            [1, 2, 3],
            [2, 6, 3, 2.5]
        ]
        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                result = parser.parse(pattern)
                self.assertEqual(len(result), len(expected[i]))
                for x, y in zip(result, expected[i]):
                    # we use assertAlmostEqual instead of assertEqual here
                    # because we are dealing with floats
                    self.assertAlmostEqual(x, y)
