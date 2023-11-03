# Filter Functions

There is a group of functions used for filtering: removing events, filtering values, etc... These functions are very low-level but they can be really interesting for specific use cases.

## mask


Apply a boolean mask on values from the collection. True values will return the value itself, others will return a silence. This function is used by others for many different operations.

**Arguments:**
- **collection:** list to be masked by the boolean pattern.
- **bool_pattern:** boolean pattern to apply on the collection.

**Example:**
```python
# Filtering the hihats using a boolean pattern
Pa * d('(mask [kick hat snare hat] [1 0 1 0])', p=.5)
```

## vanish

Vanish will make `x`% of your pattern vanish magically. It is similar to other functions like `degrade` in TidalCycles. Every element from your pattern will be returned (or not) based on a probability.

**Arguments:**
- **collection**: a list containing a pattern to vanish.
- **percentage**: how much the pattern should be degraded

**Example:**
```python
Pa * d('(vanish [kick hat snare hat] 60)', p=.5')
```

## filt

This function can be used to filter some values from a pattern. Imagine generating a 50 elements long list but being stuck with values you would like to get rid of. Using this function, you can remove one or many elements at once.

**Arguments:**
- **collection:** the collection you would like to filter.
- **filter:** a list containing the elements to filter

**Example:**
```python
# Removing 2 and 4 from the generated ramp
Pa * d('hat', p=.25, speed='(filter [0:10] [2 4])')
```


## filtdot

This function can be used to filter out some values from a pattern, replacing them with silences (.).

**Arguments:**
- **collection:** the collection you would like to filter.
- **filter:** a list containing the elements to filter

**Example:**
```python
# Replacing 2 and 4 By silences
Pa * d('hat', p=.25, speed='(filtdot [0:10] [2 4])')  # Equivalent to speed='0 1 . 3 . 5 6 7 8 9 10'
```


## keepdot

This function does the opposite of filtdot: only the values that are in the given filter are kept.

**Arguments:**
- **collection:** the collection you would like to filter.
- **filter:** a list containing the elements to keep

**Example:**
```python
# Replacing 2 and 4 By silences
Pa * d('hat', p=.25, speed='(keepdot [0:10] [2 4])')  # Equivalent to speed='. . 2 . 4 . . . . . .'
```
