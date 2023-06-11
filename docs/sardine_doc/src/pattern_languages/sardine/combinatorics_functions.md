# Combinatorics

This category of functions is containing many functions that perform many simple but important operations on lists.

# rev

Reverse a list.

- **Arguments:**
  - **None**

**Example:**
```python
(rev 1 2 3 [1 2 3])
```

# pal

Creates a palindrome. This will keep the list as is but will also append the list in reverse.

- **Arguments:**
  - **cut:** whether to repeat the last/first value of reversed list or not.

**Example:**
```python
(pal [1:10] ::cut 1) # or ::cut 0
```

# shuf

Shuffle any list.

Description ...
- **Arguments:**
  - **None**

**Example:**
```python
(shuf 1 2 3 4 5)
```

# leave

Braid multiple lists of uneven length.

- **Arguments:**
  - **...:** feed multiple lists to braid them together.

**Example:**
```python
(leave [1 2 3] [3 4 5] [1 2] [4 8 6 4])
```

# insertp

Insert a fixed element as pair element of each list.

- **Arguments:**
  - **None**

**Example:**
```python
```

# insert

Insert a fixed element as odd element of each list.

- **Arguments:**
  - **None**

**Example:**
```python
```

# insertprot

Description ...

- **Arguments:**
  - **None**

**Example:**
```python
```

# insertrot
# aspeed
