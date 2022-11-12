## The importance of patterning 

By nature, *swimming functions* are repetitive. Almost everything you play with is falling into a time loop. Strict repetition can be come pretty boring after a while, and you need to find a way to define events that will gradually change in time, whether it is because they are sequence of events, random events, mutating events, etc... Sequencing and patterning is the big deal for *live-coders*. That's how they think about composition / improvisation, that's how they write interesting music by patterning synthesizers, audio samples, custom events and much more. If you go down the rabbit hole, you can also pattern your patterns. You can also pattern the functions altering your patterns. There is no limit to it, only what you are trying to define and play with.

Thinking about music being composed with patterns, recursion and time loops is a deparature from the timeline / score model we are used to when thinking about music being written on scores or being recorded on tape. By patterning and thinking about loops, we enter into a different relationship with sound materials and the management of musical information. 

It would have been weird to design **Sardine** without taking into account the fact that **patterning** is as much needed as control over the temporal execution of code. **Sardine** is taking some inspiration from [ORCA](https://github.com/hundredrabbits/Orca) (Devine Lu Linvega), [FoxDot](https://github.com/Qirky/FoxDot) (Ryan Kirkbride) and [TidalCycles](https://tidalcycles.org) (Alex McLean and colaborators). These systems, among others, have been designed just like **Sardine** around the idea of patterning values in musical time. They all choose a different route to do so, and come up in exchange with interesting concepts about what an event or even what time is in a musical improvisation system.

### Patterning anything

```python3
@swim
def free(d=0.5, i=0):
    # Look at P
    print(P('1,2,3,4', i))
    again(free, d=0.5, i=i+1)
```
`P()` is an interface to the patterning system. Write a pattern between quotation marks (`''` or `""`) and get something back. You will need to feed the pattern system a value to extract an index (`i`).

### Patterning with Senders

```python3
@swim
def boom(d=0.5, i=0):
    S('bd', 
        cutoff='r*2000',
        speed='1,2,3,4').out(i)
    again(boom, d=0.5, i=i+1)
```
Sender objects are automatically turning string arguments into patterns. Feed the index value to the `.out()` method.

### Dual patterning

```python3
@swim
def boom(d=0.5, i=0):
    S('bd', 
        cutoff=P('r*2000', i),
        speed='1,2,3,4').out(i)
    again(boom, d=0.5, i=i+1)
```
The result of this *swimming function* is strictly similar to the one directly above. Notice the difference in coding style, with the usage of `P()`.

### See me change

```python3
@swim
def boom(d=0.5, i=0):
    S('bd', 
        cutoff=P('r*2000', i),
        speed='1,2,3,4').out(i)
    again(boom, d=0.5, i=i+1 if random() > 0.5 else -1)
```
Playing around with the basic `i` iterator structure.

### Index madness

```python3
@swim
def boom(d=0.5, i=0):
    S('bd', 
        cutoff=P('r*2000, 500, 1000', i%2),
        speed='1,2,3,4').out(randint(1,4))
    again(boom, d=0.5, i=i+1)
```
You can be creative with pattern indexes and get random sequences, drunk walks, reversed sequences, etc... Be sure to always have a few different iterators close by to morph your sequences really fast.

