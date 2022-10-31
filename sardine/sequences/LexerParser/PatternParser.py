from lark import Lark, Transformer
from pathlib import Path
import math
import random

grammar_path = Path(__file__).parent
grammar = grammar_path / "grammars/rewrite.lark"

class Directive:
    def __init__(self, name, index=0):
        self.name = name
        self.index = index
    def __str__(self):
        return self.name + ":" + str(self.index)
    def __matmul__(self, other):
        if isinstance(other, int):
            return Directive(self.name, other)
        elif isinstance(other, float):
            return Directive(self.name, int(other))
        else:
            return NotImplemented


class MidiNote:
    def __init__(self, midi):
        self.midi = midi
    def __str__(self):
        return "MidiNote({})".format(self.midi)

    midi_bases = {'A': -3, 'B': -1, 'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7}
    @staticmethod
    def make_from_desc(desc):
        count = MidiNote.midi_bases[str(desc[0]).upper()]
        desc_has_digit = False
        for item in desc[1:]:
            if str(item).isdigit():
                count += int(item) * 12
                desc_has_digit = True
            elif str(item) == 'b':
                count -= 1
            elif str(item) == '#':
                count += 1
            elif str(item) == '.':
                count -= 12
            elif str(item) == "'":
                count += 12
        if not desc_has_digit:
            count += 60
        return MidiNote(count)

    def midi_wrap(op):
        def wrapper(self, other):
            if isinstance(other, MidiNote):
                return MidiNote(op(self.midi, other.midi) % 127)
            elif isinstance(other, int):
                return MidiNote(op(self.midi, other) % 127)
            elif isinstance(other, float):
                return MidiNote(op(self.midi, int(other)) % 127)
            else:
                return NotImplemented
        return wrapper

    __add__ = midi_wrap(lambda x,y: x+y)
    __radd__ = __add__
    __sub__ = midi_wrap(lambda x,y: x-y)
    __rsub__ = midi_wrap(lambda x,y: y-x)
    __mul__ = midi_wrap(lambda x,y: x*y)
    __rmul__ = __mul__
    __truediv__ = midi_wrap(lambda x,y: x//y)
    __rtruediv__ = midi_wrap(lambda x,y: y//x)


class Vector:
    def __init__(self, items, flat):
        self.items = items
        self.flat = flat
    def __str__(self):
        return str([str(item) for item in self.items])
    def __len__(self):
        return len(self.items)

    def vectorize(op):
        def wrapper(self, other):
            if isinstance(other, (int, float, MidiNote, Directive)):
                return Vector([op(x, other) for x in self.items], self.flat)
            elif isinstance(other, Vector):
                if self.flat == other.flat:
                    if len(self) == len(other):
                        return Vector([op(x, y) for x, y in zip(self.items, other.items)], self.flat)
                    else:
                        return NotImplemented
                else:
                    if self.flat:
                        return Vector([op(x, other) for x in self.items], True)
                    else:
                        return Vector([op(self, y) for y in other.items], True)
            else:
                return NotImplemented
        return wrapper

    __add__ = vectorize(lambda x,y: x+y)
    __radd__ = __add__
    __sub__ = vectorize(lambda x,y: x-y)
    __rsub__ = vectorize(lambda x,y: y-x)
    __mul__ = vectorize(lambda x,y: x*y)
    __rmul__ = __mul__
    __truediv__ = vectorize(lambda x,y: x/y)
    __rtruediv__ = vectorize(lambda x,y: y/x)
    __matmul__ = vectorize(lambda x,y: x@y)
    __rmatmul__ = vectorize(lambda x,y: y@x)


def flatten(iterable):
    result = []
    for item in iterable:
        if isinstance(item, Vector) and item.flat:
            result.extend(item.items)
        else:
            result.append(item)
    return result


def apply_func(func, item):
    if isinstance(item, Vector):
        return Vector([apply_func(func, x) for x in item.items], item.flat)
    else:
        return func(item)


class PatternTransformer(Transformer):
    def pattern(self, children):
        return flatten(children)

    def add(self, children):
        return children[0]+children[1]
    def substract(self, children):
        return children[0]-children[1]
    def multiply(self, children):
        return children[0]*children[1]
    def divide(self, children):
        return children[0]/children[1]
    def negate(self, children):
        return (-1)*children[0]
    def math_func(self, children):
        return apply_func(getattr(math, children[0]), children[1])
    def random_number(self, children):
        return random.random()

    def ramp(self, children):
        return Vector(list(range(int(children[0]), int(children[1]))), True)
    def step_ramp(self, children):
        return Vector(list(range(int(children[0]), int(children[1]), int(children[2]))), True)
    def column(self, children):
        return Vector(list(children), False)
    def choice(self, children):
        return random.choice(children)
    def number(self, children):
        return float(children[0])
    def note(self, children):
        return MidiNote.make_from_desc(children)
    def repeat(self, children):
        return Vector(flatten([children[0]]*int(children[1])), True)

    reserved_names = {
        'note': ['Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb'],
        'math_func': ['sin', 'cos', 'tan']
    }
    def name_disamb(self, children):
        name = children[0]
        if name in PatternTransformer.reserved_names['note']:
            return make_note(name[0], name[1])
        return Directive(name)
    def specify_address(self, children):
        return Directive(children[0].name+"/"+children[1].name)
    def specify_index(self, children):
        return children[0] @ children[1]


class PatternParser:
    def __init__(self):
        with open(grammar) as f:
            self.parser = Lark(f.read())
        self.transformer = PatternTransformer()

    def parse(self, pattern):
        tree = self.parser.parse(pattern)
        result = self.transformer.transform(tree)
        return result
