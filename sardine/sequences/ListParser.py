from lark import Lark, Transformer, v_args
from itertools import cycle, islice, count, chain
from pathlib import Path
import random

__all__ = ("ListParser", "Pnote", "Pname", "Pnum")

class ParserError(Exception):
    pass

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
    # Scales begin here
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "hminor": [0, 2, 3, 5, 7, 8, 11],
    "^minor": [0, 2, 3, 5, 7, 9, 11], # doesn't work
    "vminor": [0, 2, 3, 5, 7, 8, 10],
    "penta": [0, 2, 4, 7, 9],
}

def floating_point_range(start, end, step):
    assert step != 0
    sample_count = int(abs(end - start) / step)
    return islice(count(start, step), sample_count)

@v_args(inline=True)  # Affects the signatures of the methods
class CalculateTree(Transformer):
    number = float

    # Notes
    def random_note(self): 
        return random.randint(1, 127)

    def random_note_in_range(self, number0, number1): 
        return random.randint(int(number0), int(number1))

    def make_note_anglo_saxon(self, symbol):
        table = {'C':60, 'D':62, 'E':64, 'F':65, 'G':67, 'A':69, 'B':71}
        return table[symbol.upper()]

    def make_notes(self, symbols):
        return list(symbols)

    def make_note_french_system(self, symbol):
        table = {'do': 60, 're': 62, 'ré': 62, 'mi': 64, 
                'fa': 65, 'sol': 67, 'la': 69, 'si':71}
        return table[symbol]

    def add_octave(self, note, number):
        match_table = {60:0, 62:2, 64:4, 65:5, 67:7, 69:9, 71: 11}
        return match_table[note] + 12 * int(number)

    def sharp_simple(self, note): 
        return note+1

    def flat_simple(self, note): 
        return note-1

    def sharp_octave(self, note, number): 
        match_table = {60:0, 62:2, 64:4, 65:5, 67:7, 69:9, 71: 11}
        return match_table[note]+12*int(number)+1

    def flat_octave(self, note, number): 
        match_table = {60:0, 62:2, 64:4, 65:5, 67:7, 69:9, 71: 11}
        return match_table[note]+12*int(number)-1

    def choice_note(self, note0, note1): 
        return random.choice([note0, note1])

    def repeat_note(self, note, number): 
        return [note]*int(number)

    def drop_octave(self, note): 
        return note - 12

    def raise_octave(self, note): 
        return note + 12

    def drop_octave_x(self, note, number): 
        return note - 12*int(number)

    def raise_octave_x(self, note, number): 
        return note + 12*int(number)

    def add_qualifier(self, note, qualifier):
        return [note+x for x in qualifiers[qualifier]]

    def invert_chord(self, notes):
        pass

    def transpose_up(self, notes, number):
        return notes+int(number)

    def transpose_down(self, notes, number):
        return notes-int(number)

    def make_number(self, *token):
        return int("".join(token))

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

    def generate_ramp_with_range(self, left, right, step):
        return list(floating_point_range(start=left, end=right, step=step))

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

    def make_integer(self, value): 
        return int(value)

    def sample_number_name(self, number, name): 
        return str("".join([str(number), str(name)]))

    def sample_name_number(self, name, number): 
        return str("".join([str(name), str(number)]))

    def associate_sample_number(self, name, value):
        def _simple_association(name, value):
            return name + ":" + str(int(value))

        # Potential types for names
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

grammar_path = Path(__file__).parent
grammars = {"number": grammar_path / "grammars/number.lark",
            "name": grammar_path   / "grammars/name.lark",
            "note": grammar_path   / "grammars/note.lark"}

NUMBER_GRAMMAR = Lark.open(grammars['number'], rel_to=__file__, parser='lalr', transformer=CalculateTree())
NOTE_GRAMMAR   = Lark.open(grammars['note'],   rel_to=__file__, parser='lalr', transformer=CalculateTree())
NAME_GRAMMAR   = Lark.open(grammars['name'], rel_to=__file__, parser='lalr', transformer=CalculateTree())
NUMBER_PARSER, NOTE_PARSER, NAME_PARSER = NUMBER_GRAMMAR.parse, NOTE_GRAMMAR.parse, NAME_GRAMMAR.parse

class ListParser:
    def __init__(self, parser_type: str='number'):
        if parser_type=='number':
            self.parser = NUMBER_PARSER
        elif parser_type=='note':
            self.parser = NOTE_PARSER
        elif parser_type=='name':
            self.parser = NAME_PARSER
        else:
            ParserError(f'Invalid Parser grammar, {parser_type} is not a grammar.')

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
            except Exception as e:
                raise ParserError(f"Incorrect token: {token}") from e 
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