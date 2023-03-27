# @swim function

The `@swim` function is the fundamental mechanism for managing output and changing values and parameters dynamically. Strictly speaking, a `@swim` function is an example of a *temporally recursive function*. This is a programming construct that supports repetition in time with dynamic parameter values. Temporal recursion is common in livecoding languages as it is a very fundamental way to think about time in the context of the execution of a program. In Sardine, the `@swim` function has unique ways and syntax to manage repeats. The Sardine scheduling engine will manage repeats as well as parameter and pattern value changes strictly following the tempo and beat patterns we tell Sardine to use. 

To illustrate, let's start with a basic Python function:

```python
def hello_world():
    print('Hello, World!')

# Call this function with this command.
hello_world()
```

Now let's convert this into a `@swim` function which adds temporal recursion with looping at the beat. Execute the code below, then make changes to the tempo value. Watch how the output of the python `print` statement comes in the exact tempo you specify. The `again()` statement is what provides the temporal recursion (looping in tempo). You could also just say that `again()` tells the `@swim` function to repeat! 

```python
clock.tempo=60 
@swim
def hello_world():
    print('Hello, World!')
    again(hello_world)
```
You can stop a swimming function by changing the Python "decorator" from `@swim` to `@die`.
```python
@die
def hello_world():
    print('Hello, World!')
    again(hello_world)

# You can also stop a @swim function using these commands: 
silence(hello_world)
hello_world.stop()
silence() # stops everything
```

### Iterator: "i" is the essential driver 
Let's translate this into musical output. The swimming function below uses a SuperDirt Sender **D()** with a sample pattern. Importantly, we now have an iterator - which by Sardine convention uses the character **i**. It appears in the function arguments, in the recursion `again()`, and in the Sender. 
- function definition: `inFive(p=1, i=0)` the period (p) and iterator (i) are initialized.
- sender argument: `i=i` is added. This tells Sardine to iterate over the sample and speed patterns on every recursion (repeat). 
- again argument: `i=i+1` This expression increments the iterator. We will see later how this expression can be changed to create interesting musical results. 

```python
@swim
def inFive(p=1, i=0):
    print(f"Value of i: {i}")
    D('bd!2 cp hh27:2 cr:2', speed='1 2', i=i)
    again(inFive, p=0.5, i=i+1)
```

### @swim function syntax
- **@swim**: this is the "decorator" in python terms. It always has its own line.
- `def inFive(p=1, i=0):` the "def" keyword in python creates a custom function. 
  - Format: `def <name>(arguments with default values)`
  - Function names can contain alpha-numeric but no spaces or special characters.
  - Function names must match the name provided in the `again()` statement.
  - Iterator and period values are initialized. 
- D() is the SuperDirt Sender. 
  - Any of the valid @swim [Senders](./senders.md) can be used - N(), ZD(), etc. 
  - Multiple senders can be used.
  - Sender arguments are separated by comma.
  - Senders need the iterator value: `i=i`.
- Python functions can be added.
  - In the example above, a simple python `print` statement is called with the value of "i" changing every beat. 
  - Functions will be called on each iteration. 
- `again(<functionName>, p=<value>, i=<expression>)` 
  - The again() statement requires the exact function name. 
  - The period assignment is optional, and will default to 1. It is common to include it to be able to set or easily change the rhythm per beat value. 
  - iterator expression `i=i+1` is the most common, but other values and patterns are valid and can yield interesting musical results. 

## More @swim function examples

```python
clock.tempo=100

@swim
def sequence(p=0.5, i=0):
    D('bd!2 cp:rand*20 tabla',
        speed='1 2 3 4 5 6',
        room=0.5, size=0.4, dry=0.5,
        lpf="200+rand*2000", i=i)
    D('. hh:7 hh:10', r=0.5, i=i)
    again(sequence, p=P('0.5!4 0.25!2', i), i=i+1)
```

```python
clock.tempo=64

@swim 
def test(p=1, i=0):
    D('jvbass:0~5', 
         room=0.9, gain=0.8, size=0.4, dry=0.5,
         midinote='C4 G3 E3 D6 .', i=i)
    again(test, p=1/8, i=i+1)
```





