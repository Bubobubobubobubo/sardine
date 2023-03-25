# Player vs @swim function

The are two ways to generate sound from Sardine: 1) Player and 2) @swim functions. They share common features, leverage the same pattern languages, but have a few key differences. It is important to understand both, as well as when and how to use each. Both are used for examples. 

This example will produce the same musical output with Player and @swim:
```python
# Player version
Pa >> d('bd!2 cp hh27:2 . ', speed='1 2', room=0.6, dry=0.2, size=0.5, p='0.5') 

# Swim function version
@swim
def inFive(p=0.5, i=0):
    D('bd!2 cp hh27:2 . ', speed='1 2', room=0.6, dry=0.2, size=0.5, i=i)
    again(inFive, p=0.5, i=i+1)
```

The Player version has a more compact syntax, referred to as "shorthand". Both have Senders with *most* of the same parameters and patterns as arguments. The @swim function is essentially a python function, invoked with the @swim decorator. It can contain multiple Senders, like playing multiple instruments or tracks together. @swim functions are unique with the iterator value "i" and have the period and iterator initiallized first in the function arguments.

### Feature / Syntax comparison
Shows where Player and @swim have different features or syntax. 

| feature | Player |  @swim   | notes              |
|:-------:|:-------:|:--------:|:-------------------|
| Operator    | >> or * | @swim      |    |
| Sender    | d(), n(), etc | D(), N(), etc   |    |
| Multiple Senders | no | yes  |    |
| period    | p=1 or period=1 | p=1   | "period" not valid in @swim |
| iterator  | n/a | i | initialize in function arg: i=i in sender, increment in again(i=i+1) |
| span  | span=1.5 | n/a     | See [Diving Deeper > High Level Patterns](../diving_deeper/high_level_patterns.md) |
| snap  | n/a | snap=-0.5   | See [Diving Deeper > High Level Patterns](../diving_deeper/high_level_patterns.md) |


### Benefits and Uses
Player
- Simplified syntax, often in one line statements
- Good for quick development, experimentation, learning
- Can use multiple players simultaneously - start and stop independantly
- Similar to FoxDot livecoding syntax

@swim function
- Container for more complex constructions. 
- One @swim function can have multiple senders, python statements, amphibian variables, etc
- Iterators control looping. With different values or patterning, can create more variety. 
- One @swim function can control a complete session. 

More advanced @swim function:
```python
@swim
TBD
```

Players can be complex also!
```python 

Pc >> n("vanish(bass(if(every(5) [{[D F|G A|Bb]} [D|G A {D D'}]] {D A}) do=beat(2)) \
     20 do=beat(1))", p='[1 0.5 1 0.25!4]*2', dur=0.1, vel='50~100', d=1, r=1)


```
