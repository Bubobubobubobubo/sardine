from lark import Lark, Transformer, v_args
from itertools import cycle, islice, count, chain
import random

__all__ = ("ListParser", "Pnote", "Pname", "Pnum")


class ParsingError(Exception):
    pass

# I don't know if it is worth it to go further. It's probably
# better to stack chords at this point to obtain the desired
# quality.
qualifiers = {
    'dim'    : [0, 3, 6, 12],
    'dim9'   : [0, 3, 6, 9, 14],
    'hdim7'  : [0, 3, 6, 10],
    'hdim9'  : [0, 3, 6, 10, 14],
    'hdimb9'  : [0, 3, 6, 10, 13],
    'dim7'   : [0, 3, 6, 9],
    '7dim5'  : [0, 4, 6, 10],
    'aug'    : [0, 4, 8, 12],
    'augMaj7': [0, 4, 8, 11],
    'aug7'   : [0, 4, 8, 10],
    'aug9'   : [0, 4, 10, 14],
    'maj'    : [0, 4, 7, 12],
    'maj7'   : [0, 4, 7, 11],
    'maj9'   : [0, 4, 11, 14],
    'minmaj7': [0, 3, 7, 11],
    '7'      : [0, 4, 7, 10],
    '9'      : [0, 4, 10, 14],
    'b9'     : [0, 4, 10, 13],
    'mM9'    : [0, 3, 11, 14],
    'min'    : [0, 3, 7, 12],
    'min7'   : [0, 3, 7, 10],
    'min9'   : [0, 3, 10, 14],
    'sus4'   : [0, 5, 7, 12],
    'sus2'   : [0, 2, 7, 12],
    'b5'     : [0, 4, 6, 12],
    'mb5'    : [0, 3, 6, 12],
}


number_grammar = """

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

note_grammar = """
    ?start: note

    ?number: /[0-9]/

    ?note: atom
         | atom "/" atom                     -> slash_chord
         | atom "|" atom                     -> choice_note
         | atom "!" number                   -> repeat_note
         | atom ":" NAME                     -> add_qualifier
         | atom "_" number                   -> invert_chord

    pure_atom: /[A-G]/                       -> make_note_anglo_saxon
             | /do|re|ré|mi|fa|sol|la|si/    -> make_note_french_system
    
    ?atom: pure_atom
         | atom "0".."9"                     -> add_octave
         | atom "#"                          -> sharp_simple
         | atom "b"                          -> flat_simple
         | atom "-"                          -> drop_octave
         | atom "+"                          -> raise_octave
         | atom "#" number                   -> sharp_octave
         | atom "b" number                   -> flat_octave
         | "(" atom (atom)* ")"
    
    %import common.CNAME -> NAME
"""


def floating_point_range(start, end, step):
    assert step != 0
    sample_count = int(abs(end - start) / step)
    return islice(count(start, step), sample_count)


@v_args(inline=True)  # Affects the signatures of the methods
class CalculateTree(Transformer):
    number = float

    # Notes
    def make_note_anglo_saxon(self, symbol):
        table = {'C':0, 'D':2, 'E':4, 'F':5, 
                'G':7, 'A':9, 'B':11}
        return table[symbol]
    def make_notes(self, symbols):
        return list(symbols)
    def make_note_french_system(self, symbol):
        table = {'do': 0, 're': 2, 'ré': 2, 'mi':4, 'fa':5, 'sol':7, 'la':9, 'si':11}
        return table[symbol]
    def add_octave(self, note, number):
        return note + 12*int(number)
    def sharp_simple(self, note): return note+1
    def flat_simple(self, note): return note-1
    def sharp_octave(self, note, number): return note+12*int(number)+1
    def flat_octave(self, note, number): return note+12*int(number)-1
    def choice_note(self, note0, note1): return random.choice([note0, note1])
    def repeat_note(self, note, number): return [note]*int(number)
    def drop_octave(self, note): return note - 12
    def raise_octave(self, note): return note + 12
    def add_qualifier(self, note, qualifier):
        return [note+x for x in qualifiers[qualifier]]
    def invert_chord(self, notes):
        pass
    def slash_chord(self, note0, note1):
        note0, note1 = [note0], [note1]
        return note0.extend(note1)


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


name_grammar = number_grammar # temporary, please fix
NUMBER_GRAMMAR = Lark(number_grammar, parser="lalr", transformer=CalculateTree())
NOTE_GRAMMAR = Lark(note_grammar, parser="lalr", transformer=CalculateTree())
NAME_GRAMMAR = Lark(name_grammar, parser="lalr", transformer=CalculateTree())
NUMBER_PARSER = NUMBER_GRAMMAR.parse
NOTE_PARSER = NOTE_GRAMMAR.parse
NAME_PARSER = NAME_GRAMMAR.parse

class ListParser:
    def __init__(self, parser_type: str='number'):
        if parser_type=='number':
            self.parser = NUMBER_PARSER
        elif parser_type=='note':
            self.parser = NOTE_PARSER
        elif parser_type=='name':
            self.parser = NAME_PARSER

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


# Useful utilities

def Pname(pattern: str, i: int = 0):
    parser = ListParser(parser_type='name')
    pattern = parser.parse(pattern)
    return pattern[i % len(pattern)]

def Pnote(pattern: str, i: int = 0):
    parser = ListParser(parser_type='name')
    pattern = parser.parse(pattern)
    return pattern[i % len(pattern)]

def Pnum(pattern: str, i: int = 0):
    parser = ListParser(parser_type='name')
    pattern = parser.parse(pattern)
    return pattern[i % len(pattern)]