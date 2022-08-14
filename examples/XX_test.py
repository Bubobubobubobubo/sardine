from random import random, randint, choice
c.bpm = 140
ct = 0

@swim
def test(delay=0.5, iter=0):
    global ct
    ct += 0.5
    if ct % 2.5 == 0:
        S('bd').out()
        S('jvbass', n=randint(1,20)).out()
    if ct % 3.5 == 0:
        S('cp', n=randint(1,20)).out()
        S('jvbass', n=randint(1,20)).out()
    if ct % 0.5 == 0:
        S('hh', amp=0.4).out()
    cs(test, delay=0.5, iter=iter+1)


def trump(note):
    S('jvbass', midinote=note, speed=1.5, room=0.5, amp=0.8).out()
def crow():
    S(choice(['tabla', 'sitar']).out()

@swim
def test_again(delay=0.5, iter=0, iter2=0):
    val = 1 if random() > 0.5 else 2
    val = 1 if sometimes() else 10
    val2 = 5 if sometimes() else 50
    mel = [50, 53, 57, 50, 53, 53]
    if sometimes():
        trump(note=mel[iter % len(mel) - 1])
    S('b', n=iter + val2).out()
    S(choice(['d', 'a']),
            n = 1 if sometimes() else 2,
            midinote=mel[iter % len(mel) - 1] + 24).out()
    S('c',
           midinote=mel[iter2 % len(mel) -1],
           begin=0.1,
           speed=0.2 + random(),
           legato=0.2, n=iter).out()
    if almostAlways():
        cs(test_again, delay=choice([0.5, choice([0.5, 1, 1, 0.5])]),
                iter2=iter+1, iter=(iter+1) % len(range(10)))
    else:
        crow()
        cs(test_again, delay=2, iter2=iter, iter=iter)


hush()


import random
import re

random.seed(3)
SOUND = re.compile(
    r"""
    (?P<sound>[\w|]+)
    (?: \?(?P<chance>\d*) )?
    (?:  !(?P<repeat>\d+) )?
    """,
    re.VERBOSE)
def expand_sound(s: str) -> list[str]:
    # Split the incoming string
    words, tokens = s.split(), []
    # Tokenize and parse
    for w in words:
        # Try to match a symbol, return None if not in spec
        m = SOUND.fullmatch(w)
        if m is None:
            raise ValueError(f'unknown sound definition: {w!r}')
        sound = [m['sound']]
        if '|' in m['sound']:
            sound = [random.choice( m['sound'].split('|') )]
        else:
            sound = [m['sound']]
        if m['chance'] is not None:
            chance = int(m['chance'] or 50)
            if random.randrange(100) >= chance:
                continue
        if m['repeat'] is not None:
            sound *= int(m['repeat'])
        tokens.extend(sound)
    return tokens
# s = '909? cp?30 bd?!3'
s = 'pipi|808!3 bd?'
for i in range(1, 4):
    print(f'run {i}:', expand_sound(s))


from random import uniform
random.seed(3)
SOUND = re.compile(
    r"""
    (?P<number>([-+]?[\d*\.\d+|]+))
    (?: \?(?P<chance>\d*) )?
    (?:  !(?P<repeat>\d+) )?
    (?:  :(?P<range>\d+) )?
    """,
    re.VERBOSE)
def expand_number(s: str) -> list[str]:
    # Split the incoming string
    words, tokens = s.split(), []
    # Tokenize and parse
    for w in words:
        # Try to match a symbol, return None if not in spec
        m = SOUND.fullmatch(w)
        if m is None:
            raise ValueError(f'unknown number definition: {w!r}')
        number= [m['number']]
        if m['chance'] is not None:
            chance = int(m['chance'] or 50)
            if random.randrange(100) >= chance:
                continue
        if m['repeat'] is not None:
            number *= int(m['repeat'])
        if m['range'] is not None:
            print(uniform(number, range))
            # number += [uniform(number, range)]
        tokens.extend(number)
    return tokens

s = '1:40'
for i in range(1, 8):
    print(f'run {i}:', expand_number(s))
