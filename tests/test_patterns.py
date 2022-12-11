import pytest
import pytest_asyncio

from sardine import FishBowl
from sardine.sequences import ListParser


# NOTE: only put new parsers here if they support sardine's patterning syntax
@pytest_asyncio.fixture(scope="module", params=[ListParser])
def fish_bowl(request: pytest.FixtureRequest):
    return FishBowl(parser=request.param())


@pytest.mark.parametrize(
    "pattern,expected",
    [
        (".", [None]),
        (".!4", [None] * 4),
    ],
)
def test_silence_op(fish_bowl: FishBowl, pattern: str, expected: list):
    assert fish_bowl.parser.parse(pattern) == expected


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("1|2|3|4", [[1], [2], [3], [4]]),
        ("[1,2,3,4]|[., .]", [[1, 2, 3, 4], [None, None]]),
        ("baba|dada", [["baba"], ["dada"]]),
        ("(baba:2)|(dada:4)", [["baba:2"], ["dada:4"]]),
    ],
)
def test_choice_op(fish_bowl: FishBowl, pattern: str, expected: list):
    assert fish_bowl.parser.parse(pattern) in expected


@pytest.mark.parametrize(
    "pattern,expected",
    [
        (".5", [0.5]),
        ("0.5", [0.5]),
        ("1, 2, 3", [1, 2, 3]),
        ("1+1, 2*3, 4-1, 5/2", [2, 6, 3, 2.5]),
    ],
)
def test_number_pattern(fish_bowl: FishBowl, pattern: str, expected: list):
    """
    Test parsing several patterns composed of numbers and simple math operations.
    """
    assert fish_bowl.parser.parse(pattern) == pytest.approx(expected)


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("[1,2,3]+1, [1,2,3]*2", [2, 3, 4, 2, 4, 6]),
        ("[1,2,3]/2, [1,2,3]//2", [0.5, 1.0, 1.5, 0, 1, 1]),
        ("[2,3,4]-2, [2,3,4]%2", [0, 1, 2, 0, 1, 0]),
        ("[1,2,3,4]+[1,2,3,4]", [2, 4, 6, 8]),
        ("[1,2,3,4]*[1,2,3,4]", [1, 4, 9, 16]),
        ("[1,2,3,4]/[1,2,3,4]", [1.0, 1.0, 1.0, 1.0]),
        ("[1,2,3,4]/[2,3,4,5]", [0.5, 2 / 3, 0.75, 0.8]),
        ("[2,4,6,8]%[12,8]", [2, 4, 6, 0]),
    ],
)
def test_list_arithmetic(fish_bowl: FishBowl, pattern: str, expected: list):
    assert fish_bowl.parser.parse(pattern) == pytest.approx(expected)


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("C,D,E,F,G,A,B", [60, 62, 64, 65, 67, 69, 71]),
        ("Do,Re,Mi,Fa,Sol,La,Si", [60, 62, 64, 65, 67, 69, 71]),
        ("Do,Ré,Mi,Fa,Sol,La,Si", [60, 62, 64, 65, 67, 69, 71]),
        ("C0,C1,C2,C3,C4,C5,C6,C7,C8,C9", [12, 24, 36, 48, 60, 72, 84, 96, 108, 120]),
        ("C, C#, Cb", [60, 61, 59]),
        ("C, Eb, G", [60, 63, 67]),
        ("C, C., C.., C...", [60, 48, 36, 24]),
        ("C, C', C'', C'''", [60, 72, 84, 96]),
        ("C@maj7, C@min7", [60, 64, 67, 71, 60, 63, 67, 70]),
    ],
)
def test_note_compositions(fish_bowl: FishBowl, pattern: str, expected: list):
    assert fish_bowl.parser.parse(pattern) == expected


@pytest.mark.parametrize(
    "pattern,expected_range",
    [
        ("0~1", range(0, 2)),
        ("0~10", range(0, 11)),
        ("100~200", range(100, 201)),
    ],
)
def test_integer_ranges(fish_bowl: FishBowl, pattern: str, expected_range: list):
    assert fish_bowl.parser.parse(pattern)[0] in expected_range


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("[1,2]!2", [1, 2, 1, 2]),
        ("[1,2]!!2", [1, 1, 2, 2]),
        ("[1,.]!2", [1, None, 1, None]),
        ("[1,.]!!2", [1, 1, None, None]),
    ],
)
def test_list_expansion(fish_bowl: FishBowl, pattern: str, expected: list):
    assert fish_bowl.parser.parse(pattern) == expected


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("-1", [-1]),
        ("-22.231", [-22.231]),
    ],
)
def test_negation(fish_bowl: FishBowl, pattern: str, expected: list):
    assert fish_bowl.parser.parse(pattern) == expected


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("[1:5]", [1, 2, 3, 4, 5]),
        ("[0:1,.3]", [0, 0.3, 0.6, 0.9]),
        ("[10:8,.5]", [10, 9.5, 9, 8.5, 8]),
        ("0, [1:3], 4, 5", [0, 1, 2, 3, 4, 5]),
    ],
)
def test_ramps(fish_bowl: FishBowl, pattern: str, expected: list):
    assert fish_bowl.parser.parse(pattern) == pytest.approx(expected)
