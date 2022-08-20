from typing import List
import unittest
import sys

sys.path.append("..")
from ListParser import ListParser


class NumberTest(unittest.TestCase):
    def test_positive_negative(self):
        self.assertEqual(ListParser().parse("0"), [0.0])
        self.assertEqual(ListParser().parse("-0"), [0.0])
        self.assertEqual(ListParser().parse("+0"), [0.0])

    def test_parenthesis(self):
        self.assertEqual(ListParser().parse("(0)"), [0.0])
        self.assertEqual(ListParser().parse("(0.0)"), [0.0])
        self.assertEqual(ListParser().parse("((((0.0))))"), [0.0])

    def test_mul_div_precedence(self):
        self.assertEqual(ListParser().parse("2*2+4"), [8.0])
        self.assertEqual(ListParser().parse("2/2+4"), [5.0])

    def test_parenthesis_precedence(self):
        self.assertEqual(ListParser().parse("(3+3)*3"), [18.0])
        self.assertEqual(ListParser().parse("(3+3)/3"), [2.0])

    def test_arithmetic_operators(self):
        operators = ["+", "-", "*", "/"]
        for operator in operators:
            # 2+2
            self.assertEqual(
                ListParser().parse(f"2{operator}2"), [float(eval(f"2{operator}2"))]
            )
            # (2)+(2)
            self.assertEqual(
                ListParser().parse(f"(2){operator}(2)"),
                [float(eval(f"(2){operator}(2)"))],
            )
            # 2+2+2
            self.assertEqual(
                ListParser().parse(f"2{operator}2{operator}2"),
                [float(eval(f"2{operator}2{operator}2"))],
            )
            # (2+2)+2
            self.assertEqual(
                ListParser().parse(f"(2{operator}2){operator}2"),
                [float(eval(f"(2{operator}2){operator}2"))],
            )
            # -2+2
            self.assertEqual(
                ListParser().parse(f"-2{operator}2"), [float(eval(f"-2{operator}2"))]
            )
            # -2+-2
            self.assertEqual(
                ListParser().parse(f"-2{operator}-2"), [float(eval(f"-2{operator}-2"))]
            )


class RandomTest(unittest.TestCase):
    def test_generate_random_number(self):
        self.assertTrue(0.0 < ListParser().parse("r")[0] < 1.0)

    def test_extend_on_random_number(self):
        true_for_all = []
        pattern = ListParser().parse("r!3")
        for token in pattern:
            if 0.0 < token < 1.0:
                true_for_all.append(True)
            else:
                true_for_all.append(False)
        self.assertTrue(all(true_for_all))

    def test_rng_number_arithmetic(self):
        self.assertTrue(-1.0 < ListParser().parse("-r")[0] < 0.0)
        self.assertTrue(1.0 < ListParser().parse("r+1")[0] < 2.0)
        self.assertTrue(0.0 < ListParser().parse("r*4")[0] < 4.0)

    def test_number_in_range(self):
        self.assertTrue([1.0] == ListParser().parse("1:1"))
        self.assertTrue(0.0 < ListParser().parse("0:5")[0] < 5.0)
        self.assertTrue(5.0 < ListParser().parse("5:10")[0] < 10.0)

    def test_choice_operator_on_number(self):
        self.assertTrue(ListParser().parse("1|2|3|4|5")[0] in [1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertTrue(ListParser().parse("-1|-2")[0] in [-1.0, -2.0])


class ListTest(unittest.TestCase):
    def test_basic_list(self):
        self.assertEqual(ListParser().parse("[2,2]"), [2.0, 2.0])
        self.assertEqual(ListParser().parse("[2**2,3**3]"), [4.0, 27.0])
        self.assertEqual(ListParser().parse("[dada,dada]"), ["dada", "dada"])

    def test_list_addition(self):
        self.assertEqual(ListParser().parse("[2,2]+[2,2]"), [4.0, 4.0])
        self.assertEqual(ListParser().parse("([2,2])+([2,2])"), [4.0, 4.0])

    def test_list_substraction(self):
        self.assertEqual(ListParser().parse("[2,2]-[2,2]"), [0.0, 0.0])
        self.assertEqual(ListParser().parse("([2,2]-[2,2])"), [0.0, 0.0])

    def test_list_multiplication(self):
        self.assertEqual(ListParser().parse("[2,2]*[2,2]"), [4.0, 4.0])
        self.assertEqual(ListParser().parse("([2,2])*([2,2])"), [4.0, 4.0])

    def test_list_division(self):
        self.assertEqual(ListParser().parse("[2,2]/[2,2]"), [1.0, 1.0])
        self.assertEqual(ListParser().parse("([8,8])/([4,4])"), [2.0, 2.0])

    def test_list_power(self):
        self.assertEqual(ListParser().parse("[2,2]**[2,2]"), [4.0, 4.0])
        self.assertEqual(ListParser().parse("([2,2])**([2,2])"), [4.0, 4.0])

    def number_arithmetic_applied_to_list(self):
        self.assertEqual(ListParser().parse("[2,2]+1"), [3.0, 3.0])
        self.assertEqual(ListParser().parse("1+[2,2]"), [3.0, 3.0])
        self.assertEqual(ListParser().parse("[2,2]-1"), [1.0, 1.0])
        self.assertEqual(ListParser().parse("1-[2,2]"), [1.0, 1.0])
        self.assertEqual(ListParser().parse("[2,2]*2"), [4.0, 4.0])
        self.assertEqual(ListParser().parse("2*[2,2]"), [4.0, 4.0])
        self.assertEqual(ListParser().parse("[2,2]/2"), [1.0, 1.0])
        self.assertEqual(ListParser().parse("2/[2,2]"), [1.0, 1.0])
        self.assertEqual(ListParser().parse("[2,2]**10"), [1024.0, 1024.0])
        self.assertEqual(ListParser().parse("10**[2,2]"), [1024.0, 1024.0])
