import random
import statistics
from itertools import chain, cycle, islice
from math import cos, sin, tan, asin, pi, atan
from random import shuffle
from typing import Optional, Union
from time import time
import datetime

from ..sequence import euclid
from .chord import Chord
from .utils import map_binary_function, map_unary_function

# Type declarations


class FunctionLibrary:
    qualifiers = {
        "dim": [0, 3, 6, 12],
        "dim9": [0, 3, 6, 9, 14],
        "hdim7": [0, 3, 6, 10],
        "hdim9": [0, 3, 6, 10, 14],
        "hdimb9": [0, 3, 6, 10, 13],
        "dim7": [0, 3, 6, 9],
        "aug": [0, 4, 8, 12],
        "augMaj7": [0, 4, 8, 11],
        "aug7": [0, 4, 8, 10],
        "aug9": [0, 4, 10, 14],
        "maj": [0, 4, 7, 12],
        "maj7": [0, 4, 7, 11],
        "maj9": [0, 4, 11, 14],
        "minmaj7": [0, 3, 7, 11],
        "five": [0, 7, 12],
        "six": [0, 4, 7, 9],
        "seven": [0, 4, 7, 10],
        "nine": [0, 4, 10, 14],
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
        "doubleharmonic": [0, 1, 4, 5, 8, 11],
        "enigmatic": [0, 1, 4, 6, 8, 10, 11],
        "flamenco": [0, 1, 4, 5, 7, 8, 11],
        "gypsy": [0, 2, 3, 6, 7, 8, 10],
        "halfdim": [0, 2, 3, 5, 6, 8, 10],
        "harmmajor": [0, 2, 4, 5, 7, 8, 11],
        "harmminor": [0, 2, 3, 5, 7, 8, 11],
        "hirajoshi": [0, 4, 6, 7, 11],
        "hungarianminor": [0, 2, 3, 6, 7, 8, 11],
        "hungarianmajor": [0, 3, 4, 6, 7, 9, 10],
        "in": [0, 1, 5, 7, 8],
        "insen": [0, 1, 5, 7, 10],
        "ionian": [0, 2, 4, 5, 7, 9, 11],
        "istrian": [0, 1, 3, 4, 6, 7],
        "iwato": [0, 1, 5, 6, 10],
        "locrian": [0, 1, 3, 5, 6, 8, 10],
        "lydianaug": [0, 2, 4, 6, 8, 9, 11],
        "lydian": [0, 2, 4, 5, 7, 8, 9, 11],
        "majorlocrian": [0, 2, 4, 5, 6, 8, 10],
        "majorpenta": [0, 2, 4, 7, 9],
        "melominup": [0, 2, 3, 5, 7, 9, 11],
        "minorpenta": [0, 3, 5, 7, 10],
        "melomindown": [0, 2, 3, 5, 7, 8, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "neapolitan": [0, 1, 3, 5, 7, 8, 11],
        "octatonic": [0, 2, 3, 5, 6, 8, 9, 11],
        "octatonic2": [0, 1, 3, 4, 6, 7, 9, 10],
        "persian": [0, 1, 4, 5, 6, 8, 11],
        "phrygian": [0, 1, 4, 5, 7, 8, 10],
        "prometheus": [0, 2, 4, 6, 9, 10],
        "harmonics": [0, 3, 4, 5, 7, 9],
        "tritone": [0, 1, 4, 6, 7, 10],
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

    def __init__(self, clock, amphibian, inner_variables, global_scale):
        self.clock = clock
        self.amphibian = amphibian
        self.inner_variables = inner_variables
        self.global_scale = global_scale

    # ============================================================================ #
    # Dmitri Tymoczko algorithm
    # ============================================================================ #

    def dmitri_tymoczko_algorithm(self, collection: list, chord_len: int = 4) -> list:
        def octave_transform(input_chord, root):
            """
            Squish things into a single octave for comparison between chords and
            sort from lowest to highest.
            """
            result = sorted(list(map(lambda x: root + (x % 12), input_chord)))
            return result

        def t_matrix(chord_a, chord_b):
            """Get the distance between notes"""
            root = chord_a[0]
            return [
                j - i
                for i, j in zip(
                    octave_transform(chord_a, root), octave_transform(chord_b, root)
                )
            ]

        def voice_lead(chord_a, chord_b):
            """
            Get mapping of notes in chord a to the sorted version of the chord a
            """
            root = chord_a[0]
            a = list(
                map(
                    lambda x: [
                        x,
                        octave_transform(chord_a, root).index(root + (x % 12)),
                    ],
                    chord_a,
                )
            )
            t = t_matrix(chord_a, chord_b)
            chord_x = (x[0] for x in a)
            chord_y = (x[1] for x in a)
            b_voicing = list(map(lambda x, y: x + t[y], chord_x, chord_y))
            return b_voicing

        def _slice_collection(collection: list, slice_size=chord_len) -> list:
            """Slice a collection in chunks of length n"""
            return [
                collection[i : i + slice_size]
                for i in range(0, len(collection), slice_size)
            ]

        # Now for the part where we can take a list of x chords and voice them.
        chords = _slice_collection(collection)

        for i in range(len(chords) - 1):
            # print(f"Première passe: {chords}")
            chords[i + 1] = voice_lead(chords[i], chords[i + 1])

        chords[-1] = voice_lead(chords[-2], chords[-1])

        return chords

    def dmitri(self, collection: list, chord_len: list = [4], **kwargs) -> list:
        voiced = self.dmitri_tymoczko_algorithm(collection, chord_len[0])
        return voiced

    def chordify(self, *x) -> list:
        """Turn a list into a chord"""
        return Chord(*x)

    def beat(self, *args, **kwargs) -> list:
        """Return True if we are on the desired beat. Multiple beats are supported"""
        return (
            [1]
            if int(self.clock.beat % self.clock.beats_per_bar)
            in list(map(lambda x: int(x), list(chain(*args))))
            else [0]
        )

    def phase(self, x: list, y: list, **kwargs) -> list:
        """Return True if phase is in between x and y else False"""
        tolerance = 0.01
        return [1] if x[0] + tolerance <= self.clock.phase <= y[0] - tolerance else [0]

    def oddbar(self, *args, **kwargs) -> list:
        """Return True if the current bar is odd, false otherwise"""
        return [1] if self.clock.bar % 2 != 0 else [0]

    def modbar(self, modulo, *args, **kwargs) -> list:
        """Return True if modulo of bar against current bar is true"""
        return [1] if self.clock.bar % modulo[0] == 0 else [0]

    def evenbar(self, *args, **kwargs) -> list:
        """Return True if the current bar is even, false otherwise"""
        return [1] if self.clock.bar % 2 == 0 else [0]

    def dice(self, choice: list, faces: list, *args, **kwargs) -> list:
        """Simulation of a dice"""
        return random.randint(1, faces[0]) == choice[0]

    def every(self, *args, **kwargs):
        """
        Inspired by the 'every' function in TidalCycles. Will return True if the
        current bar is the modulo of the targetted bar, false otherwise. Multiple
        arguments are allowed (is it even useful?)
        """

        def inner_function(x) -> list:
            modulo_operation = (int(self.clock.bar) % x[0]) + 1
            return [1] if modulo_operation == x[0] else [0]

        results = []

        for _ in args:
            if inner_function(_) == [1]:
                results.append(True)
            else:
                results.append(False)

        return [1] if True in results else [0]

    def binary_condition(self, condition, pattern_a=[None], pattern_b=[None], **kwargs):
        """If the condition is True, play pattern A, else play pattern B"""
        return pattern_a if condition[0] >= 1 else pattern_b

    def negative_binary_condition(
        self, condition, pattern_a=[None], pattern_b=[None], **kwargs
    ):
        """If the condition is True, play pattern A, else play pattern B"""
        return pattern_b if condition[0] >= 1 else pattern_a

    def unary_condition(self, condition, pattern=[None], **kwargs):
        """While loop that returns nothing is the condition is not met"""
        return pattern if condition[0] >= 1 else [None]

    def in_condition(self, test_value, condition, **kwargs):
        """Return something from the pattern if the condition is met"""
        value = int(test_value[0])
        condition_list = list(map(lambda x: int(x), condition))
        print(f"Testing if {value} in {condition_list}")
        return [1] if value in condition_list else [0]

    def negative_unary_condition(self, condition, pattern=[None], **kwargs):
        """Do something only if the condition is not True"""
        return pattern if condition != [1] else [None]

    def set_variable(self, *args, **kwargs):
        """Set an internal variable to the given value and return the same value"""
        self.inner_variables[str(args[0][0])] = args[1]
        return args[1]

    def get_variable(self, *args, **kwargs):
        """Get an internal variable. If it doesn't exist, will return 0"""
        return self.inner_variables.get(args[0][0], [0])

    def get_amphibian_variable(self, *args, **kwargs):
        """
        Return the value of an amphibian variable coming from the Python
        side. The result can only be an int, a float or a string. The
        final result is always assumed to be a list.
        """
        reset = kwargs.get("reset", 0)

        if reset == 0:
            self.amphibian.reset(str(str(args[0])))
            return [getattr(self.amphibian, str(args[0][0]))]
        else:
            return [getattr(self.amphibian, str(args[0][0]))]

    def set_amphibian_variable(self, *args):
        """
        Set an amphibian variable to a new value. This value can be of any
        type supported internally by the Sardine pattern language. This
        function will return the new-set value.
        """
        setattr(self.amphibian, str(args[0][0]), args[1])
        return [getattr(self.amphibian, str(args[1][0]))]

    def drunk(self, *args, **kwargs):
        """
        Drunk walk: 50% chance +1, 50% chance -1.
        The span argument will make it possible to
        jump from +/- the given span, randomly.
        """
        span = kwargs.get("span", None)
        if span:
            random_span = random.randint(0, span[0])
        else:
            random_span = 1

        args = list(chain(*args))

        def drunk(number):
            random_factor = random.random()
            return number + random_span if random_factor > 0.5 else number - random_span

        return map_unary_function(drunk, args)

    def anti_speed(self, *args, **kwargs) -> list:
        """Adds one silence per element in the list"""
        args = list(chain(*args))
        list_of_silences = [[None] * x for x in range(0, len(args))]
        return list(zip(args, list_of_silences))

    def proba(self, x: list, **kwargs) -> list:
        """Probability of returning True or False"""
        return [1] if random.random() * 100 <= x[0] else [0]

    def invert(self, x: list, how_many: list = [0], **kwargs) -> list:
        """Chord inversion algorithm"""
        x = list(reversed(x)) if how_many[0] < 0 else x
        for _ in range(abs(how_many[0])):
            x[_ % len(x)] += -12 if how_many[0] <= 0 else 12
        return x

    def _remap(self, x, in_min, in_max, out_min, out_max):
        """Remapping a value from a [x, y] range to a [x', y'] range"""
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def scale(
        self,
        collection: list,
        imin: list,
        imax: list,
        omin: list = [0],
        omax: list = [1],
        **kwargs,
    ) -> list:
        """User-facing scaling function"""
        return list(
            map(
                lambda x: self._remap(x, imin[0], imax[0], omin[0], omax[0]), collection
            )
        )

    def euclidian_to_number(
        self, pulses: list, steps: list, rotation: Optional[list] = [0]
    ) -> list:
        """Convert a 'binary' euclidian rhythm to a number based representation usable by patterns"""
        rhythm = euclid(pulses[0], steps[0], rotation[0])

        def convert(input_list):
            input_list = int("".join([str(i) for i in input_list]))

            def convert_code(number):
                count, result = 0, []
                for digit in str(number):
                    if digit == "1":
                        if count > 0:
                            result.append(count)
                        count = 1
                    elif digit == "0":
                        count += 1
                if count > 0:
                    result.append(count)
                return result

            return convert_code(input_list)

        return convert(rhythm)

    def euclidian_rhythm(
        self,
        collection: list,
        pulses: list,
        steps: list,
        rotation: Optional[list] = [0],
        **kwargs,
    ) -> list:
        """
        Apply an euclidian rhythm as a boolean mask on values from the collection.
        True values will return the value itself, others will return a silence.
        """
        # This one-liner is creating a collection-length euclidian rhythm (repeating the rhythm)
        boolean_mask = list(
            islice(
                cycle(
                    euclid(
                        pulses[0], steps[0], rotation[0] if rotation is not None else 0
                    )
                ),
                len(collection) if len(collection) >= steps[0] else steps[0],
            )
        )
        new_collection = []

        # Masking values
        collection = list(islice(cycle(collection), steps[0]))
        for item, mask in zip(collection, boolean_mask):
            if mask == 1:
                new_collection.append(item)
            else:
                new_collection.append(None)

        return new_collection

    def negative_euclidian_rhythm(
        self,
        collection: list,
        pulses: list,
        steps: list,
        rotation: Optional[list] = None,
        **kwargs,
    ) -> list:
        """
        Apply an euclidian rhythm as a boolean mask on values from the collection.
        True values will return the value itself, others will return a silence.
        """
        # This one-liner is creating a collection-length euclidian rhythm (repeating the rhythm)
        boolean_mask = list(
            islice(
                cycle(
                    euclid(
                        pulses[0], steps[0], rotation[0] if rotation is not None else 0
                    )
                ),
                len(collection) if len(collection) >= steps[0] else steps[0],
            )
        )

        # reversing the euclidian pattern!
        boolean_mask = list(map(lambda x: x ^ 1, boolean_mask))

        new_collection = []

        # Masking values
        collection = list(islice(cycle(collection), steps[0]))
        for item, mask in zip(collection, boolean_mask):
            if mask == 1:
                new_collection.append(item)
            else:
                new_collection.append(None)

        return new_collection

    def find_voice_leading(
        self,
        collection,
        divider: Optional[Union[list, int]] = 4,
    ) -> list:
        """Simple voice leading algorithm"""
        # Splitting the collection with divider
        divider = divider[0] if isinstance(divider, list) else divider

        collection = [
            collection[i : i + divider] for i in range(0, len(collection), divider)
        ]
        root_note = collection[0][0]
        new_progression = []
        for chord in collection:
            new_chord = list(
                map(lambda x: x + 12 * (root_note // 12), [x % 12 for x in chord])
            )
            new_chord.sort()
            new_progression.append(new_chord)
        return new_progression

    def mask(self, collection: list, mask: list, **kwargs) -> list:
        """
        Apply a boolean mask on values from the collection.
        True values will return the value itself, others will
        return a silence.
        """
        invert = kwargs.get("invert", 0)
        invert = True if invert == 1 else False

        if invert:
            for index, _ in enumerate(mask):
                if _ == 1:
                    mask[index] = 0
                if _ == 0:
                    mask[index] = 1

        new_collection = []

        collection = list(islice(cycle(collection), len(mask)))
        for item, mask in zip(collection, mask):
            if mask == 1:
                new_collection.append(item)
            else:
                new_collection.append(None)
        return new_collection

    def clamp(
        self,
        collection: list,
        low_boundary: list,
        high_boundary: list,
        **kwargs,
    ) -> list:
        """
        Simple clamp function, restraining collection to a given range.
        """

        def _work(n, smallest, largest):
            return max(smallest, min(n, largest))

        return list(map(_work, collection, low_boundary, high_boundary))

    def remove_x(self, collection: list, percentage, **kwargs) -> list:
        """
        Replacing x % of the collection by silences
        """
        percentage = len(collection) * percentage[0] // 100
        shuffled_indexes = list(range(0, len(collection)))
        shuffle(shuffled_indexes)
        for _ in range(percentage):
            collection[shuffled_indexes[_]] = [None]
        return collection

    def custom_filter(self, collection: list, elements: list, **kwargs) -> list:
        """Equivalent of the filter function from functional languages..."""

        def cond(thing) -> bool:
            return not thing in elements

        return list(filter(cond, collection))

    def _quantize(self, val, to_values, **kwargs):
        """Quantize a value with regards to a set of allowed values.

        Examples:
            quantize(49.513, [0, 45, 90]) -> 45
            quantize(43, [0, 10, 20, 30]) -> 30

        Note: function doesn't assume to_values to be sorted and
        iterates over all values (i.e. is rather slow).

        Args:
            val        The value to quantize
            to_values  The allowed values
        Returns:
            Closest value among allowed values.

        Taken from: https://gist.github.com/aleju/eb75fa01a1d5d5a785cf
        """
        if val is None:
            return None
        best_match = None
        best_match_diff = None
        for other_val in to_values:
            diff = abs(other_val - val)
            if best_match is None or diff < best_match_diff:
                best_match = other_val
                best_match_diff = diff
        return best_match

    def quantize(self, collection: list, quant_reference: list, **kwargs):
        """
        Quantize function. It takes a collection as left argument and a reference
        to a quantifier or an arbitrary collection as right argument. Will quanti-
        ze to the desired value by building a new list of quantized values taken
        from the collection.
        """

        # Deal with finding the reference
        if len(quant_reference) == 1 and isinstance(quant_reference[0], str):
            try:
                quant_reference = self.qualifiers[quant_reference[0]]
            except KeyError:
                raise KeyError(
                    "Unknown qualifier! Possible quantifiers are: "
                    + f"{', '.join(self.qualifiers)}"
                )

        # Extending the quant_reference to all possible octaves
        initial_extended_reference = (
            12 * i + (x % 12) for x in quant_reference for i in range(0, 11)
        )
        extended_reference = [x for x in set(initial_extended_reference) if x <= 127]

        # Quantization takes place here
        return map_unary_function(
            lambda value: self._quantize(value, extended_reference), collection
        )

    def expand(self, collection: list, factor: list, **kwargs) -> list:
        """
        Chance-based operation. Apply a random octave transposition process
        to every note in a given collection. There is an optional factor
        parameter that multiplies the octave transposition.

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: Chance-expanded list of integers
        """
        factor = factor[0]

        def expand_number(number: Union[int, float]) -> int | float:
            expansions = [0, -12, 12]
            return [number + (random.choice(expansions) * factor)]

        return map_unary_function(expand_number, collection)

    def disco(self, *args, **kwargs) -> list:
        """Takes every other note down an octave

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: A list of integers
        """
        depth = kwargs.get("depth", [1])
        depth = depth[0]
        collection = list(chain(*args))
        offsets = cycle([0, -12 * depth])
        return [
            x + offset if x is not None else None
            for (x, offset) in zip(collection, offsets)
        ]

    def palindrome(
        self,
        *collection,
        **kwargs,
    ) -> list:
        """Make a palindrome out of a newly generated collection

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: palindromed list of integers from qualifier's based
            collection
        """
        collection = list(chain(*collection))
        cut = kwargs.get("cut", None)
        if cut is not None:
            return collection + list(reversed(collection))
        else:
            return collection + list(reversed(collection))[1:]

    def reverse(
        self,
        *collection,
        **kwargs,
    ) -> list:
        """Reverse a newly generated collection.

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: reversed list of integers from qualifier's based collection
        """
        collection = list(chain(*collection))
        return list(reversed(collection))

    def leave(self, *args) -> list:
        """Braid multiple lists of uneven length

        Args:
            collection (list): Lists

        Returns:
            list: An interleaved list
        """
        return list(chain(*zip(*args)))

    def insert_pair(self, collection: list, element: list, **kwargs) -> list:
        """Insert a fixed element as pair element of each list"""
        return [i for x in collection for i in (x, element)][:-1]

    def insert(self, collection: list, element: list, **kwargs) -> list:
        """Insert a fixed element as odd element of each list"""
        return [i for x in collection for i in (element, x)][:-1]

    def insert_pair_rotate(self, collection: list, element: list, **kwargs) -> list:
        """Insert a list in another list"""
        rotation = cycle(element)
        return [i for x in collection for i in (next(rotation), x)][:-1]

    def insert_rotate(self, collection: list, element: list, **kwargs) -> list:
        """Insert function to insert a fixed element as odd element of each list"""
        rotation = cycle(element)
        return [i for x in collection for i in (next(rotation), x)][:-1]

    def shuffle(self, *args, **kwargs) -> list:
        """Shuffle a newly generated collection

        Args:
            collection (list): A list generated through a qualifier

        Returns:
            list: A shuffled list of integers
        """
        collection = list(chain(*args))
        random.shuffle(collection)
        return collection

    def prob(self, prob: list, *x, **kwargs) -> list:
        """Return the pattern specified as second argument with probability"""
        return list(map(lambda x: x if random.random() * 100 < prob[0] else None, x))

    def cosinus(self, *x) -> list:
        """Basic cosinus function

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return map_unary_function(cos, x)

    def unipolar_cosinus(self, *x) -> list:
        """Basic unipolar cosinus function

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return map_unary_function(cos, abs(x))

    def sinus(self, *x) -> list:
        """Basic sinus function

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return map_unary_function(sin, x)

    def square_wave(self, *x, **kwargs) -> list:
        """Basic pulse-width modulable square wave function

        Args:
            pwm (float): pulse width of the square wave (0 < pulse_width < 1)
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        pw = kwargs.get("pwm", 0.5)
        x = list(chain(*x))
        return map_unary_function(lambda val: 1 if sin(2 * pi * val) < pw else -1, x)

    def unipolar_square_wave(self, *x, **kwargs) -> list:
        """Basic unipolar pulse-width modulable square wave function

        Args:
            pulse_width (float): pulse width of the square wave (0 < pulse_width < 1)
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        pw = kwargs.get("pwm", 0.5)
        x = list(chain(*x))
        return map_unary_function(lambda val: 1 if sin(2 * pi * val) < pw else 0, x)

    def sawtooth_wave(self, *x) -> list:
        """Basic sawtooth wave function

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return map_unary_function(lambda val: (2 / pi) * atan(tan(pi * val)), x)

    def unipolar_sawtooth_wave(self, *x) -> list:
        """Basic unipolar sawtooth wave function

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return map_unary_function(lambda val: abs((2 / pi) * atan(tan(pi * val))), x)

    def unipolar_sinus(self, *x) -> list:
        """Basic unipolar sinus function

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return map_unary_function(sin, abs(x))

    def maximum(self, *x) -> list:
        """Maximum operation

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return map_unary_function(max, [x])

    def mean(self, *x) -> list:
        """Mean operation

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return statistics.mean(list(x))

    def minimum(self, *x) -> list:
        """Minimum operation

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return map_unary_function(max, [x])

    def absolute(
        self,
        *x,
    ) -> list:
        """Basic absolute function

        Args:
            x (list): pattern

        Returns:
            list: a valid pattern.
        """
        x = list(chain(*x))
        return map_unary_function(abs, x)

    def lsin(self, period: int | float, **kwargs) -> list:
        """Basic sinusoïdal low frequency oscillator
        Args:
            period (int|float): LFO period (duration in beats)
        Returns:
            list: lfo value (-1 -> 1)
        """
        period = float(period[0])
        return [sin(2 * pi * self.clock.time / period)]

    def ltri(self, period: int | float, **kwargs) -> list:
        """Basic triangular low frequency oscillator
        Args:
            period (int|float): LFO period (duration in beats)
        Returns:
            list: lfo value (-1 -> 1)
        """
        period = float(period[0])
        t = self.clock.time % period

        def inner_func():
            if t < period / 4:
                return 4 * t / period
            elif t > 3 * period / 4:
                return 4 * t / period - 4
            else:
                return -4 * t / period + 2

        return [inner_func()]

    def lsaw(self, period: int | float, **kwargs) -> list:
        """Basic sawtooth low frequency oscillator
        Args:
            period (int|float): LFO period (duration in beats)
        Returns:
            list: lfo value (-1 -> 1)
        """
        period = float(period[0])
        t = self.clock.time % period
        return [((2 * t if t < period / 2 else (2 * t)) / 2) - 1]

    def lrect(self, period: int | float, pwm: int | float = 0.5, **kwargs) -> list:
        """Basic square low frequency oscillator
        Args:
            period (int|float): LFO period (duration in beats)
        Returns:
            list: lfo value (-1 -> 1)
        """
        period, pwm = float(period[0]), float(pwm[0]) * 100
        t = self.clock.time % period
        return [1 if t < (period * (pwm / 100)) else -1]

    def ulsin(self, period: int | float, **kwargs) -> list:
        """Basic unipolar sinusoïdal low frequency oscillator
        Args:
            period (int|float): LFO period (duration in beats)
        Returns:
            list: lfo value (0 -> 1)
        """
        # period = float(period[0])
        return self.absolute(*[self.lsin(period)])

    def ultri(self, period: int | float, **kwargs) -> list:
        """Basic unipolar triangular low frequency oscillator
        Args:
            period (int|float): LFO period (duration in beats)
        Returns:
            list: lfo value (0 -> 1)
        """
        return self.absolute(*[self.ltri(period=period)])

    def ulsaw(self, period: int | float, **kwargs) -> list:
        """Basic unipolar sawtooth low frequency oscillator
        Args:
            period (int|float): LFO period (duration in beats)
        Returns:
            list: lfo value (0 -> 1)
        """
        return self.absolute(*[self.lsaw(period=period)])

    def get_time(self, *args, **kwargs):
        """Return a specific time unit"""
        if len(args) >= 1:
            data = str(args[0][0])
        else:
            data = None

        print(data)

        if not data:
            return [self.clock.time]
        elif data == "year":
            return [int(datetime.datetime.now().year)]
        elif data == "month":
            return [int(datetime.datetime.now().month)]
        elif data == "day":
            return [int(datetime.datetime.now().day)]
        elif data == "hour":
            return [int(datetime.datetime.now().hour)]
        elif data == "minute":
            return [int(datetime.datetime.now().minute)]
        elif data == "second":
            return [int(datetime.datetime.now().second)]
        elif data == "micro":
            return [int(datetime.datetime.now().microsecond)]

    def get_bar(self, *args, **kwargs):
        """Return current measure (bar) as integer"""
        return [self.clock.bar]

    def get_phase(self, *args, **kwargs):
        """Return current phase (phase) as integer"""
        return [self.clock.phase]

    def get_unix_time(self, *args, **kwargs):
        """Return current unix time as integer"""
        return [int(time())]

    def get_scale_note(self, *args, **kwargs):
        """
        Return a note from the currently selected scale.
        If the index is higher than the collection, will
        wrap around and octave up.
        """
        x = list(chain(*args))
        forced_scale = kwargs.get("scale", None)
        if forced_scale:
            selected_scale = self.qualifiers[forced_scale[0]]
        else:
            selected_scale = self.qualifiers[self.global_scale]

        def note_computer(note) -> int:
            """Internal function to calculate the current note"""
            octave, note = divmod(note, len(selected_scale) - 1)
            return 48 + (12 * octave) + selected_scale[note]

        return map_unary_function(note_computer, x)

    def set_scale(self, *args, **kwargs):
        """
        Set the current global scale. If the name is
        unknown, will continue on the current scale.
        """
        args = list(chain(*args))

        def internal_scale_changer(scale_name):
            new_scale = str(scale_name)
            if new_scale in self.qualifiers.keys():
                self.global_scale = new_scale

        return map_unary_function(internal_scale_changer, args)

    def binary_rhythm_generator(
        self, input_number: int | float, rotation: int | float = [0]
    ):
        """
        Generate rhythms by converting an integer to binary representation.
        Everything is then converted in a rhythm using the same technique
        as the euclidian rhythm generator
        """
        rotation = int(rotation[0])
        number_as_list = [int(x) for x in list("{0:0b}".format(int(input_number[0])))]
        if rotation != 0:
            number_as_list = number_as_list[-rotation:] + number_as_list[:-rotation]

        def convert(input_list):
            input_list = int("".join([str(i) for i in input_list]))

            def convert_code(number):
                count, result = 0, []
                for digit in str(number):
                    if digit == "1":
                        if count > 0:
                            result.append(count)
                        count = 1
                    elif digit == "0":
                        count += 1
                if count > 0:
                    result.append(count)
                return result

            return convert_code(input_list)

        result = convert(number_as_list)
        return result

    def binary_list(self, number: int | float, rotation: int | float = [0]):
        """Generate a binary list with optional rotation"""
        rotation = int(rotation[0])
        number_as_list = [int(x) for x in list("{0:0b}".format(int(number[0])))]
        if rotation != 0:
            number_as_list = number_as_list[-rotation:] + number_as_list[:-rotation]
        return number_as_list
