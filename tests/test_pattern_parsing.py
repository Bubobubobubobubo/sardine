import unittest
from sardine.sequences.LexerParser.ListParser import ListParser
from typing import Union
from unittest import mock


PARSER = ListParser(None, None, None)

class TestPatternParsing(unittest.TestCase):

    def test_choice_operator(self):
        """
        Test the choice (|) operator 
        """
        parser = PARSER
        patterns = [
                "1|2|3|4",
                "[1,2,3,4]|[., .]",
                "baba|dada",
                "(baba:2)|(dada:4)"
        ]
        expected = [
                [[1],[2],[3],[4]],
                [[1,2,3,4], [None, None]],
                [["baba"], ["dada"]],
                [["baba:2"], ["dada:4"]]
        ]
        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                self.assertIn(parser.parse(pattern), expected[i])

    def test_presence_operator(self):
        """
        Test the presence operator (?) that can make things disappear
        50% of the time
        """
        parser = PARSER
        patterns = [
                "[1,2,3,4,5]?",
                "1?,2?,3?,4?",
        ]
        expected_true = [
                [1,2,3,4,5],
                [1,2,3,4]
        ]
        expected_false = [
                [None]*5,
                [None]*4
        ]
        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                mocked_random_choice = lambda : 1.0
                with mock.patch('random.random', mocked_random_choice):
                    result = parser.parse(pattern)
                    self.assertEqual(expected_true[i], result)
                mocked_random_choice = lambda : 0.0
                with mock.patch('random.random', mocked_random_choice):
                    result = parser.parse(pattern)
                    self.assertEqual(expected_false[i], result)


    def test_number_pattern(self):
        """
        Test parsing several patterns composed of numbers and simple math operations.
        """
        parser = PARSER
        patterns = [
            ".5", 
            "0.5",
            "1, 2, 3",
            "1+1, 2*3, 4-1, 5/2",
        ]
        expected = [
            [.5], 
            [0.5],
            [1, 2, 3],
            [2, 6, 3, 2.5],
        ]
        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                result = parser.parse(pattern)
                self.assertEqual(len(result), len(expected[i]))
                for x, y in zip(result, expected[i]):
                    self.assertAlmostEqual(x, y)

    def test_list_arithmetic(self):
        """
        Test parsing several patterns composed of numbers and simple math operations.
        """
        parser = PARSER
        patterns = [
            "[1,2,3]+1, [1,2,3]*2", 
            "[1,2,3]/2, [1,2,3]//2", 
            "[2,3,4]-2, [2,3,4]%2", 
            "[1,2,3,4]+[1,2,3,4]", 
            "[1,2,3,4]*[1,2,3,4]", 
            "[1,2,3,4]/[1,2,3,4]", 
            "[1,2,3,4]/[2,3,4,5]", 
            "[2,4,6,8]%[12,8]", 
        ]
        expected = [
            [2, 3, 4, 2, 4, 6], 
            [0.5, 1.0, 1.5, 0, 1, 1], 
            [0, 1, 2, 0, 1, 0], 
            [2, 4, 6, 8], 
            [1, 4, 9, 16], 
            [1.0, 1.0, 1.0, 1.0], 
            [0.5, 0.6666666666666666, 0.75, 0.8], 
            [2, 4, 6, 0], 
        ]
        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                result = parser.parse(pattern)
                self.assertEqual(len(result), len(expected[i]))
                for x, y in zip(result, expected[i]):
                    self.assertAlmostEqual(x, y)

    def test_notes(self):
        """
        Test parsing simple note composition
        """
        parser = PARSER
        patterns = [
                "C,D,E,F,G,A,B",
                "Do,Re,Mi,Fa,Sol,La,Si",
                "Do,Ré,Mi,Fa,Sol,La,Si",
                "C0,C1,C2,C3,C4,C5,C6,C7,C8,C9",
                "C, C#, Cb", 
                "C, Eb, G",
                "C, C., C.., C...",
                "C, C', C'', C'''",
                "C@maj7, C@min7",
        ]
        expected = [
            [60, 62, 64, 65, 67, 69, 71],
            [60, 62, 64, 65, 67, 69, 71],
            [60, 62, 64, 65, 67, 69, 71],
            [12, 24, 36, 48, 60, 72, 84, 96, 108, 120],
            [60, 61, 59], 
            [60, 63, 67],
            [60, 48, 36, 24],
            [60, 72, 84, 96],
            [60, 64, 67, 71, 60, 63, 67, 70],
        ]
        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                result = parser.parse(pattern)
                self.assertEqual(len(result), len(expected[i]))
                for x, y in zip(result, expected[i]):
                    self.assertEqual(x, y)

    def test_integer_ranges(self):
        """
        Test parsing integer ranges
        """

        def in_range(test_range: list, y: Union[int, float]) -> bool:
            return y in test_range

        parser = PARSER
        patterns = [
                "0~1", 
                "0~10", 
                "100~200",
        ]

        expected = [
            list(range(0,2)),
            list(range(0,11)),
            list(range(100,201))
        ]

        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                result = parser.parse(pattern)[0]
                self.assertTrue(in_range(
                    expected[i], y=result))

    def test_list_expansion(self):
        """
        Test the ! and !! operators for expanding lists
        """

        parser = PARSER
        patterns = [
                "[1,2]!2", 
                "[1,2]!!2", 
                "[1,.]!2", 
                "[1,.]!!2", 
        ]

        expected = [
                [1,2,1,2],
                [1,1,2,2],
                [1,None,1,None],
                [1,1,None,None],
        ]

        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                result = parser.parse(pattern)
                self.assertEqual(expected[i], result)

    def test_negation(self):
        """
        Test the ! and !! operators for expanding lists
        """

        parser = PARSER
        patterns = [
                "-1", 
                "-22.231",
        ]

        expected = [
                [-1],
                [-22.231],
        ]

        for i, pattern in enumerate(patterns):
            with self.subTest(i=i, pattern=pattern):
                result = parser.parse(pattern)
                self.assertEqual(expected[i], result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
