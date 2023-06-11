# Time Functions

This type of functions is all about returning information about the current time. This timing information can either refer to the wall clock (the real world time) or to the Sardine Clock (internal representation of time). It will sometimes refer to musical time, sometimes to *'time as we know it'*.

## time

This function returns wall clock time, spanning from the current year down to microseconds. It takes zero or one argument, the type of time you want to see returned.

**Arguments:**
- `data`: `year`, `month`, `day`, `minute`, `second`, `micro`. If `data` is not given, will return the current internal time of the **Sardine** clock.

**Example:**
```python
P('(time year)')
```

## bar

This function returns current the current bar (as integer).

**Arguments:** 
- **None**

**Example:**
```python
P('(bar)')
```

## phase

This function returns current the current phase (as float).

**Arguments:** 
- **None**

**Example:**
```python
P('(phase)')
```

## beat

This function returns current the current beat (as float).

**Arguments:** 
- **None**


**Example:**
```python
P('(beat)')
```

## unix

This function returns current the current Unix Time (as integer) because why not! It can be used as a cool random number generator or as an incrementer.

**Arguments:** 
- **None**

**Example:**
```python
P('(unix)')
```
