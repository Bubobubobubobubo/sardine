from lark import Lark, Transformer, v_args, Tree
from itertools import cycle, islice, count, chain
from pathlib import Path
import random

__all__ = ("ListParser", "Pnote", "Pname", "Pnum")


class ParserError(Exception):
    pass


qualifiers = {
    "dim": [0, 3, 6, 12],
    "dim9": [0, 3, 6, 9, 14],
    "hdim7": [0, 3, 6, 10],
    "hdim9": [0, 3, 6, 10, 14],
    "hdimb9": [0, 3, 6, 10, 13],
    "dim7": [0, 3, 6, 9],
    "7dim5": [0, 4, 6, 10],
    "aug": [0, 4, 8, 12],
    "augMaj7": [0, 4, 8, 11],
    "aug7": [0, 4, 8, 10],
    "aug9": [0, 4, 10, 14],
    "maj": [0, 4, 7, 12],
    "maj7": [0, 4, 7, 11],
    "maj9": [0, 4, 11, 14],
    "minmaj7": [0, 3, 7, 11],
    "5": [0, 7, 12],
    "6": [0, 4, 7, 9],
    "7": [0, 4, 7, 10],
    "9": [0, 4, 10, 14],
    "b9": [0, 4, 10, 13],
    "mM9": [0, 3, 11, 14],
    "min": [0, 3, 7, 12],
    "min7": [0, 3, 7, 10],
    "min9": [0, 3, 10, 14],
    "sus4": [0, 5, 7, 12],
    "sus2": [0, 2, 7, 12],
    "b5": [0, 4, 6, 12],
    "mb5": [0, 3, 6, 12],
    # Scales begin here
    # Based on a very partial list found here:
    # https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "hminor": [0, 2, 3, 5, 7, 8, 11],
    "^minor": [0, 2, 3, 5, 7, 9, 11],  # doesn't work
    "vminor": [0, 2, 3, 5, 7, 8, 10],
    "penta": [0, 2, 4, 7, 9],
    "acoustic": [0, 2, 4, 6, 7, 9, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "algerian": [0, 2, 3, 6, 7, 9, 11, 12, 14, 15, 17],
    "superlocrian": [0, 1, 3, 4, 6, 8, 10],
    "augmented": [0, 3, 4, 7, 8, 11],
    "bebop": [0, 2, 4, 5, 7, 9, 10, 11],
    "blues": [0, 3, 5, 6, 7, 10],
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "double-harmonic": [0, 1, 4, 5, 8, 11],
    "enigmatic": [0, 1, 4, 6, 8, 10, 11],
    "flamenco": [0, 1, 4, 5, 7, 8, 11],
    "gypsy": [0, 2, 3, 6, 7, 8, 10],
    "halfdim": [0, 2, 3, 5, 6, 8, 10],
    "harm-major": [0, 2, 4, 5, 7, 8, 11],
    "harm-minor": [0, 2, 3, 5, 7, 8, 11],
    "hirajoshi": [0, 4, 6, 7, 11],
    "hungarian-minor": [0, 2, 3, 6, 7, 8, 11],
    "hungarian-major": [0, 3, 4, 6, 7, 9, 10],
    "in": [0, 1, 5, 7, 8],
    "insen": [0, 1, 5, 7, 10],
    "ionian": [0, 2, 4, 5, 7, 9, 11],
    "istrian": [0, 1, 3, 4, 6, 7],
    "iwato": [0, 1, 5, 6, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    "lydian-augmented": [0, 2, 4, 6, 8, 9, 11],
    "lydian": [0, 2, 4, 5, 7, 8, 9, 11],
    "major-locrian": [0, 2, 4, 5, 6, 8, 10],
    "major-penta": [0, 2, 4, 7, 9],
    "melodic-minor-ascending": [0, 2, 3, 5, 7, 9, 11],
    "melodic-minor-descending": [0, 2, 3, 5, 7, 8, 10],
    "minor-penta": [0, 3, 5, 7, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "neapolitan": [0, 1, 3, 5, 7, 8, 11],
    "octatonic": [0, 2, 3, 5, 6, 8, 9, 11],
    "octatonic2": [0, 1, 3, 4, 6, 7, 9, 10],
    "persian": [0, 1, 4, 5, 6, 8, 11],
    "phrygian": [0, 1, 4, 5, 7, 8, 10],
    "prometheus": [0, 2, 4, 6, 9, 10],
    "harmonics": [0, 3, 4, 5, 7, 9],
    "tritone": [0, 1, 4, 6, 7, 10],
    "two-semitone": [0, 1, 2, 6, 7, 8],
    "ukrainian": [0, 2, 3, 6, 7, 9, 10],
    "whole": [0, 2, 4, 6, 8, 10],
    "yo": [0, 3, 5, 7, 10],
    "symetrical": [0, 1, 2, 6, 7, 10],
    "symetrical2": [0, 2, 3, 6, 8, 10],
    "messiaen1": [0, 2, 4, 6, 8, 10],
    "messiaen2": [0, 1, 3, 4, 6, 7, 9, 10],
    "messiaen3": [0, 2, 3, 4, 6, 7, 8, 10, 11],
    "messiaen4": [0, 1, 2, 4, 6, 7, 8, 11],
    "messiaen5": [0, 1, 5, 6, 7, 11],
    "messiaen6": [0, 2, 4, 5, 6, 8],
    "messiaen7": [0, 1, 2, 3, 5, 6, 7, 8, 9, 11],
    # Structures (other musical objects)
    "fourths": [0, 4, 10, 15, 20],
    "fifths": [0, 7, 14, 21, 28],
    "sixths": [0, 9, 17, 26, 35],
    "thirds": [0, 4, 8, 12],
    "octaves": [0, 12, 24, 36, 48],
}


def floating_point_range(start, end, step):
    assert step != 0
    sample_count = int(abs(end - start) / step)
    return islice(count(start, step), sample_count)


@v_args(inline=True)  # Affects the signatures of the methods
class CalculateTree(Transformer):
    number = float

    # ---------------------------------------------------------------------- #
    # Notes: methods used by the note-specific parser
    # ---------------------------------------------------------------------- #

    def random_note(self):
        """Generates a random MIDI Note in the range 1 - 127.

        Returns:
            int: a random MIDI Note
        """
        return random.randint(1, 127)

    def random_note_in_range(self, number0, number1):
        """Generates a random MIDI Note in the range number0 - number1.

        Args:
            number0 (int):  low boundary
            number1 (int): high boundary

        Returns:
            int: a random MIDI Note.
        """
        return random.randint(int(number0), int(number1))

    def make_note_anglo_saxon(self, symbol):
        """Return a valid MIDI Note (fifth octave)
        from a valid anglo-saxon note name.

        Args:
            symbol (str): a string representing a valid note (a to g).

        Returns:
            int: A MIDI Note (fifth octave)
        """
        table = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}
        return table[symbol.upper()]

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
        match_table = {60: 0, 62: 2, 64: 4, 65: 5, 67: 7, 69: 9, 71: 11}
        return match_table[note] + 12 * int(number)

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
        return [note + x for x in qualifiers[str(quali)]]

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
        collection.reverse()
        return collection

    def collection_palindrome(self, collection):
        """Make a palindrome out of a newly generated collection

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: palindromed list of integers from qualifier's based collection
        """
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
            list: A list of integers with the second and fourth note dropped an octave.
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
        return list(args)

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
            return new_list

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
        if isinstance(value, float):
            return -value
        elif isinstance(value, list):
            return [-x for x in value]

    def addition(self, left, right):
        if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
            return left + right
        elif all(map(lambda x: isinstance(x, list), [left, right])):
            return [x + y for x, y in zip(cycle(right), left)]
        elif isinstance(left, (int, float)) and isinstance(right, list):
            return [x + left for x in right]
        elif isinstance(left, list) and isinstance(right, (float, int)):
            return [x + right for x in left]

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

    def name(self, name):
        return str(name)

    def make_integer(self, value):
        return int(value)

    def name_from_number_name(self, number, name):
        return str("".join([str(number), str(name)]))

    def name_from_name_number(self, name, number):
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
grammars = {
    "number": grammar_path / "grammars/number.lark",
    "name": grammar_path / "grammars/name.lark",
    "note": grammar_path / "grammars/note.lark",
}

parsers = {
    "number": {
        "raw": Lark.open(
            grammars["number"],
            rel_to=__file__,
            parser="lalr",
            start="start",
            cache=True,
            lexer="contextual",
        ),
        "full": Lark.open(
            grammars["number"],
            rel_to=__file__,
            parser="lalr",
            start="start",
            cache=True,
            lexer="contextual",
            transformer=CalculateTree(),
        ),
    },
    "name": {
        "raw": Lark.open(
            grammars["name"],
            rel_to=__file__,
            parser="lalr",
            start="start",
            cache=True,
            lexer="contextual",
        ),
        "full": Lark.open(
            grammars["name"],
            rel_to=__file__,
            parser="lalr",
            start="start",
            cache=True,
            lexer="contextual",
            transformer=CalculateTree(),
        ),
    },
    "note": {
        "raw": Lark.open(
            grammars["note"],
            rel_to=__file__,
            parser="lalr",
            start="start",
            cache=True,
            lexer="contextual",
        ),
        "full": Lark.open(
            grammars["note"],
            rel_to=__file__,
            parser="lalr",
            start="start",
            cache=True,
            lexer="contextual",
            transformer=CalculateTree(),
        ),
    },
}


class ListParser:
    def __init__(self, parser_type: str = "number"):
        """
        Initialise two different parsers:
        - result_parser: the parser used to generate patterns
        - printing_parser: the parser used for debugging purposes
        """
        try:
            self._result_parser = parsers[parser_type]["full"]
            self._printing_parser = parsers[parser_type]["raw"]
        except KeyError:
            ParserError(f"Invalid Parser grammar, {parser_type} is not a grammar.")

    def _flatten_result(self, pat):
        """Flatten a nested pattern result list. Probably not optimised."""
        if len(pat) == 0:
            return pat
        if isinstance(pat[0], list):
            return self._flatten_result(pat[0]) + self._flatten_result(pat[1:])
        return pat[:1] + self._flatten_result(pat[1:])

    def pretty_print(self, expression: str):
        """Pretty print an expression from parser"""
        print(f"EXPR: {expression}")
        print(Tree.pretty(self._printing_parser.parse(expression)))
        print(f"RESULT: {self._result_parser.parse(expression)}")

    def print_tree_only(self, expression: str):
        """Print only tree for debugging purposes"""
        print(Tree.pretty(self._printing_parser.parse(expression)))

    def _parse_token(self, string: str):
        """Parse a single token and return the result for usage"""
        return self._result_parser.parse(string)

    def parse(self, pattern: str):
        """Parse a whole pattern and return a flattened list"""
        final_pattern = []
        for token in pattern.split():
            try:
                final_pattern.append(self._parse_token(token))
            except Exception as e:
                raise ParserError(f"Non valid token: {token}") from e
        return self._flatten_result(final_pattern)

    def _parse_debug(self, pattern: str):
        """Parse a whole pattern in debug mode"""
        final_pattern = []
        for token in pattern.split():
            try:
                self.pretty_print(expression=token)
            except Exception as e:
                import traceback

                print(f"Error: {e}: {traceback.format_exc()}")
                continue


# Useful utilities


def Pname(pattern: str, i: int = 0):
    parser = ListParser(parser_type="name")
    pattern = parser.parse(pattern)
    return pattern[i % len(pattern)]


def Pnote(pattern: str, i: int = 0):
    parser = ListParser(parser_type="note")
    pattern = parser.parse(pattern)
    return pattern[i % len(pattern)]


def Pnum(pattern: str, i: int = 0):
    parser = ListParser(parser_type="number")
    pattern = parser.parse(pattern)
    return pattern[i % len(pattern)]
