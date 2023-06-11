# Mathematical

Simple mathematical functions that can be applied on any numeric expression. They are very often the typical generic operations that you can find on digital calculators:

## sin

Apply the sinus function to all the provided arguments.

**Arguments**:
- **...** (any number of arguments)

**Example:**
```python
(sin 1 2 3)
(sin time)
```

## usin

Unipolar version of the sin function.

**Arguments**:
- **...** (any number of arguments)

**Example:**
```python
(usin 1 2 3)
(usin time)
```

## cos

Apply the cosinus function to all the provided arguments.

**Arguments**:
- **...** (any number of arguments)

**Example:**
```python
(cos 4 5 6)
(cos bar)
```

## ucos

Unipolar version of the cos function.

**Arguments**:
- **...** (any number of arguments)

**Example:**
```python
(cos 4 5 6)
(cos bar)
```

## tan

Apply the tangent function to all the provided arguments.

**Arguments**:
- **...** (any number of arguments)

**Example:**
```python
(tan (abs -0.25))
(tan (sin (time)))
(tan 2)
```

## saw

Sawtooth wave generator, in a range from `-1` to `1`.

**Arguments**:
- **...** (any number of arguments)

**Example:**
```python
(saw (time))
(saw (phase))/4
```

## usaw

Unipolar variant (from `0` to `1`) of the saw function.

**Arguments**:
- **...** (any number of arguments)

**Example:**
```python
(usaw (time))
(usaw (phase))/4
```

## rect

Square wave generator, in a range from `-1` to `1`. The pulse width can be modulated using a special argument.

**Arguments**:
- **...** (any number of arguments)
- **pwm**: pulse width modulation (`0` to `1`).

**Example:**
```python
(rect (time))
(rect (phase))/4
```

## urect

Unipolar variant (from `0` to `1`) of the rect function. The pulse width can be modulated using a special argument.

**Arguments**:
- **...** (any number of arguments)
- **pwm**: pulse width modulation (`0` to `1`).


**Example:**
```python
(urect (time))
(urect (phase))/8
```

## abs

Returns the absolute value of all the provided arguments.

**Arguments**:
- **...** (any number of arguments)


**Example:**
```python
(abs [1:-5, 1])
(abs -10)
```

## max

Returns the maximum value in all the numbers provided as argument.


**Arguments**:
- **...** (any number of arguments)


**Example:**
```python
(max 1 2 3)
(max [rand rand rand rand])
```

## min

Returns the minimum value in all the numbers provided as argument.

**Arguments**:
- **...** (any number of arguments)

**Example:**
```python
(min 1 2 3)
(min [rand rand rand rand])
```

## mean

Returns the mean of all the numbers provided as argument.

**Arguments**:
- **...** (any number of arguments)

**Example:**
```python
(mean 1.5 3 2 10.4)
```

## scale

Scale a number `z` from the range `x` `y` to the range `x1`, `y1`.

**Arguments**:
- **None**

**Example:**
```python
(scale (bar) 0 4 0 10)
```

## clamp 

Clamp a value `a` in between `b` and `c`. This means that the number `a` will be limited and range and will never be able to be set lower than `b` or higher than `c`.

**Arguments**:
- **None**

**Example:**
```python
(clamp 1000 0 127) # -> returns 127
```

## drunk

The drunk walk function will return +1 or -1 to any provided integer with a 50% chance for either of them. It is frequent to see this function used for writing generative melodies or parameter trajectories. This version of drunk also features a keyword argument to specify by how much a step should increment or decrement.

**Arguments**:
- **span:** increment span, from `0` to `x`.

**Example:**
```python
(drunk (get a) ::span 4) # -> returns 127
```

**More examples and application:**

```python
@swim
def demo(p=1/4, i=0):
    D('moog:5', lpf='(sin (time)*2500)', res='(cos (time))/2', i=i, legato=0.1)
    D('cp', speed='0+(abs -rand*5)', d=8, i=i)
    again(demo, p=1/8, i=i+1)
```   

These functions are the bread and butter of a good high-speed **Sardine** pattern. They will allow you to create **signal-like** value generators (*e.g* **Low frequency oscillators**). They are also very nice to use in conjunction with `(time)` or any time function. You will find many creative ways to use them (especially by combining with arithmetic operators).
