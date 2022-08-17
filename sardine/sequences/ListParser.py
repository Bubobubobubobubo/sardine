from lark import Lark, Transformer, v_args
from itertools import cycle, islice, count, chain
import random

__all__ = ('ListParser',)


grammar = """
    ?start: sum
          | list -> list

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub
        | sum "|" product   -> choice
        | sum ":" product   -> range

    ?product: atom
            | product "*" atom   -> mul
            | product "**" atom  -> pow
            | product "/" atom   -> div
            | product "!" atom   -> extend

    ?random:
           | "r" -> get_random_number
           | "r" "!" atom -> replicate_random_number

    ?name: NAME -> sample_name
         | name ":" sum -> associate_sample_number
         | name "+" name -> add_name
         | name "-" name -> sub_name
         | name "|" name -> choice_name
         | "(" name ")"

    ?atom: NUMBER           -> number
         | name
         | "-" atom         -> neg
         | "(" sum ")"
         | random

    ?list: "[" (atom ",")* atom"]" -> make_list
         | atom "->" atom -> generate_ramp
         | atom "->" "(" atom ")" atom -> generate_ramp_step
         | list "+" atom -> add_number_to_list
         | list "-" atom -> sub_number_to_list
         | list "*" atom -> mul_number_to_list
         | list "**" atom -> pow_number_to_list
         | list "/" atom -> div_number_to_list
         | list "+" list -> add_list
         | list "-" list -> sub_list
         | list "*" list -> mul_list
         | list "/" list -> div_list
         | list "**" list -> pow_list
         | list "**" atom -> pow_number_to_list
         | list "|" list -> choice_list
         | list "!" atom -> extend_list

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %import common.WS

    %ignore WS_INLINE
"""

def floating_point_range(start, end, step):
    assert (step != 0)
    sample_count = int(abs(end - start) / step)
    return islice(count(start, step), sample_count)

@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv, neg, pow
    number = float

    def __init__(self):
        self.vars = {}

    # names

    def add_name(self, a, b):
        return a + b

    def sub_name(self, a, b):
        return a.replace(b, '')

    def choice_name(self, a, b):
        return random.choice([a, b])

    def associate_sample_number(self, a, b):
        return a + ":" + str(int(b))


    # Generators
    def get_random_number(self):
        return random.random()

    def get_random_number_in_range(self, a):
        return random.random() * a


    def replicate_random_number(self, a):
        return [random.random() for x in list(range(int(a)))]

    def generate_ramp(self, a, b):
        return list(range(int(a), int(b + 1)))

    def generate_ramp_step(self, a, b, c):
        result = list(floating_point_range(start=a,end=b,step=c))
        print(result)
        return result

    # List-based operations

    def choice_list(self, a, b):
        return self.choice(a, b)

    def add_number_to_list(self, a, b):
        return [x+b for x in a]

    def sub_number_to_list(self, a, b):
        return [x-b for x in a]

    def mul_number_to_list(self, a, b):
        return [x*b for x in a]

    def div_number_to_list(self, a, b):
        return [x/b for x in a]

    def pow_number_to_list(self, a, b):
        return [pow(x,b) for x in a]

    def list(self, value):
        return value

    def make_list(self, *args):
        """Form a Python-based list for further operations"""
        return list(args)

    def add_list(self, a, b):
        return [x + y for x, y in zip(cycle(b), a)]

    def sub_list(self, a, b):
        return [x - y for x, y in zip(cycle(b), a)]

    def mul_list(self, a, b):
        return [x * y for x, y in zip(cycle(a), b)]

    def div_list(self, a, b):
        return [x / y for x, y in zip(cycle(a), b)]

    def pow_list(self, a, b):
        return [pow(x, y) for x, y in zip(cycle(a), b)]

    def extend(self, atom, factor):
        """Duplicate 'atom' to form list [atom]*factor"""
        return [atom]*int(factor)

    def extend_list(self, atom, factor):
        """Extend list by factor, replicating the content x times"""
        new_list = []
        for _ in range(int(factor)):
            [new_list.append(x) for x in atom]
        return new_list

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    # Extended arithmetic

    def range(self, a, b):
        """Generate a number in range"""
        return random.uniform(a, b)

    def choice(self, a, b):
        """Choose between two tokens"""
        return random.choice([a, b])

    # Sample and names handling

    def sample_name(self, name):
        """Return a sample name"""
        return str(name)

GRAMMAR = Lark(grammar, parser='lalr', transformer=CalculateTree())
PARSER  = GRAMMAR.parse

class ListParser:
    def __init__(self):
        # self._parser = Lark(grammar, parser='lalr', transformer=CalculateTree())
        self.parser = PARSER

    def _flatten_result(self, pat):
        """Flatten a nested pattern result list. Probably not optimised. """
        if len(pat) == 0:
            return pat 
        if isinstance(pat[0], list):
            return self._flatten_result(pat[0]) + self._flatten_result(pat[1:])
        return pat[:1] + self._flatten_result(pat[1:])

    def _parse_token(self, string: str):
        """Parse a single token"""
        return self.parser(string)
    
    def parse(self, pattern: str):
        """Parse a whole pattern and return a flatenned list"""
        final_pattern = []
        for token in pattern.split():
            try:
                final_pattern.append(
                    self._parse_token(token))
            except Exception:
                continue
        return self._flatten_result(final_pattern)
        


if __name__ == '__main__':
    calc_parser = Lark(grammar, parser='lalr', transformer=CalculateTree())
    calc = calc_parser.parse
   
    def main():
        while True:
            try:
                s = input('> ')
                s = s.split()
            except EOFError:
                break
            liste = []
            for elem in s:
                try:
                    liste.append(calc(elem))
                except Exception:
                    continue
                # print(calc(s))
            print(liste)

    parser = ListParser()
    print(parser.parse('[1,2] 2 3 r!4'))