import pprint

from .grammar import grammar
from .interpreter import MiniInterpreter, MiniVisitor

visitor = MiniVisitor()
interpreter = MiniInterpreter()


def parse_mini(code):
    raw_ast = grammar.parse(code)
    return visitor.visit(raw_ast)


def mini(code, print_ast=False):
    ast = parse_mini(code)
    if print_ast:
        pprint.pp(ast)
    return interpreter.eval(ast)
