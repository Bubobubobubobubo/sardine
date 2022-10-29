from lark import Transformer, v_args
from typing import Union
from .Qualifiers import qualifiers
from .Utilities import zip_cycle, map_unary_function, map_binary_function
from lark.lexer import Token
from typing import Any
from itertools import cycle, takewhile, count
from math import cos, sin, tan
from time import time
import datetime
import random


@v_args(inline=True)
class CalculateTree(Transformer):
    def __init__(self, clock, iterators, variables):
        super().__init__()
        self.clock = clock
        self.iterators = iterators
        self.variables = variables
        self.memory = {}

    def number(self, number):
        return float(number)

    def negative_number(self, number):
        return -float(number)

    def return_pattern(self, *args):
        return list(args)

    # ---------------------------------------------------------------------- #
    # Silence: handling silence 
    # ---------------------------------------------------------------------- #

    def silence(self, *args):
        """
        Pure silence. The absence of an event. Silence is represented using
        a dot or multiple dots for multiple silences.
        """
        return [None]*len(args)

    # ---------------------------------------------------------------------- #
    # Variables: methods concerning bi-valent variables
    # ---------------------------------------------------------------------- #

    def get_variable(self, letter):
        letter = str(letter)
        return getattr(self.variables, letter)

    def reset_variable(self, letter):
        letter = str(letter)
        self.variables.reset(letter)
        return getattr(self.variables, letter)

    def set_variable(self, letter, number):
        letter, number = str(letter), int(number)
        setattr(self.variables, letter, number)
        return getattr(self.variables, letter)

    # ---------------------------------------------------------------------- #
    # Iterators: methods concerning iterators
    # ---------------------------------------------------------------------- #

    def get_iterator(self, letter):
        letter = str(letter)
        return getattr(self.iterators, letter)

    def reset_iterator(self, letter):
        letter = str(letter)
        self.iterators.reset(letter)
        return getattr(self.iterators, letter)

    def set_iterator(self, letter, number):
        letter, number = str(letter), int(number)
        setattr(self.iterators, letter, number)
        return getattr(self.iterators, letter)

    def set_iterator_step(self, letter, number, step):
        letter, number, step = str(letter), int(number), int(step)
        setattr(self.iterators, letter, [number, step])
        return getattr(self.iterators, letter)

    # ---------------------------------------------------------------------- #
    # Notes: methods used by the note-specific parser
    # ---------------------------------------------------------------------- #

    def specify_address(self, name0, name1):
        """Convert underscore into slash for name based addresses"""
        return "".join([name0, "/", name1])

    def random_note_in_range(self, number0, number1):
        """Generates a random MIDI Note in the range number0 - number1.

        Args:
            number0 (int):  low boundary
            number1 (int): high boundary

        Returns:
            int: a random MIDI Note.
        """
        return random.randint(int(number0), int(number1))

    def make_note(self, *args):
        """Return a valid MIDI Note (fifth octave)
        from a valid anglo-saxon note name.

        Args:
            symbol (str): a string representing a valid note (a to g).

        Returns:
            int: A MIDI Note (fifth octave)
        """
        total = 0
        table = {"A": -3, "B": -1, "C": 0, "D": 2, "E": 4, "F": 5, "G": 7}
        args = list(args)

        if not any([str(x).isdigit() for x in args]):
            total += 60

        for token in args:
            if str(token).isdigit():
                number = int(token)
                if number >= 10:
                    total += int(token[0]) * 12
                else:
                    total += int(token) * 12
                continue
            if str(token) == "#":
                total += 1
                continue
            if str(token) == "b":
                total -= 1
                continue
            if str(token) == "'":
                total += 12
                continue
            if str(token) == ".":
                total -= 12
                continue
            try:
                if token.type == "NOTE":
                    total += table[str(token).upper()]
                    continue
            except AttributeError:
                pass

        if total >= 127:
            return 127
        elif total <= 0:
            return 0
        else:
            return total

    def add_modifier(self, col, *modifier):

        quali = list(modifier)
        quali = "".join([str(x) for x in quali])

        modifiers_list = {
            "expand": self.expand_collection,
            "disco": self.disco_collection,
            "palindrome": self.collection_palindrome,
            "reverse": self.reverse_collection,
            "braid": self.braid_collection,
            "shuffle": self.shuffle_collection,
            "drop2": self.collection_drop2,
            "drop3": self.collection_drop3,
            "drop2and4": self.collection_drop2and4,
        }
        try:
            return modifiers_list[quali](col)
        except Exception as e:
            return col

    def add_qualifier(self, note, *quali):
        """Adding a qualifier to a note taken from a qualifier list.
        Adding a qualifier is the main method to generate scales and
        chords in a monophonic fashion (each note layed out as a list).

        Qualifiers are applied by taking the first note as a reference,
        and building the collection of notes against it. Eg: c5:major
        the reference note -> [60, added notes from coll -> 67, 72]

        Args:
            note (int): A MIDI Note

        Returns:
            list: A collection of notes built by applying a collection to
            the note given as input.
        """
        quali = list(quali)
        quali = "".join([str(x) for x in quali])
        try:
            return [note + x for x in qualifiers[str(quali)]]
        except KeyError:
            return note

    def make_number(self, *token):
        """Turn a number from string to integer. Used by the parser,
        transform a token matched as a string to a number before
        applying other rules.

        Returns:
            int: an integer
        """
        return int("".join(token))

    def reverse_collection(self, collection):
        """Reverse a newly generated collection.

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: reversed list of integers from qualifier's based collection
        """
        if not isinstance(collection, list):
            return collection
        else:
            return reversed(collection)

    def collection_palindrome(self, collection):
        """Make a palindrome out of a newly generated collection

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: palindromed list of integers from qualifier's based
            collection
        """
        if not isinstance(collection, list):
            return collection
        else:
            return collection + list(reversed(collection))

    def shuffle_collection(self, collection):
        """Shuffle a newly generated collection

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: A shuffled list of integers
        """
        if not isinstance(collection, list):
            return collection
        else:
            random.shuffle(collection)
            return collection

    def braid_collection(self, collection):
        """Take the first half of a list, take its second half, interleave.

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: An interleaved list of integers
        """
        if not isinstance(collection, list):
            return collection
        else:
            col_len = len(collection) // 2
            first, second = collection[:col_len], collection[col_len:]
            return [val for pair in zip(first, second) for val in pair]

    def expand_collection(self, collection):
        """Chance-based operation. Apply a random octave transposition process
        to every note in a given collection.

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: Chance-expanded list of integers
        """

        def expand_number(number):
            expansions = [0, -12, 12]
            return number + random.choice(expansions)

        return map_unary_function(expand_number, collection)

    def disco_collection(self, collection):
        """Takes every other note down an octave

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: A list of integers
        """
        if not isinstance(collection, list):
            return collection
        else:
            offsets = cycle([-12, 0])
            return [x + offset for (x, offset) in zip(collection, offsets)]

    def collection_drop2(self, collection):
        """Simulate a drop2 chord.

        Args:
            collection (list): A list of integers

        Returns:
            list: A list of integers with the second note dropped an octave.
        """
        if not isinstance(collection, list):
            return collection
        else:
            collection[1] = collection[1] - 12
            return collection

    def collection_drop3(self, collection):
        """Simulate a drop3 chord.

        Args:
            collection (list): A list of integers

        Returns:
            list: A list of integers with the third note dropped an octave.
        """
        if not isinstance(collection, list):
            return collection
        else:
            collection[2] = collection[2] - 12
            return collection

    def collection_drop2and4(self, collection):
        """Simulate a drop2&4 chord.

        Args:
            collection (list): A list of integers

        Returns:
            list: A list of integers with the second and fourth note dropped
            an octave.
        """
        if not isinstance(collection, list):
            return collection
        else:
            collection[1] = collection[1] - 12
            collection[3] = collection[3] - 12
            return collection

    def id(self, a):
        """Identity function. Returns first argument."""
        return a

    def make_list(self, *args):
        """Make a list from gathered arguments (alias used by parser)

        Returns:
            list: Gathered arguments in a list
        """
        new_list = []
        for element in args:
            if isinstance(element, list):
                new_list += element
            else:
                new_list.append(element)
        return new_list

    def get_time(self):
        """Return current clock time (tick) as integer"""
        return int(self.clock.tick)

    def get_year(self):
        """Return current clock time (tick) as integer"""
        return int(datetime.datetime.now().year)

    def get_month(self):
        """Return current clock time (tick) as integer"""
        return int(datetime.datetime.now().month)

    def get_day(self):
        """Return current clock time (tick) as integer"""
        return int(datetime.datetime.now().day)

    def get_hour(self):
        """Return current clock time (tick) as integer"""
        return int(datetime.datetime.now().hour)

    def get_minute(self):
        """Return current clock time (tick) as integer"""
        return int(datetime.datetime.now().minute)

    def get_second(self):
        """Return current clock time (tick) as integer"""
        return int(datetime.datetime.now().second)

    def get_microsecond(self):
        """Return current clock time (tick) as integer"""
        return int(datetime.datetime.now().microsecond)

    def get_measure(self):
        """Return current measure (bar) as integer"""
        return int(self.clock.bar)

    def get_phase(self):
        """Return current phase (phase) as integer"""
        return int(self.clock.phase)

    def get_unix_time(self):
        """Return current unix time as integer"""
        return int(time())

    def get_random_number(self):
        """Return a random number (alias used by parser)

        Returns:
            float: a random floating point number
        """
        return random.random()

    def generate_ramp(self, left, right):
        """Generates a ramp of integers between x included and y
        included (used by parser). Note that this is an extension
        of Python's default range function: descending ranges are
        possible.

        Args:
            left (int): First boundary
            right (int): Second boundary

        Returns:
            list: a ramp of ascending or descending integers
        """
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            if int(left) > int(right):
                new_list = list(reversed(range(int(right), int(left) + 1)))
                return new_list
            else:
                return list(range(int(left), int(right) + 1))

        if isinstance(left, list):
            if isinstance(right, (float, int)):
                last = left.pop()
                return left + self.generate_ramp(last, right)

    def generate_ramp_with_range(self, left, right, step=1):
        """Generates a ramp of integers between x included and y
        included (used by parser). Variant using a step param.

        Args:
            left (int): First boundary
            right (int): Second boundary
            step (int): Range every x steps

        Returns:
            list: a ramp of ascending or descending integers with step
        """

        epsilon = 0.0000001
        start = min(left, right)
        stop = max(left, right)
        ramp = list(takewhile(lambda x: x < stop + epsilon, (start + i*abs(step) for i in count())))
        if left > right:
            return list(reversed(ramp))
        else:
            return ramp

    def extend(self, left, right):
        """Extend a token: repeat the token x times. Note that this function
        will work for any possible type on its left and right side. A list
        can extend a list, etc.. etc.. See examples for a better understanding
        of the mechanism.

        Examples:
        [1,2,3]![1,2,3] -> [1,2,2,3,3,3]
        1!3 -> [1,1,1]
        [2,1]!4 -> [2,1,2,1,2,1,2,1]
        etc..

        Args:
            left (Union[list, float, int]): A token that will be extended
            right (Union[list, float, int]): A token used as an extension rule

        Returns:
            list: A list of integers after applying the expansion rule.
        """
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            return [left] * int(right)
        if isinstance(left, list) and isinstance(right, (float, int)):
            return left * int(right)
        if isinstance(left, (float, int)) and isinstance(right, list):
            return [left] * sum (int(x) for x in right)
        if isinstance(left, list) and isinstance(right, list):
            return sum(([x]*int(y) for (x, y) in zip_cycle(left, right)), start=[])

    def extend_repeat(self, left, right):
        """Variation of the preceding rule.
        TODO: document this behavior."""
        if isinstance(left, (float, int)):
            if isinstance(right, (list, float, int)):
                return self.extend(left, right)
        if isinstance(left, list):
            if isinstance(right, (int, float)):
                return [x for x in left for _ in range(0, int(right))]
            elif isinstance(right, list):
                return sum(([x]*int(y) for (x, y) in zip_cycle(left, right)), start=[])

    def choice(self, left, right):
        """Choose 50%-50% between the 'left' or 'right' token

        Args:
            left (any): First possible choice
            right (any): Second possible choice

        Returns:
            any: A token chosen between 'left' or 'right'.
        """
        return random.choice([left, right])

    def random_in_range(self, left, right):
        return map_binary_function(random.uniform, left, right)

    def negation(self, value):
        return map_unary_function(lambda x: -x, value)

    def addition(self, left, right):
        return map_binary_function(lambda x, y: x + y, left, right)

    def waddition(self, left, right):
        """Wrapped variant of the addition method"""
        return map_binary_function(lambda x, y: (x + y)%127, left, right)

    def modulo(self, left, right):
        return map_binary_function(lambda x, y: x % y, left, right)

    def wmodulo(self, left, right):
        return map_binary_function(lambda x, y: (x % y)%127, left, right)

    def power(self, left, right):
        return map_binary_function(lambda x, y: pow(x, y), left, right)

    def wpower(self, left, right):
        """Wrapped variant of the power method"""
        return map_binary_function(lambda x, y: pow(x, y)%127, left, right)

    def substraction(self, left, right):
        return map_binary_function(lambda x, y: x - y, left, right)

    def wsubstraction(self, left, right):
        """Wrapped variant of the substraction method"""
        return map_binary_function(lambda x, y: (x - y)%127, left, right)

    def multiplication(self, left, right):
        return map_binary_function(lambda x, y: x * y, left, right)

    def wmultiplication(self, left, right):
        """Wrapped variant of the multiplication method"""
        return map_binary_function(lambda x, y: (x * y)%127, left, right)

    def division(self, left, right):
        return map_binary_function(lambda x, y: x / y, left, right)

    def wdivision(self, left, right):
        """Wrapped variant of the division method"""
        return map_binary_function(lambda x, y: (x / y)%127, left, right)

    def floor_division(self, left, right):
        return map_binary_function(lambda x, y: x // y, left, right)

    def wfloor_division(self, left, right):
        """Wrapped variant of the floor division method"""
        return map_binary_function(lambda x, y: (x // y)%127, left, right)

    def name_disamb(self, name):
        """Generating a name"""
        # Fix two letters words with b being interpreted as words
        if name in ["Ab", "Bb", "Cb", "Db", "Eb", "Fb", "Gb"]:
            # We need to return in two separate tokens
            # See make_note
            return self.make_note(name[0], name[1])
        return str(name)

    def name_from_name_number(self, name, number):
        return str("".join([str(name), str(number)]))

    def assoc_sp_number(self, name, value):
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

    def choice_name(self, a, b):
        """Choose 50%/50% between name 'a' and name 'b'.

        Args:
            a (str): A name
            b (str): A name

        Returns:
            str: The name chosen by a chance operation
        """
        return random.choice([a, b])

    def repeat_name(self, name, value):
        """Repeats a name 'value' times.

        Args:
            name (str): A name given as a string
            value (_type_): Number of repetitions

        Returns:
            list[str]: A list composed of 'value' times the 'name'.
        """
        return [name] * int(value)

    def cosinus(self, x):
        return map_unary_function(cos, x)

    def sinus(self, x):
        return map_unary_function(sin, x)

    def tangente(self, x):
        return map_unary_function(tan, x)
