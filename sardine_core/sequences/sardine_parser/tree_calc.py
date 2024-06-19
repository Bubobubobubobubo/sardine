import random
from itertools import chain, count, takewhile
from time import time

from lark import Transformer, v_args
from lark.lexer import Token
from rich.panel import Panel

from sardine_core.logger import print

from . import funclib
from .chord import Chord
from .utils import CyclicalList, map_binary_function, map_unary_function, zip_cycle


@v_args(inline=True)
class CalculateTree(Transformer):
    def __init__(self, clock, variables, inner_variables: dict, global_scale: str):
        super().__init__()
        self.clock = clock
        self.variables = variables
        self.inner_variables = inner_variables
        self.global_scale = global_scale
        self.memory = {}
        self.library = funclib.FunctionLibrary(
            clock=self.clock,
            amphibian=self.variables,
            inner_variables=self.inner_variables,
            global_scale=self.global_scale,
        )

    def number(self, number):
        try:
            return [int(number)]
        except ValueError:
            return [float(number)]

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
        return [None] * len(args)

    def numbered_silence(self, duration):
        """
        Variant of a silence with a numeric value indicating silence length
        """
        print(duration)
        return [None] * duration

    # ---------------------------------------------------------------------- #
    # Notes: methods used by the note-specific parser
    # ---------------------------------------------------------------------- #

    def specify_address(self, name0, name1):
        """Convert underscore into slash for name based addresses"""
        return map_binary_function(lambda x, y: x + "/" + y, name0, name1)

    def random_note_in_range(self, number0, number1):
        """Generates a random MIDI Note in the range number0 - number1.

        Args:
            number0 (int):  low boundary
            number1 (int): high boundary

        Returns:
            int: a random MIDI Note.
        """
        return random.randint(int(number0), int(number1))

    def make_note(self, note):
        """Return a valid MIDI Note (fourth octave)
        from a valid anglo-saxon, french or canadian note name.

        Args:
            note (str): a string representing a valid note ("A" to "G", or "Do" to "Si").

        Returns:
            int: A MIDI Note (fourth octave)
        """
        if note in ["Cb", "Dob"]:
            return -1 + 12 + 12 * 4
        elif note in ["C", "Do", "B#", "Si#"]:
            return 0 + 12 + 12 * 4
        elif note in ["C#", "Db", "Do#", "Réb", "Reb"]:
            return 1 + 12 + 12 * 4
        elif note in ["D", "Re", "Ré"]:
            return 2 + 12 + 12 * 4
        elif note in ["D#", "Ré#", "Re#", "Eb", "Mib"]:
            return 3 + 12 + 12 * 4
        elif note in ["E", "Mi"]:
            return 4 + 12 + 12 * 4
        elif note in ["F", "Fa"]:
            return 5 + 12 + 12 * 4
        elif note in ["F#", "Fa#", "Gb", "Solb"]:
            return 6 + 12 + 12 * 4
        elif note in ["G", "Sol"]:
            return 7 + 12 + 12 * 4
        elif note in ["G#", "Sol#", "Ab", "Lab"]:
            return 8 + 12 + 12 * 4
        elif note in ["A", "La"]:
            return 9 + 12 + 12 * 4
        elif note in ["Bb", "A#", "Sib", "La#"]:
            return 10 + 12 + 12 * 4
        elif note in ["B", "Si", "Ti"]:
            return 11 + 12 + 12 * 4

    def note_flat(self, note):
        """Flatten a note"""
        return note - 1

    def note_sharp(self, note):
        """Sharpen a note"""
        return note + 1

    def note_set_octave(self, note, value):
        """Move a note to a given octave"""
        return ((note - 12) % 12) + 24 + 12 * int(value)

    def get_slice(self, content: list, list_slice: list) -> list:
        """Return a slice of the given list"""
        if len(list_slice) == 1:
            return content[list_slice[0] % len(content) - 1]
        else:
            content = CyclicalList(content)
            return content[list_slice[0] : list_slice[1]]

    def make_chord(self, *args: list):
        """Turn a list into a chord"""
        return [self.library.chordify(*sum(args, start=[]))]

    def chord_reverse(self, notes: list, inversion: list) -> list:
        """Chord inversion upwards"""
        return self.library.invert(notes, [int(inversion[0])])

    def note_octave_up(self, note):
        """Move a note one octave up"""
        if note <= 127 - 12:
            return note + 12
        else:
            return note

    def note_octave_down(self, note):
        """Move a note one octave down"""
        if note >= 12:
            return note - 12
        else:
            return note

    def finish_note(self, note):
        """Finish the note construction"""
        return [note]

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
            return map_binary_function(
                lambda x, y: x + y, note, self.library.qualifiers[str(quali)]
            )
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

    def id(self, a):
        """Identity function. Returns first argument."""
        return a

    def make_list(self, *args):
        """Make a list from gathered arguments (alias used by parser)

        Returns:
            list: Gathered arguments in a list
        """
        return sum(args, start=[])

    def make_list_repeat(self, *args):
        """Make a list from gathered arguments (alias used by parser)

        Returns:
            list: Gathered arguments in a list
        """
        return sum(args, start=[]) * 2

    def get_random_number(self):
        """Return a random number (alias used by parser)

        Returns:
            float: a random floating point number
        """
        return [random.random()]

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
        try:
            ramp_from, ramp_to = left[-1], right[0]
            if any([isinstance(x, float) for x in [ramp_from, ramp_to]]):
                return self.generate_ramp_with_range([ramp_from], [ramp_to], [1.0])
            between = range(min(ramp_from, ramp_to) + 1, max(ramp_from, ramp_to))
            between_flipped = between if ramp_from <= ramp_to else reversed(between)
            return left + list(between_flipped) + right
        except Exception as e:
            print(e)

    def generate_ramp_with_range(self, left, right, step):
        """Generates a ramp of integers between x included and y
        included (used by parser). Variant using a step param.

        Args:
            left (int): First boundary
            right (int): Second boundary
            step (int): Range every x steps

        Returns:
            list: a ramp of ascending or descending integers with step
        """
        start, stop, step, epsilon = (
            min(left, right)[0],
            max(left, right)[0],
            step[0],
            0.0000001,
        )
        ramp = list(
            takewhile(
                lambda x: x < stop + epsilon, (start + i * abs(step) for i in count())
            )
        )
        if left > right:
            return list(reversed(ramp))
        else:
            return ramp

    def generate_ramp_with_interpolate(self, left, right, steps):
        """Generates a ramp of floats between x included and y
        included (used by parser). Variant using a step param.

        Args:
            left (int): First boundary
            right (int): Second boundary
            step (int): Number of steps over which to generate this ramp

        Returns:
            list: a ramp of ascending or descending floats with step
        """
        start, stop, steps = (
            min(left, right)[0],
            max(left, right)[0],
            steps[0],
        )
        delta = (stop - start) / steps
        ramp = list([start + i * delta for i in range(steps)])
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
        if isinstance(left, Chord):
            return [self.make_chord(left)] * sum(
                int(x) if x is not None else 0 for x in right
            )
        else:
            return left * sum(int(x) if x is not None else 0 for x in right)

    def extend_repeat(self, left, right):
        """Variation of the preceding rule.
        TODO: document this behavior."""
        return sum(
            (
                [x] * (int(y) if y is not None else 0)
                for (x, y) in zip_cycle(left, right)
            ),
            start=[],
        )

    def choice(self, left, right):
        """Choose 50%-50% between the 'left' or 'right' token

        Args:
            left (any): First possible choice
            right (any): Second possible choice

        Returns:
            any: A token chosen between 'left' or 'right'.
        """
        return random.choice([left, right])

    def union(self, left, right):
        """
        Merge the two lists into a list of the same length as the longest one,
        applying an element-wise logical OR. Works best with 1s, 0s, and rests.

        If one of the operand is shorter than the other, it is repeated until
        it reaches the length of the longest one.

        If two "truthy" elements are being compared, the one from the left
        operand is kept.
        """
        out = []

        if not len(left):
            return right
        if not len(right):
            return left

        for i in range(max(len(left), len(right))):
            out.append(left[i % len(left)] or right[i % len(right)])

        return out

    def intersection(self, left, right):
        """
        Merge the two lists into a list of the same length as the longest one,
        applying an element-wise logical AND. Works best with 1s, 0s, and rests.

        If one of the operand is shorter than the other, it is repeated until
        it reaches the length of the longest one.

        If two "falsy" elements are being compared, the one from the left
        operand is kept.
        """
        out = []

        if not len(left):
            return [None] * len(right)
        if not len(right):
            return [None] * len(left)

        for i in range(max(len(left), len(right))):
            out.append(left[i % len(left)] and right[i % len(right)])

        return out

    def xor(self, left, right):
        """
        Merge the two lists into a list of the same length as the longest one,
        applying an element-wise logical XOR. Works best with 1s, 0s, and rests.

        If one of the operand is shorter than the other, it is repeated until
        it reaches the length of the longest one.

        If two "truthy" elements are being compared, the one from the left
        operand is kept.
        """
        out = []

        if not len(left):
            return [None] * len(right)
        if not len(right):
            return [None] * len(left)

        for i in range(max(len(left), len(right))):
            if left[i % len(left)] and right[i % len(right)]:
                # Returning a rest as default value when both elements are truthy seems to be the most appropriate
                # way of doing things, since those methods are mostly used for rhythms generation.
                out.append(None)
            else:
                out.append(left[i % len(left)] or right[i % len(right)] or None)

        return out

    def random_in_range(self, left, right):
        left = min([left, right])
        right = max([left, right])

        def my_random(low, high):
            if isinstance(low, int) and isinstance(high, int):
                return random.randint(low, high)
            else:
                return random.uniform(low, high)

        return map_binary_function(my_random, left, right)

    def negation(self, value):
        return map_unary_function(lambda x: -x, value)

    def addition(self, left, right):
        return map_binary_function(lambda x, y: x + y, left, right)

    def modulo(self, left, right):
        return map_binary_function(lambda x, y: x % y, left, right)

    def power(self, left, right):
        return map_binary_function(lambda x, y: pow(x, y), left, right)

    def substraction(self, left, right):
        return map_binary_function(lambda x, y: x - y, left, right)

    def multiplication(self, left, right):
        return map_binary_function(lambda x, y: x * y, left, right)

    def division(self, left, right):
        return map_binary_function(lambda x, y: x / y, left, right)

    def floor_division(self, left, right):
        return map_binary_function(lambda x, y: x // y, left, right)

    def name(self, name):
        """Generating a name"""
        return [str(name)]

    def assoc_sp_number(self, name, value):
        def _simple_association(name, value):
            return name + ":" + str(int(value))

        return map_binary_function(_simple_association, name, value)

    def easy_choice(self, *args):
        return random.choice(args)

    def is_equal(self, left, right):
        return [1] if left[0] == right[0] else [0]

    def is_greater(self, left, right):
        if None or [None] in [left, right]:
            return [0]
        else:
            return [1] if left[0] > right[0] else [0]

    def is_greater_or_equal(self, left, right):
        if None or [None] in [left, right]:
            return [0]
        else:
            return [1] if left[0] >= right[0] else [0]

    def is_smaller(self, left, right):
        if None or [None] in [left, right]:
            return [0]
        else:
            return [1] if left[0] < right[0] else [0]

    def is_smaller_or_equal(self, left, right):
        if None or [None] in [left, right]:
            return [0]
        else:
            return [1] if left[0] <= right[0] else [0]

    def function_call(self, func_name, *args):
        """
        Function application: supports arguments and keyword arguments just like the
        basic Python syntax. There are a few special keys you can use for conditional
        application of the function:

        - cond: apply the function only if boolean (represented by 1/0) is True. Condi-
          tions can be chained as well for weirder chance / probability based operations

        """

        # Splitting between arguments and keyword arguments
        current_keyname, past_keywords, skip_mode = "", [], False
        arguments, kwarguments = [], {}

        for _ in args:
            # print(f'Token: {_} (type: {type(_)})')
            # We need to determine if we are currently looking at a keyword and its
            # value. If we have a repeating keyword, we will do our best to
            # completely ignore it.
            if isinstance(_, Token):
                if not _ in past_keywords:
                    current_keyname = str(_)
                    kwarguments[current_keyname] = []
                else:
                    skip_mode = True

            if skip_mode:
                continue

            if current_keyname == "":
                arguments.append(_)
            else:
                if not isinstance(_, Token):
                    kwarguments[current_keyname].append(_)

        # Cleaning keyword_arguments so they form clean lists
        kwarguments = {k: list(chain(*v)) for k, v in kwarguments.items()}

        try:
            modifiers_list = {
                # Amphibian variables
                "get": self.library.get_variable,
                "set": self.library.set_variable,
                "getA": self.library.get_amphibian_variable,
                "setA": self.library.set_amphibian_variable,
                "ga": self.library.get_amphibian_variable,
                "sa": self.library.set_amphibian_variable,
                "g": self.library.get_variable,
                "s": self.library.set_variable,
                # Pure conditions
                "if": self.library.binary_condition,
                "nif": self.library.negative_binary_condition,
                "while": self.library.unary_condition,
                "nwhile": self.library.negative_unary_condition,
                # Boolean functions
                "phase": self.library.phase,
                "beat": self.library.beat,
                "obar": self.library.oddbar,
                "modbar": self.library.modbar,
                "ebar": self.library.evenbar,
                "every": self.library.every,
                "maybe": self.library.proba,
                "dice": self.library.dice,
                # Voice leading operations
                "dmitri": self.library.dmitri,
                "voice": self.library.find_voice_leading,
                "quant": self.library.quantize,
                "disco": self.library.disco,
                "invert": self.library.invert,
                "aspeed": self.library.anti_speed,
                # Boolean mask operations
                "eu": self.library.euclidian_rhythm,
                "neu": self.library.negative_euclidian_rhythm,
                "mask": self.library.mask,
                "notdot": self.library.notdot,
                "filtdot": self.library.filtdot,
                "keepdot": self.library.keepdot,
                "euclid": self.library.euclidian_to_number,
                "numclid": self.library.euclidian_to_number,
                "e": self.library.euclidian_to_number,
                "vanish": self.library.remove_x,
                "expand": self.library.expand,
                "pal": self.library.palindrome,
                "rev": self.library.reverse,
                "leave": self.library.leave,
                "insertp": self.library.insert_pair,
                "insert": self.library.insert,
                "insertprot": self.library.insert_pair_rotate,
                "insertrot": self.library.insert_rotate,
                "shuf": self.library.shuffle,
                # Math functions
                "sin": self.library.sinus,
                "usin": self.library.unipolar_sinus,
                "cos": self.library.cosinus,
                "ucos": self.library.unipolar_cosinus,
                "drunk": self.library.drunk,
                "saw": self.library.sawtooth_wave,
                "usaw": self.library.unipolar_sawtooth_wave,
                "rect": self.library.square_wave,
                "clamp": self.library.clamp,
                "urect": self.library.unipolar_square_wave,
                "abs": self.library.absolute,
                "max": self.library.maximum,
                "min": self.library.minimum,
                "mean": self.library.mean,
                "scale": self.library.scale,
                "filt": self.library.custom_filter,
                "quant": self.library.quantize,
                # Bipolar and unipolar time-dependent Low frequency oscillators
                "lsin": self.library.lsin,
                "ltri": self.library.ltri,
                "lsaw": self.library.lsaw,
                "lrect": self.library.lrect,
                "ulsin": self.library.ulsin,
                "ultri": self.library.ultri,
                "ulsaw": self.library.ulsaw,
                # Time information
                "time": self.library.get_time,
                "bar": self.library.get_bar,
                "phase": self.library.get_phase,
                "unix": self.library.get_unix_time,
                "t": self.library.get_time,
                "b": self.library.get_bar,
                "p": self.library.get_phase,
                "u": self.library.get_unix_time,
                # Global scale support
                "scl": self.library.get_scale_note,
                "setscl": self.library.set_scale,
                # Binary rhythm generator
                "br": self.library.binary_rhythm_generator,
                "bl": self.library.binary_list,
                "rot": self.library.rotate,
            }
        except Exception as e:
            print(e)
        try:
            if kwarguments.get("cond", [1]) >= [1] or not "cond" in kwarguments.keys():
                return modifiers_list[func_name](
                    *list(chain(arguments)), **(kwarguments)
                )
            else:
                return list(arguments)
        except Exception as e:
            # Fail safe
            print(
                Panel.fit(
                    f"[red]/!\\\\[/red] [bold]Unknown or malformed function [/bold][bold yellow]{func_name}[/bold yellow] [red]/!\\\\[/red]\n\n[reverse gold1]{e}\n[/reverse gold1]\n[bold]Possible functions are:[/bold] \n\n"
                    + "".join(f"{name} " for name in modifiers_list.keys())
                )
            )
            return args[0]
