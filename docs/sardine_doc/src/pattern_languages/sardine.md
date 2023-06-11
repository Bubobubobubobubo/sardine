# Sardine Pattern Language

## What and where are patterns?

You will find the pattern language pretty much everywhere in **Sardine**. Everytime you use any of the senders like `D()`, `N()`, `P()` and their lowercase variants, you are likely using the pattern language already. **Sardine** automatically turns every `string` argument it receives into a pattern using the **Sardine Pattern Language**:

```python
D('bd', speed=1, legato=2) # speed and legato are using regular Python types
D('b', speed='1|2', legato='1~4') # speed and legato are now patterns (string)
```

Think of it as having a second programming language inside your main programming language. This language is a welcomed addition:

- It is an efficient way to create variety in the musical output of your code. 
- It saves space and makes it easier to express complex pattern transformations.
- It gives you access to new operators that **Python** doesn't provide by default.
- It makes writing lists way easier and less verbose compared to Python.

Note that pattern languages are one of the basic tools used in most live coding environments. Each environment comes with its own flavour, and Sardine comes with multiple pattern languages!

## Pattern Object

Sardine also has a pattern object, named `P()`. This object is very useful when you start exploring on your own and start building your own abstractions. The most typical usage of the `P()` is to pattern the `again` call in a **swimming function** like so:

```python
@swim
def donothing(p=1, i=0):
    print('I do nothing really interesting!')
    again(donothing, p=P('1 2 0.5!4', i), i=i+1)
```

If you want to learn more about it, I encourage you to read: [Diving Deeper > Pattern Object](../diving_deeper/pattern_object.md).


