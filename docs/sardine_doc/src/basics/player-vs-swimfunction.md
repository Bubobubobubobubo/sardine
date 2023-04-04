# Player vs @swim function

The are two ways to generate patterns with Sardine: 
1) `@swim` functions: the fundamental mechanism.
1) `Player`: a shorthand syntax to use it.

They share common features, leverage the same pattern languages, but have a few key differences. It is important to understand both, as well as when and how to use each. You will find that using one syntax or the other is more appropriate depending on the what you are trying to do. 

This example will produce the same musical output with Player and @swim:
```python
# Player version
Pa * d('bd!2 cp hh27:2 . ', speed='1 2', 
       room=0.6, dry=0.2, size=0.5, p='0.5') 

# Swim function version
@swim
def inFive(p=0.5, i=0):
    D('bd!2 cp hh27:2 . ', speed='1 2',
      room=0.6, dry=0.2, size=0.5, i=i)
    again(inFive, p=0.5, i=i+1)
```

The **Player** version has a more compact syntax, referred to as *shorthand*. Both have Senders with most of the same parameters and patterns as arguments. The `@swim` function is essentially a Python function, invoked with the `@swim` decorator. It can contain multiple Senders, like playing multiple instruments or tracks together. `@swim` functions are unique with the iterator value **i** and have the **period** and **iterator** initiallized in the function arguments.

### Feature / Syntax comparison

Here is a short comparison of the **Player** syntax against the **@swim** syntax:

| Feature | Player |  @swim   | notes              |
|:-------:|:-------:|:--------:|:-------------------|
| **Operator**    | `>>` or `*` | `@swim`      | Functions take a decorator, Players use an operator.   |
| **Sender**    | d(), n(), ...| D(), N(), ...| Uppercase against lowercase.   |
| **Multiple Senders** | no | yes  | Players can only play **one pattern** at the same time. |
| **period**    | `p=1` or `period=1` | `p=1`   | `period` not valid in @swim |
| **iterator**  | Implicit | Explicit | For `@swim`, iterator control is manual. Initialize it in function args: `i=i`, increment it in the final recursive call: `again(i=i+1)` |
| **span**  | span=1.5 | n/a     | See [Diving Deeper > High Level Patterns](../diving_deeper/high_level_patterns.md) |
| **snap**  | `snap=-0.5` | `snap=-0.5`   | See [Diving Deeper > High Level Patterns](../diving_deeper/high_level_patterns.md) |


### Benefits and Uses

Each technique has some benefits and some downsides.

**Players:**
- Simplified friendly syntax: often one line statements.
- Good for quick development, experimentation, learning.
- Multiple players can be used simultaneously.
- Each player can start and stop independantly.
- Similar to the well-known syntax of [FoxDot](https://github.com/Qirky/FoxDot).
- Complex patterns can be harder to understand on a single line. 

**@swim functions:**
- Containers for more complex constructions. 
- One `@swim` function can have multiple senders, Python statements, etc...
- Manual control over looping through iteration.
  - With different values or iteration methods, more creative patterns can be found.
- One `@swim` function can control a complete session. 
- More suited for adding custom python code. 


## Demo

### Complex swimming function

Here is a more advanced `@swim` function. Notice how it spans over multiple lines and contains a large group of independent senders. This function is playing many synths at the same time and also controls drumming!

```python
@swim
def tran(p=0.5, i=0):
    D('(eu braids 5 8)', n='C2', model=9, lpf=500, i=i, timbre='0.5')
    D('(eu braids 7 8)', n='C4|C3', model=9, lpf='rand*4000', i=i, timbre='0.5')
    ZD('braids', '<0 7> (2,8)', 
       scale='minor', model=9, lpf='((sin $)/2)*2000', i=i, timbre='0.5', leg=1.5)
    ZD('braids', '_ <0 7> (2,8) [0 ^5]', 
       scale='minor', model=9, lpf='((sin $)/2)*4000', i=i, timbre='0.5', leg=1.5)
    ZD('braids', '_ <0 3> (2,8) [0 ^7]', 
       scale='minor', model=12, lpf='((sin $)/2)*5000', i=i, timbre='0.5', leg=1.5)
    D('hkick ...', i=i)
    D('..  hsnare:8 .', r=0.75, i=i, lpf=4000, amp=0.1)
    again(tran, p=0.5, i=i+1)
```

### Complex player function

Players can also be used to generate complex patterns but notice how you quickly loose in readability! It is better to limit the usage of Players to single tasks (one instrument, one musical part). They are easier to control individually.

```python 

Pc >> n("vanish(bass(if(every(5) [{[D F|G A|Bb]} [D|G A {D D'}]] {D A}) do=beat(2)) \
     20 do=beat(1))", p='[1 0.5 1 0.25!4]*2', dur=0.1, vel='50~100', d=1, r=1)


```
