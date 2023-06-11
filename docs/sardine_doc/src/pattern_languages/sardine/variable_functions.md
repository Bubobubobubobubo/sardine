# Variable Functions

This set of functions is handling all the variables available in the **Sardine Pattern Language**. You will find functions used to set the value or get the value of **amphibian variables**, **internal variables** and also some other important variables such as the currently selected global scale. 

# set (s)

Assign a variable to a name in a global namespace shared by all the SPL expressions. The variable can be anything: a number, a name, a list, etc... The function also returns the value, allowing it to be re-used immediately for the current pattern. This function is of **paramount importance**. You can use it to write reactive patterns, where multiple patterns share the same data.

**Arguments:**
- **name:** variable name. Can be any valid name.
- **value:** a single value (int, float, name, list).

**Example:**
```python
# Change (set a ...) to update multiple patterns at once
Pa * d('kick', speed='(set imp [1 3 4 9 2 4])') # Setting some numbers in the variable "imp"
Pb * d('hat:(get imp)', speed='(get imp)')      # Getting these numbers in many other patterns
```

# get (g)

Get a variable associated to a name. This function is the second part of the *get*/*set* mechanism. You can retrieve any value currently associated to a name. If no name-value is found for that name, the value `0` will be returned in an attempt to prevent crashes.

**Arguments:**
- **name:** variable name.

**Example:**
```python
Pz * d('clap', room='(get roomy)', crush='(get globalcrush)')
```

# setA (sa)

This function is part of the [amphibian variables](../../diving_deeper/amphibian_variables.html) mechanism. In a similar fashion to **set**, this function can be used to set the value of the associated amphibian variable. There is currently 26 amphibian variables you can use, one for each letter of the latin alphabet in lowercase. Just like **set**, you can set a value and still return its value for later usage.

**Arguments:**
- **variable name:** name of the amphibian variable to get.

**Example:**
```python
(setA b 20)
(sa b 20)
```

# getA (ga)

- **variable name:** name of the amphibian variable to set.
**Arguments:**

**Example:**
```python
V.n = [52, randint(40, 60), 72, 35]
Pa * d('supersaw', n='(ga n)', p=0.75 )
```

# setscl

The **Sardine Pattern Language** always remember the name of a global scale that the user can set. It defaults to `major`, taken from the [list of possible qualifiers](../sardine/notes.md). You can choose any scale from that list as the default scale for all patterns using **scl**, thus the name of this very function.

**Arguments:**
- **scale_name:** valid scale from the [qualifiers list](../sardine/notes.md). If the name doesn't exist, will default to major.

**Example:**
```python
P('(setscl minor)')
P('(setscl acoustic)')
P('(setscl min9)')
```

