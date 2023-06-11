# Function Library

The **Sardine Pattern Language** is a real programming language. It supports function calls with arguments and keyword arguments just like Python and you can combine multiple functions to create complex patterns. 

Calling a function is really simple given that you know the syntax to do so. The syntax functions as follows:

- a function starts with a name wrapped in-between two parentheses: `(sopr 1 2 3 4)`, `(time)`, `(bar)`.
- Functions can take any amount of arguments. Some of them will have fixed positional arguments.
    - any amount: `(func 1 2 3 4 5 6 ...)`
    - positional: `(func 1 2)` where `1` and `2` are required and other arguments get discarded.
- Some functions take keyword arguments. They are written using the `::keyword` form: `(disco C4 D4 E4 ::depth 2)`.

The documentation is the best place to learn about functions. Your code editor won't help you because the **Sardine Pattern Language** is written as strings and is not recognized as code by any autocompletion engine or plugin.

I will always provide indications on how to call the function, telling you the role of each argument.
- `...` means that the function can take any number of arguments.
- otherwise, the function will take a fixed number of arguments whose name will be given.
