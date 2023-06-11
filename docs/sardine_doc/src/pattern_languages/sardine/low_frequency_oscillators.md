# Low Frequency Oscillators

These functions are implementing low-frequency oscillators whose period is based on a selectable number of clock beats. They offer another better flavor to the basic technique that works by manually calculating stuff using `sin()` or `cos()` functions. 

# lsin

This is a bipolar (`-1` to `1`) sinusoïdal low frequency oscillator that you can use for modulations in any pattern.

**Arguments:**
- **period:** frequency expressed in clock beats.

**Example:**
```python
(lsin 4)
```
# ltri


This is a bipolar (`-1` to `1`) triangular low frequency oscillator that you can use for modulations in any pattern.
**Arguments:**
- **period:** frequency expressed in clock beats.

**Example:**
```python
(ltri 4)
```

# lsaw

This is a bipolar (`-1` to `1`) sawtooth low frequency oscillator that you can use for modulations in any pattern.


**Arguments:**
- **period:** frequency expressed in clock beats.

**Example:**
```python
(lsaw 4)
```

# lrect

This is a bipolar (`-1` to `1`) rectangular low frequency oscillator that you can use for modulations in any pattern.


**Arguments:**
- **period:** frequency expressed in clock beats.
- **pwm:** pulse width modulation (number between `0` and `1`).


**Example:**
```python
(lrect 4 0.2)
```

# ulsin

This is an unipolar (`0` to `1`) sinusoïdal low frequency oscillator that you can use for modulations in any pattern.

**Arguments:**
- **period:** frequency expressed in clock beats.



**Example:**
```python
(ulsin 3)
```

# ultri

This is an unipolar (`0` to `1`) triangular low frequency oscillator that you can use for modulations in any pattern.

**Arguments:**
- **period:** frequency expressed in clock beats.



**Example:**
```python
(ultri 3)
```

# ulsaw

This is an unipolar (`0` to `1`) sawtooth low frequency oscillator that you can use for modulations in any pattern.

**Arguments:**
- **period:** frequency expressed in clock beats.


**Example:**
```python
(ulsaw 3)
```

# What to do with Low Frequency Oscillators?

Remember that you can do math operations on these oscillators such as clamping (`clamp`), scaling (`scale`), etc. You can also pattern the `period` or `pwm` for extra weirdness or for doing custom shapes. Folding and wrapping operations can be very useful to generate interesting shapes on a large time scale. 

Modulations are extremely important to get dynamic sounding patterns.
