from lark import Transformer, v_args
from .Qualifiers import qualifiers
from lark.lexer import Token
from typing import Any
from itertools import cycle
from time import time
import random


@v_args(inline=True)
class CalculateTree(Transformer):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock
        self.memory = {}

    def number(self, number):
        return float(number)

    def negative_number(self, number):
        return -float(number)

    def return_pattern(self, *args):
        return list(args)

    # ---------------------------------------------------------------------- #
    # Lists: methods concerning lists
    # ---------------------------------------------------------------------- #

    def list_addition(self, left, right):
        def solve_addition(left, right):
            if all(map(lambda x: isinstance(x, (int, float)), [left, right])):
                return left + right
            elif all(map(lambda x: isinstance(x, list), [left, right])):
                return [x + y for x, y in zip(cycle(right), left)]
            elif all(map(lambda x: isinstance(x, str), [left, right])):
                return "".join([right, left])

        return [solve_addition(x, y) for x, y in zip(cycle(right), left)]

    def list_substraction(self, left, right):
        def solve_substraction(left, right):
            if all(map(lambda x: isinstance(x, (int, float)), [left, right])):
                return left - right
            elif all(map(lambda x: isinstance(x, list), [left, right])):
                return [x - y for x, y in zip(cycle(right), left)]
            elif all(map(lambda x: isinstance(x, str), [left, right])):
                new_string = []
                for _ in right:
                    if _ not in left:
                        new_string.append(_)
                return "".join(new_string)

        return [solve_substraction(x, y) for x, y in zip(cycle(right), left)]

    def list_modulo(self, left, right):
        def solve_modulo(left, right):
            if all(map(lambda x: isinstance(x, (int, float)), [left, right])):
                return left % right
            elif all(map(lambda x: isinstance(x, list), [left, right])):
                return [x % y for x, y in zip(cycle(right), left)]
            elif all(map(lambda x: isinstance(x, str), [left, right])):
                return None

        return [solve_modulo(y, x) for x, y in zip(cycle(right), left)]

    def list_multiplication(self, left, right):
        def solve_multiplication(left, right):
            if all(map(lambda x: isinstance(x, (int, float)), [left, right])):
                return left * right
            elif all(map(lambda x: isinstance(x, list), [left, right])):
                return [x * y for x, y in zip(cycle(right), left)]
            elif all(map(lambda x: isinstance(x, str), [left, right])):
                return left

        return [solve_multiplication(y, x) for x, y in zip(cycle(right), left)]

    def list_floor_division(self, left, right):
        def solve_floor_division(left, right):
            if all(map(lambda x: isinstance(x, (int, float)), [left, right])):
                return left // right
            elif all(map(lambda x: isinstance(x, list), [left, right])):
                return [x // y for x, y in zip(cycle(right), left)]
            elif all(map(lambda x: isinstance(x, str), [left, right])):
                return None

        return [solve_floor_division(y, x) for x, y in zip(cycle(right), left)]

    def list_choice(self, left, right):
        """Choose between two lists"""
        return self.choice_note(left, right)

    def list_extend(self, left, right):
        """Copy of the extend rule"""
        return self.extend(left, right)

    def list_extend_repeat(self, left, right):
        """Probably not the right behavior"""
        return self.extend_repeat(left, right)

    def list_negation(self, collection):
        """Will apply a negative sign when possible to list"""
        return list(map(lambda x: -x if isinstance(x, (int, float)) else x, collection))

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

    def make_note(self, symbol):
        """Return a valid MIDI Note (fifth octave)
        from a valid anglo-saxon note name.

        Args:
            symbol (str): a string representing a valid note (a to g).

        Returns:
            int: A MIDI Note (fifth octave)
        """
        table = {"A": 57, "B": 59, "C": 60, "D": 62, "E": 64, "F": 65, "G": 67}
        return table[str(symbol).upper()]

    def make_note_french_system(self, symbol):
        """Return a valid MIDI Note (fifth octave)
        from a valid french note name.

        Args:
            symbol (str): a string representing a valid note (do to si)

        Returns:
            int: A MIDI Note (fifth octave)
        """
        table = {
            "do": 60,
            "re": 62,
            "ré": 62,
            "mi": 64,
            "fa": 65,
            "sol": 67,
            "la": 69,
            "si": 71,
        }
        return table[symbol]

    def add_octave(self, note, number):
        """Given a note, transpose it up to the given octave

        Args:
            note (int): a MIDI note (0-127)
            number (int): octave number

        Returns:
            int: A valid MIDI Note at given octave
        """
        return (int(note) - 12 * 5) + 12 * int(number)

    def sharp_simple(self, note):
        """Sharpen a note

        Args:
            note (int): A MIDI Note

        Returns:
            int: A sharpened MIDI Note (note+1)
        """
        return note + 1

    def flat_simple(self, note):
        """Flatten a note

        Args:
            note (int): A MIDI Note

        Returns:
            int: A flattened MIDI Note (note-1)
        """
        return note - 1

    def sharp_octave(self, note, number):
        """Combination of preceding functions for sharp + octaviated note

        Args:
            note (int): A MIDI Note
            number (int): An octave from 0 to 9

        Returns:
            int: A sharpened and octaviated MIDI Note
        """
        match_table = {60: 0, 62: 2, 64: 4, 65: 5, 67: 7, 69: 9, 71: 11}
        return match_table[note] + 12 * int(number) + 1

    def flat_octave(self, note, number):
        """Combination of preceding functions for flat + octaviated note

        Args:
            note (int): A MIDI Note
            number (int): An octave from 0 to 9

        Returns:
            int: A flattened and octaviated MIDI Note
        """
        match_table = {60: 0, 62: 2, 64: 4, 65: 5, 67: 7, 69: 9, 71: 11}
        return match_table[note] + 12 * int(number) - 1

    def choice_note(self, note0, note1):
        """Choose 50%/50% between two notes

        Args:
            note0 (int): A MIDI Note
            note1 (int): An other MIDI Note

        Returns:
            int: The chosen MIDI Note
        """
        return random.choice([note0, note1])

    def repeat_note(self, note, number):
        """Turn a note into a list of 'number' times 'note.

        Args:
            note (int): A MIDI Note
            number (int): Number of repetitions

        Returns:
            list: A list of the same note repeated 'number' times.
        """
        return [note] * int(number)

    def drop_octave(self, note):
        """Drop the note an octave down

        Args:
            note (int): A MIDI Note

        Returns:
            int: A MIDI Note
        """
        return note - 12

    def raise_octave(self, note):
        """Raise the note an octave up

        Args:
            note (int): A MIDI Note

        Returns:
            int: A MIDI Note
        """
        return note + 12

    def drop_octave_x(self, note, number):
        """Drop a note 'x' octaves down

        Args:
            note (int): A MIDI Note
            number (int): Number of octaves to drop

        Returns:
            int: A MIDI Note
        """
        return note - 12 * int(number)

    def raise_octave_x(self, note, number):
        """Raise a note 'x' octaves up

        Args:
            note (int): A MIDI Note
            number (int): Number of octaves to raise

        Returns:
            int: A MIDI Note
        """
        return note + 12 * int(number)

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

    def transpose_up(self, notes, number):
        """Transpose a note 'number' notes up.

        Args:
            notes (int): A MIDI Note_
            number (int): Transposition factor

        Returns:
            int: A MIDI Note
        """
        return notes + int(number)

    def transpose_down(self, notes, number):
        """Transpose a note 'number' notes down

        Args:
            notes (int): A MIDI Note
            number (int): Transposition factor

        Returns:
            int: A MIDI Note
        """
        return notes - int(number)

    def make_number(self, *token):
        """Turn a number from string to integer. Used by the parser,
        transform a token matched as a string to a number before
        applying other rules.

        Returns:
            int: an integer
        """
        return int("".join(token))

    def slash_chord(self, note0, note1):
        """Build a list from two notes as if it was a slashed chord.
        Used for cosmetic purposes (more easy to read for the user).

        Args:
            note0 (int): A MIDI Note
            note1 (int): A MIDI Note

        Returns:
            int: A MIDI Note
        """
        note0, note1 = [note0], [note1]
        return note0.extend(note1)

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
            collection.reverse()
            return collection

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
            collection.reverse()
            return collection + list(reversed(collection))

    def shuffle_collection(self, collection):
        """Shuffle a newly generated collection

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: A shuffled list of integers
        """
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

        return [expand_number(x) for x in collection]

    def disco_collection(self, collection):
        """Takes every other note down an octave

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: A list of integers
        """
        applier = cycle([lambda x: x - 12, lambda x: self.id(x)])
        return [next(applier)(x) for x in collection]

    def repeat_collection(self, collection, number):
        """Repeats a list 'number' times

        Args:
            collection (list): A list generated through a qualifier
            number (int): Number of repetitions

        Returns:
            list: Repeated list of integers
        """
        final_list = []
        for list in [collection] * int(number):
            final_list.extend(list)
        return final_list

    def repeat_collection_x(self, collection, number):
        """See grammar file for better understanding"""
        return self.repeat_collection(collection, number)

    def add_collection(self, collec0, collec1):
        """Addition between two lists (symetrical or asymetrical).
        The longest list will take precedence and thus the result
        will yield a list of the length of the longest list. Additions
        are performed cyclically until the index of the longest list is
        reached.

        Args:
            collec0 (list): A list of integeers
            collec1 (list): A list of integers

        Returns:
            list: A list of additioned integers
        """
        if isinstance(collec1, (int, float)):
            return [x + collec1 for x in collec0]
        longest, list = max(len(collec0), len(collec1)), []
        collec0, collec1 = cycle(collec0), cycle(collec1)
        for _ in range(longest):
            list.append(next(collec0) + next(collec1))
        return list

    def sub_collection(self, collec0, collec1):
        """Substraction between two lists (symetrical or asymetrical).
        The longest list will take precedence and thus the result
        will yield a list of the length of the longest list. Substractions
        are performed cyclically until the index of the longest list is
        reached.

        Args:
            collec0 (list): A list of integeers
            collec1 (list): A list of integers

        Returns:
            list: A list of additioned integers
        """
        if isinstance(collec1, (int, float)):
            return [x - collec1 for x in collec0]

        longest, list = max(len(collec0), len(collec1)), []
        collec0, collec1 = cycle(collec0), cycle(collec1)
        for _ in range(longest):
            list.append(next(collec0) - next(collec1))
        return list

    def collection_drop2(self, collection):
        """Simulate a drop2 chord.

        Args:
            collection (list): A list of integers

        Returns:
            list: A list of integers with the second note dropped an octave.
        """
        collection[1] = collection[1] - 12
        return collection

    def collection_drop3(self, collection):
        """Simulate a drop3 chord.

        Args:
            collection (list): A list of integers

        Returns:
            list: A list of integers with the third note dropped an octave.
        """
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
                for i in element:
                    new_list.append(i)
            else:
                new_list.append(element)
        return new_list

    def make_list_gen(self, gen):
        """Make a list from a generator (un-nest it)

        Returns:
            list: Generator turned into a list
        """
        return gen

    def get_time(self):
        """Return current clock time (tick) as integer"""
        return int(self.clock.tick)

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
        if int(left) > int(right):
            new_list = list(reversed(range(int(right), int(left) + 1)))
            return new_list
        else:
            return list(range(int(left), int(right) + 1))

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
        if int(left) > int(right):
            new_list = list(reversed(range(int(right), int(left) + 1, int(step))))
            return new_list
        else:
            return list(range(int(left), int(right) + 1, int(step)))

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
        if isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return [left] * int(right)

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
                new_list = []
                cycling_through = cycle(right)
                for element in left:
                    for _ in range(int(next(cycling_through))):
                        new_list.append(element)
                return new_list

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
        if all(map(lambda x: isinstance(x, float), [left, right])):
            return random.uniform(left, right)
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [random.uniform(x, y) for x, y in zip(cycle(right), left)]

    def negation(self, value):
        if isinstance(value, (float, int)):
            return -value
        elif isinstance(value, list):
            return [-x for x in value]

    def concat(self, left, operator, right):
        """List Concatenation: takes a list and extends it with
        another list. Used by proto parser.

        Args:
            left (list): The initial list
            right (list): The list to concatenate

        Results
            list: One list of of two
        """

        if isinstance(left, list):
            if isinstance(right, list):
                left.extend(right)
                return left
            if isinstance(right, (float, int)):
                left.extend([right])
                return left
        if isinstance(left, (int, float)):
            if isinstance(right, list):
                [left].extend(right)
                return left
            if isinstance(right, (float, int)):
                return [left, right]

    def addition(self, left, right):
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            return left + right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x + y for x, y in zip(cycle(right), left)]
        elif isinstance(left, (int, float)) and isinstance(right, list):
            return [x + left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x + right for x in left]

    def modulo(self, left, right):
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            return left % right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x % y for x, y in zip(cycle(right), left)]
        elif isinstance(left, (int, float)) and isinstance(right, list):
            return [x % left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x % right for x in left]

    def power(self, left, right):
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            return pow(left, right)
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [pow(x, y) for x, y in zip(cycle(right), left)]
        elif isinstance(left, (int, float)) and isinstance(right, list):
            return [pow(left, x) for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [pow(right, x) for x in left]

    def substraction(self, left, right):
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            return left - right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x - y for x, y in zip(cycle(right), left)]
        elif isinstance(left, (int, float)) and isinstance(right, list):
            return [x - left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x - right for x in left]

    def multiplication(self, left, right):
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            return left * right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x * y for x, y in zip(cycle(right), left)]
        if isinstance(left, (int, float)) and isinstance(right, list):
            return [x * left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x * right for x in left]

    def division(self, left, right):
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            return left / right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x / y for x, y in zip(cycle(right), left)]
        if isinstance(left, (int, float)) and isinstance(right, list):
            return [x / left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x / right for x in left]

    def floor_division(self, left, right):
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            return left // right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x // y for x, y in zip(cycle(right), left)]
        if isinstance(left, (int, float)) and isinstance(right, list):
            return [x // left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x // right for x in left]

    def name_disamb(self, name):
        """Generating a name"""
        # Fix two letters words with b being interpreted as words
        if name in ["Ab", "Bb", "Cb", "Db", "Eb", "Fb", "Gb"]:
            return self.flat_simple(self.make_note(symbol=name[0]))
        return str(name)

    def make_integer(self, value):
        return int(value)

    def name_from_number_name(self, number, name):
        return str("".join([str(number), str(name)]))

    def name_from_name_number(self, name, number):
        return str("".join([str(name), str(number)]))

    def association(self, name, value):
        """Associate a name to a value in memory"""
        self.memory[name] = value

    def recover_variable(self, name):
        """Recover a variable that has been stored in memory"""
        if name in self.memory.keys():
            return self.memory[name]
        else:
            return None

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

    def add_name(self, a, b):
        return a + b

    def times_name(self, a, b):
        return a * int(b)

    def sub_name(self, a, b):
        """Substraction of a name by a name. Every letter present
        in name 'b' will be substracted from name 'a'.

        Args:
            a (str): A name
            b (str): A name

        Returns:
            str: A Substracted name.
        """
        return a.replace(b, "")

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
