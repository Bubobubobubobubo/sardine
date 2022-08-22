from lark import Lark, Transformer, v_args
from itertools import cycle, islice, count, chain
import random

__all__ = ("ListParser",)


class ParsingError(Exception):
    pass


grammar = """

    ?start: sum

    ?sum: product
        | sum "+" product   -> addition
        | sum "-" product   -> substraction

    ?product: atom
        | product "*" atom  -> multiplication
        | product "/" atom  -> division
        | product "|" atom  -> choice
        | product ":" atom  -> random_in_range
        | product "!" atom  -> extend
        | product "!!" atom  -> extend_repeat

    ?name: NAME          -> sample_name
         | name ":" sum  -> associate_sample_number
         | name "+" name -> add_name
         | name "-" name -> sub_name
         | name "!" sum  -> repeat_name
         | name "|" name -> choice_name
         | "[" name ("," name)* ","? "]" -> make_list
         | "(" name ")"

    ?list: "[" sum ("," sum)* ","? "]" -> make_list
         | atom "_" atom                 -> generate_ramp

    ?value: NUMBER -> number
          | list

    ?atom: value
         | "-" atom         -> negation
         | "+" atom         -> id
         | name
         | "(" sum ")"
         | "r"              -> get_random_number

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""


def floating_point_range(start, end, step):
    assert step != 0
    sample_count = int(abs(end - start) / step)
    return islice(count(start, step), sample_count)


@v_args(inline=True)  # Affects the signatures of the methods
class CalculateTree(Transformer):
    number = float

    def id(self, a):
        return a

    def make_list(self, *args):
        return list(args)

    def get_random_number(self):
        return random.random()

    def generate_ramp(self, left, right):
        return list(range(int(left), int(right) + 1))

    def extend(self, left, right):
        if all(map(lambda x: isinstance(x, float), [left, right])):
            return [left] * int(right)
        if isinstance(left, list) and isinstance(right, (float, int)):
            new_list = []
            for _ in range(int(right)):
                [new_list.append(x) for x in left]
            return new_list
        if isinstance(left, (float, int)) and isinstance(right, list):
            new_list = []
            for _ in range(int(left)):
                [new_list.append(x) for x in right]
            return new_list

    def extend_repeat(self, left, right):
        if isinstance(left, (float, int)):
            if isinstance(right, (list, float, int)):
                return self.extend(left, right)
        if isinstance(left, list):
            if isinstance(right, (int, float)):
                return [x for x in left for _ in range(0, int(right))]
            elif isinstance(right, list):
                new_list = []
                cycling_through = cycle(right)
                for element in left:
                    for _ in range(int(next(cycling_through))):
                        new_list.append(element)
                return new_list

    def choice(self, left, right):
        return random.choice([left, right])

    def random_in_range(self, left, right):
        if all(map(lambda x: isinstance(x, float), [left, right])):
            return random.uniform(left, right)
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [random.uniform(x, y) for x, y in zip(cycle(right), left)]

    def negation(self, value):
        if isinstance(value, float):
            return -value
        elif isinstance(value, list):
            return [-x for x in value]

    def addition(self, left, right):
        if all(map(lambda x: isinstance(x, float), [left, right])):
            return left + right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x + y for x, y in zip(cycle(right), left)]
        elif isinstance(left, (int, float)) and isinstance(right, list):
            return [x + left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x + right for x in left]

    def substraction(self, left, right):
        if all(map(lambda x: isinstance(x, float), [left, right])):
            return left - right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x - y for x, y in zip(cycle(right), left)]
        elif isinstance(left, (int, float)) and isinstance(right, list):
            return [x - left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x - right for x in left]

    def multiplication(self, left, right):
        if all(map(lambda x: isinstance(x, float), [left, right])):
            return left * right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x * y for x, y in zip(cycle(right), left)]
        if isinstance(left, (int, float)) and isinstance(right, list):
            return [x * left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x * right for x in left]

    def division(self, left, right):
        if all(map(lambda x: isinstance(x, float), [left, right])):
            return left / right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x / y for x, y in zip(cycle(right), left)]
        if isinstance(left, (int, float)) and isinstance(right, list):
            return [x / left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x / right for x in left]

    def sample_name(self, name):
        return str(name)

    def associate_sample_number(self, name, value):
        def _simple_association(name, value):
            return name + ":" + str(int(value))

        # Possible tyoes for names
        if isinstance(name, str):
            if isinstance(value, (float, int)):
                return _simple_association(name, value)
            elif isinstance(value, list):
                return [_simple_association(name, x) for x in value]

        if isinstance(name, list):
            if isinstance(value, (float, int)):
                return [_simple_association(n, value) for n in name]
            if isinstance(value, list):
                return [str(x) + ":" + str(int(y)) for x, y in zip(cycle(name), value)]

    def add_name(self, a, b):
        return a + b

    def sub_name(self, a, b):
        return a.replace(b, "")

    def choice_name(self, a, b):
        return random.choice([a, b])

    def repeat_name(self, name, value):
        return [name] * int(value)


GRAMMAR = Lark(grammar, parser="lalr", transformer=CalculateTree())
PARSER = GRAMMAR.parse


class ListParser:
    def __init__(self):
        # self._parser = Lark(grammar, parser='lalr', transformer=CalculateTree())
        self.parser = PARSER

    def _flatten_result(self, pat):
        """Flatten a nested pattern result list. Probably not optimised."""
        if len(pat) == 0:
            return pat
        if isinstance(pat[0], list):
            return self._flatten_result(pat[0]) + self._flatten_result(pat[1:])
        return pat[:1] + self._flatten_result(pat[1:])

    def _parse_token(self, string: str):
        """Parse a single token"""
        return self.parser(string)

    def parse(self, pattern: str):
        """Parse a whole pattern and return a flattened list"""
        final_pattern = []
        for token in pattern.split():
            try:
                final_pattern.append(self._parse_token(token))
            except Exception:
                raise ParsingError(f"Incorrect token: {token}")
        return self._flatten_result(final_pattern)

    def _parse_debug(self, pattern: str):
        """Parse a whole pattern in debug mode"""
        final_pattern = []
        for token in pattern.split():
            try:
                print(self._parse_token(token))
            except Exception as e:
                import traceback

                print(f"Error: {e}: {traceback.format_exc()}")
                continue
