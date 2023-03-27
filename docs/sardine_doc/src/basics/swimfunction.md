# @swim function

The @swim function is the fundamental mechanism for managing output and changing values and parameters dynamically. Strictly speaking, a @swim function is an example of a "temporal recursion function." This is a construct used in programming that supports repetition in time with dynamic parameter values. Temporal recursion is common in livecoding languages. In Sardine, the @swim function has unique ways and syntax to manage repeats. The trick under the hood is that we need the Sardine scheduling engine to manage repeats, parameter and pattern value changes strictly in the tempo we tell Sardine to use. 

To illustrate, execute the following code, then make changes to the tempo value. Watch out the output of the python `print` statement comes in the exact tempo you specify. The `again()` function is what provides the temporal recursion. You could also just say that `again()` tells the @swim function to repeat! 

```python
clock.tempo=60 
@swim
def hello_world():
    print('Hello, World!')
    again(hello_world)
```
**Iterator** - the essential driver. 
Let's translate this into a musical output. The @swim function below has a Sender **D()**, Sender arguments with an iterator assignment: `i=i`. Note that the iterator value and period value are first initialized in the function definition line `inFive(p=1, i=0)`, then modified in the `again()` section. 

```python
@swim
def inFive(p=1, i=0):
    print(f"Value of i: {i}")
    D('bd!2 cp hh27:2 cr:2', speed='1 2', i=i)
    again(inFive, p=0.5, i=i+1)
```

Syntax anatomy:
- **@swim**: this is the "decorator" in python terms. It always has its own line.
- `def inFive(p=1, i=0):` "def" in python creates a custom function. 
  - format: `def <name>(arguments with default values)`
  - function names can contain alpha-numeric but no spaces or special characters
  - function names must match to the name provided in `again()`. 
- D() is the SuperDirt Sender. 
  - Any of the valid @swim [Senders](./senders.md) can be used - N(), ZD(), etc. 
  - Multiple senders lines can be used.
- Python functions can be called - but note that they will be called on each iteration. 
  - Here a simple python `print` statement is called with the value of "i" changing every beat. 
- `again(<functionName>, p=<value>, i=i+1)` 
  - The again() section requires the exact function name. 
  - The period assignment is option, and will default to 1. It is common to include it to be able to set or easily change the rhythm per beat value. 
  - **iterator expression** `i=i+1` is the most common, but other values and patterns are valid and can yield interesting musical results. 

## More @swim function examples


```python

```

```python
@swim
def inFive(p=1, i=0):
    print(f"Value of i: {i}")
    D('bd!2 cp hh27:2 cr:2', speed='1 2', i=i)
    again(inFive, p=0.5, i=i+1)
```





