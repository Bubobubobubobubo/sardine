"""
Mini-notation grammar for Vortex.

Grammar is defined using the PEG parsing library `parsimonious`.

Given the set of rules and definitions (grammar) defined in this file, calling
`grammar.parse(mn)` generates an abstract syntax tree (AST) for a given input
mini-notation string named `mn`.

Printing the tree object shows the generated ASTs. e.g.:

```
tree = grammar.parse("bd(3, 8) cp")
```

yields the following (truncated) AST, which can be pretty-printed with:

```
print(tree.prettily())
```

```
<Node called "valid" matching "bd(3, 8) cp">
    <Node called "sequence" matching "bd(3, 8) cp">
        <Node matching "">
            <RegexNode called "ws" matching "">
        <Node called "element" matching "bd(3, 8) ">
            <Node called "modified" matching "bd(3, 8) ">
                <Node called "modifiable" matching "bd">
                    <Node called "word" matching "bd">
                    ...
        <Node matching "cp">
            <Node matching "cp">
                <RegexNode called "ws" matching "">
                <Node matching "cp">
                    <Node called "element" matching "cp">
                        <Node called "word" matching "cp">
```

The parsimonious README (https://github.com/erikrose/parsimonious) was all I
needed to get started writing a 'port' of the TidalCycles mini-notation grammar
for Vortex.

The strudel PEG grammar written in pegjs by Felix Roos was a valuable starting
point, and many ideas were taken from there.
https://github.com/tidalcycles/strudel/blob/main/packages/mini/krill.pegjs

Reach out on the TidalCycles discord or club.tidalcycles.org if you have any
bugs, optimizations, or questions.

-Tyler

"""

from parsimonious import Grammar

grammar = Grammar(
    r"""
    root = ws? sequence ws?

    ##
    # Sequences
    #
    # A Sequence is a white-space separated collection of 2 or more elements
    # like "bd bd" or "[bd bd] [bd bd]".  Underscores (continuation symbol) can
    # be part of a sequence but cannot be the first element.
    sequence = group (ws !'|' '.' ws group)* (ws? '|' ws? sequence)*
    group = element (ws !'.' element)*

    # An Element is an item of a Sequence, it can be a simple Term, or another
    # subsequence: Polymeters (braces), Polyrhythms (square brackets) or one-cycle
    # polymeter (angle brackets)
    element = element_value euclid_modifier? modifiers (ws '_')*
    element_value = term / polyrhythm_subseq / polymeter_subseq / polymeter1_subseq

    ##
    # Subsequences
    #
    polyrhythm_subseq = '[' ws? subseq_body ws? ']'
    polymeter_subseq = '{' ws? subseq_body ws? '}' polymeter_steps?
    polymeter1_subseq = '<' ws? subseq_body ws? '>'
    polymeter_steps = '%' number
    subseq_body = sequence (ws? ',' ws? sequence)*

    ##
    # Terms
    #
    term = number / word_with_index / rest
    word_with_index = word index?
    index = ':' number

    ##
    # Euclid modifier
    #
    euclid_modifier = '(' ws? sequence ws? ',' ws? sequence euclid_rotation_param? ws? ')'
    euclid_rotation_param = ws? ',' ws? sequence

    ##
    # Term modifiers
    #
    modifiers = modifier*
    modifier = fast / slow / repeat / degrade / weight
    fast = '*' element
    slow = '/' element
    repeat = (repeatn / repeat1)+
    repeatn = '!' !'!' pos_integer
    repeat1 = '!'
    degrade = degrader / degraden / degrade1
    degrader = '?' !'?' pos_real
    degraden = '?' !'?' !pos_real pos_integer
    degrade1 = '?'
    weight = '@' number

    ##
    # Primitives
    #
    # A primitive is a simple token like a word (string) or a number (real or
    # integer).
    word = ~"[-\w]+"
    number = real / integer
    real = integer '.' pos_integer?
    pos_real = pos_integer '.' pos_integer?
    integer = minus? pos_integer
    pos_integer = !minus ~"[0-9]+"
    rest = '~'

    ## Misc
    minus = '-'
    ws = ~"\s+"
    """
)
