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

    def test_notes(self):
        """
        Test parsing a random number generator
        """
        parser = ListParser(None, None, None)
        patterns = [
                "C,D,E,F,G,A,B",
                "Do,Re,Mi,Fa,Sol,La,Si",
                "Do,Ré,Mi,Fa,Sol,La,Si",
                "C0,C1,C2,C3,C4,C5,C6,C7,C8,C9",
        ]
        expected = [
            [60, 62, 64, 65, 67, 69, 71],
            [60, 62, 64, 65, 67, 69, 71],
            [60, 62, 64, 65, 67, 69, 71],
            [12, 24, 36, 48, 60, 72, 84, 96, 108, 120],
        ]
        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                result = parser.parse(pattern)
                self.assertEqual(len(result), len(expected[i]))
                for x, y in zip(result, expected[i]):
                    # we use assertAlmostEqual instead of assertEqual here
                    # because we are dealing with floats
                    self.assertEqual(x, y)

if __name__ == '__main__':
    unittest.main()
