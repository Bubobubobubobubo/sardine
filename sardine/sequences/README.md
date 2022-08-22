# Sequences

This part of Sardine is responsible for patterning / patterns and composition. It contains a variety of tools to deal with musical composition, pattern writing, etc...

## Chance

Chance contains basic functions inspired by similar functions from TidalCycles that I know and love! It basically provides syntactic sugar for operations based on `random()`.

## ListParser
### Description

I am trying to integrate a small Lexer/Parser to Sardine. It is thought of as a glorified calculator that can also perform operations on lists. Its main purpose is to make it easy for the user to generate interesting lists really fast. The parser is built thanks to the [Lark](https://github.com/lark-parser/lark) package, using the LALR(1) algorithm for its simplicity and speed. There 

### Usage

There are multiple ways to use the Parser when using Sardine:
* the `parser(pattern: str)` function. Feed it a pattern, observe the output.
* the `parser_repl()` function that operates like a debug mode for the parser. Quit by typing `Ctrl-C`.
* from the main Sardine objects themselves when you are making music.

String arguments passed to the `S()`, `O()` and `M()` objects will be parsed using the `ListParser`. It means that you can use the mini-notation defined by the parser for every musical parameter!

### Debug and future improvements

I don't really know how to write a parser or even how it operates in detail! I lack method and discipline for writing such a complex piece of software, even for something as simple as a glorified calculator! If you know how to write something better, please do! The output of the parser is verified by running *incomplete* and *to be improved* tests using the `unittest` module. Tests are stored in the `tests/` folder. You can run the tests yourself by typing the following command from the `sequences/` folder:

```bash
python3 -m unittest
```

Note that you can increase the verbosity of the tests if you need (choose one option):

```bash
python3 -m unittest -v -vv -vvv 
```