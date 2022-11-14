**Sardine** users refer to the functions they use as *swimming functions*. This section will help you to grow more confident using them! *Swimming functions* must dance before your eyes like sardines in the ocean. You must fell comfortable writing them and manipulating them. These functions are the foundation of **Sardine** and nothing really makes sense without them.

Joking aside, and for those of you who already know how to program, *swimming functions* are temporally recursive functions. These functions run and schedule themselves later in time instead of returning. This is a very primitive but very powerful mechanism that has been harnassed by *live-coders* in multiple programming environments since the inception of that type of computer music performance.

## I - Swimming Functions

### Out-of-time

```python3
S('bd').out()
```

This command will play a single bassdrum with the **SuperDirt** sound engine. We are not currently using a *swimming function*, this event is atomic and non-repeating. It is a one-shot event, a single instruction sent to the **Python** interpreter. We haven't learned anything yet, you don't know anything about **Senders**, *swimming functions*, etc... Just note that these one-letter objects are constantly and repeatedly used to trigger different types of messages. We will need to *pattern* them and to *arrange* or *compose* them in time. You can use **Sender** objects outside of a recursive function. It will work, but you will be *un-timed*, or *out-of-time*, just like your regular **Python** script that doesn't really care about time or about when or how things happen. 

By using **Python** with **Sardine**, you will constantly run into things that either are *timed* or *un-timed*. It can help if you like manipulating only certain parts of your interactive programs with time constraints or if you like to store options and configuration in a part of your script, apart from your musical patterns.

### Swimming

```python3
@swim # or @die
def basic():
    print('I am swimming now!')
    again(basic)

hush(basic) # or panic()
```
This is the most basic and iconic *swimming function* you can write. We could make a sweatshirt out of it. It is just like your regular **Python** function to the exception of two little details : 

- the `@swim` or `@die` decorators.

- the `again`, `anew`, `a` final recursive call.

Behind the stage, the `@swim` decorator will provide all the necessary plumbing to properly handle time and repetition. The `again(...)` function is actually the same thing as `@swim`. It is how the recursion happens, where the function enters the infinite time loop defined by the clock. Updating the function with the `@die` decorator will stop the recursivity, ending the production of sound.

Using `hush(function_name)` or just `hush()` will halt the function execution. There is also `panic()` which is a bit more extreme but needed in some cases where sound doesn't stop after running `hush()`. `hush()` will just stop the function / all functions while `panic()` will do the same but also violently stop every sound sample / synthesizer currently being used. This is useful if you feel that you are loosing control when playing with loud or very long samples.


### Swimming with style

```python3
@swim 
def basic(d=0.5, i=0):
    print('I am swimming now!')
    again(basic, d=0.5, i=i+1)

hush(basic)
```

This is a *swimming function* with some minor improvements. The function is passed a duration (`d`) and an iterator (`i`) as arguments. This is the function you will want/need to save as a snippet somewhere in your text editor. **Sardine** users write this skeleton constantly, mechanically, without even thinking about it.

- The `d` parameter is the function's **duration**,  the `0.5` value representing half of a beat.  

- The `i` parameter is an hand-crafted **iterator**, progressively incremented by recursion. Don't be scared by all this jargon. It just means that the value increases by one each time the function is repeated.

### Drowning in numbers

```python3
@swim 
def basic(d=0.5, i=0, j=0, k=0):
    print(f'I am swimming with {i}, {j}, and {k}!')
    again(basic, d=0.5, i=i+1, j=j+2, k=P('r*10', i))

hush(basic)
```

A function with three different iterators. Why not? Notice how the iterator values are evolving independently. `i` is a basic increment, while `j` walks through even numbers. And `k` is randomized using the notation `P('r*10', i)`. To learn more about this, please refer to the section about Patterns and about the pattern Language. You will sometimes encounter features you don't know about yet while scrolling through these examples. Don't worry, they are covered somewhere!
 
### Swimming with friends

```python3
def calling_you():
    print('I hear you')

@swim 
def basic():
    calling_you()
    again(basic)

hush(basic)
```
A swimming function can call a regular function (*i.e.* a function with no **Sardine** decorator). This example is boring as hell but it demonstrates one thing: **Sardine** is just regular **Python** with a twist. Be creative, import your favorite packages and make your computer crash in rhythm!

### Synchronized Swimming

```python3
@swim
def first():
    print('first!')
    again(second)
def second():
    print('second!')
    again(first)
```
A *swimming function* calling another one, which will call back the first one in return. This is a loop of looping functions. You can make use of this to organise longer pieces if you'd like to.

### Sardines playing Waterpolo

```python3
@swim
def first(d=0.5, rng=0):
    print(f"Received: {rng}")
    rng = randint(1,10)
    print(f"Sending: {rng}")
    again(second, d=0.5, rng=rng)

# evaluate me first
def second(d=0.5, rng=0):
    print(f"Received: {rng}")
    rng = randint(1,10)
    print(f"Sending: {rng}")
    again(first, d=0.5, rng=rng)
```
Exchanging data between *swimming functions* just like sardines playing waterpolo. This is just an extension of some on the materials depicted above. There is no limit to the things you can do by recursion. It will only gradually cause more headaches as you go along.

## II - Surfing: concise syntax

There is an alternative jam-oriented way of using *swimming functions* inspired by [FoxDot](https://foxdot.org/), another very cool *live-coding* library for **Python** created by [Ryan Kirkbride](https://ryan-kirkbride.github.io/). This technique is an *emulation* or *simulation* of **FoxDot** mode of operation. It uses the same syntax and the same philosophy of patterning but it relies on **Sardine**'s foundations. This mode of *swimming* is basically assigning **Senders** to an invisible *swimming function* that runs automatically behind your back. 

!!! warning 

    If you don't know yet what a **Sender** is, you better go consult the page about it first before reading this section.

### Surfboards (Players)

By default, there are 48 `Players` ready for surfing. This is more than you will ever need! Nobody can play with that many patterns live. They are named in a consistent way from `Pa`, to `PZ`: `[Pa, Pb, Pc, Pd, Pe, Pf, ..., PA, PB, PC, ... PZ]`. These objects use a central method: `>>`. Just like anything else with **Sardine**, you can also fine-tune your patterns with some setters that will alter how the pattern is interpreted by the clock. We will use `Pa` for demonstration purposes:

* `Pa.rate`: time spent on a single event in a linear sequence of events (step speed).
* `Pa.dur`: duration of a single event in a linear sequence of events (step duration).

While playing/patterning with *surfboards*, you will only ever need to deal with these three methods. All the rest is integrated with the rest of the **Sardine** ecosystem: 

```python
# The sun is high, let's go surfing
Pa >> play('bd, ., hh')
Pa.rate = 1

# Ok, I'm done surfing for today.. Time to eat marshmallows..
hush()
```

In addition to that, take note of the `play()` method used for assigning a **Sender** to **Players**. There is one method per available default **Sender**. It behaves **exactly like your typical senders**:

* `play(*args, **kwargs)`: the default **SuperDirt** (or **S**) Sender.
* `play_midi(*args, **kwargs)`: the default **MIDI** (or **M**) Sender.
* `play_osc(*args, **kwargs)`: the default **OSC** (or **O**) Sender.
* `run(func: Callable)`: run any function like if it was a surfboard!

I repeat, these functions are basically senders with a different name! You will have to learn how to use **Senders** to be truly efficient with the surfing mode. You can spend your life using **Sardine** this way or combine it with *swimming functions*, this is entirely up to you! This mode was initially designed in order to demonstrate the syntax of [FoxDot](https://foxdot.org). I find it to be a fun and efficient way to jam along with friends as well :) You can just fire up a **Sardine** session and write pretty fast.

### The efficiency of surfing

```python
PB >> play('jvbass:r*8, ..., pluck, ...')
PA >> play('bd, ., hh, sn, hh', 
        amp=0.4,
        legato='0.3~1', speed='1')
```
By using the `play()` method and combining it with regular patterns, you can more quickly generate efficient drum patterns without having to type too much! Your drum patterns will only take a few lines, and more complex *swimming functions* can be reserved for more complex tasks.

### Surfing on MIDI Cables

```python
PA >> play_midi('<C@maj7>', dur='1~8')
PA.dur = 3
PB >> play_midi("C.., C|C'|C''", dur='1~8')
PB.rate = 2
```
The `play_midi()` function is the good old `M()` **Sender**. The `note=` parameter has been promoted to an *arg* in this mode in order to save you from having to type 5 more letters :)

### How to stop surfing

**Surfing** patterns are fully integrated with the rest of **Sardine**. You can shut them down by calling the `hush()` or `panic()` function just like for other *swimming functions*.
```python
PA >> play('bd, ., hhh, .')
PA.rate = 1

hush()
```


## III - Fast swimming functions

This section requires a good understanding of general **Sardine** concepts. You need to understand **patterns**, **senders**, and a few other concepts. You need to have at least a very vague idea about the temporal system **Sardine** is using and how patterns are written/interpreted, etc... It will open up a very cool world of polyrythmic patterns, rhythmic divisions, etc...

### Swimming at clock speed

```python

@swim 
def fast(d=0.25, i=0):
    S('bd', speed='0.5,2', legato=0.1).out(i, div=4, rate=2)
    S('hh, jvbass:0|8|4,', 
            pan='[0:1,0.1]',
            legato=0.1).out(i, div=8 if rarely()
                    else 5, rate=2)
    S('cp', legato=0.1).out(i, div=8)
    a(fast, d=1/8, i=i+1)
```
**Sardine** *swimming functions* are usually slow (compared to the clock internal speed). However, you can speed up your recursion, the only hard limit being the speed at which the clock itself operates. It means that the faster you go, the better the rhythmic precision. The faster, the merrier! You will be able to have a finely grained control over time and events, with the ability to write more groovy or swinging code. It will also make your LFOs and signal-like patterns sing more. 

The recipe for *fast swimming* is the following:

- Use a very fast recursion speed (`1/8`, `1/16`, `1/32`), usually constant (no patterning).

- Play a lot with silences and with the arguments of `.out(iterator, div, rate)`. 

### Fast swimming template

```python
@swim 
def fast(d=0.5, i=0):
    # print("Damn, that's fast!")
    a(fast, d=1/32, i=i+1)
```
This is the template for a fast *swimming function*. You can skip the iterator if you don't need it or if you wish to use another iteration tool (such as **amphibian variables**). This function is really fast. Uncomment the `print` statement to notice how fast it is. To learn how to control it efficiently, take a look at the following paragraphs about *divisors* and the *rate* factor.

### Fast swimming parameters

```python

@swim 
def fast(d=0.5, i=0):
    S('bd').out(i, div=8)
    a(fast, d=1/16, i=i+1)
```
The `.out()` method as well as the independant `P()` [object](#patterning-freely-p) can take up to three arguments:

- `i` (*int*): the iterator for patterning. **Mandatory** for the two other arguments to work properly. This **iterator** is the index of the values extracted from your linear list-like patterns. How this index will be interpreted will depend on the next two arguments.

- `div` (*int*): **a timing divisor**. It is very much alike a modulo operation. If `div=4`, the event will hit once every 4 iterations. The default is `div=1`, where every event is a hit! Be careful not to set a `div=1` on a very fast *swimming function* as it could result in catastrophic failure / horrible noises. There is no parachute out in the open sea.

- `rate` (*float*): a speed factor for iterating over pattern values. It will slow down or speed up the iteration speed, the speed at which the pattern values are indexed on. For the pattern `1, 2, 3` and a rate of `0.5`, the result will be perceptually similar to `1, 1, 2, 2, 3, 3`.

Let's illustrate. In the example below, we are playing with various divisors to generate an interesting rythmic pattern. Combine that with more interesting drumming and boom, you now have the secret recipe for an interesting [algorave](https://algorave.com/).

```python
@swim 
def fast(d=0.5, i=0):
    S('bd').out(i, div=8)
    S('hh').out(i, div=7)
    S('sd').out(i, div=16)
    a(fast, d=1/16, i=i+1)
```

### Can we do more?

Of course we can. So far, we only used one patterning speed because every **sender** is iterating over all its patterns at the same speed but you could use the `P()` object for including different iteration speeds inside your main fast swimming rhythm. This is a bit jargon heavy but I hope that you will understand what I mean. If you don't, see for yourself:

```python
c.bpm = 125
@swim 
def there_is_a_light(d=0.5, i=0):
    S('drum', legato=1, speed='1').out(i, 8)
    S('drum:[1,2,3,4]', legato=1, 
        speed=P('1,2,3,4,5,1!2,4!4', i+1, 2, 0.5)).out(i, 4)
    a(there_is_a_light, d=1/8, i=i+1)
```
Go slow, read line after line and you will eventually get it!


## Conclusion about swimming

The concept of temporal recursion is deep. There are many clever things you can do with it, and it might take some time to see and master different patterning techniques. *Swimming functions* are only the beginning to your temporal voyage with **Sardine** because you will notice that there are multiple ways to speak / think about time even in the context of this very generic framework. Let's go through some examples really quick to whet your appetite.

### Imperative style

Take a *swimming function*, make it long enough, use our very special `sleep()` function (which is not the regular **Python** sleep) and you can write code *à la* [Sonic Pi](https://sonic-pi.net/):

```python
@swim
def sonorous_cake(d=0.5, i=0):
    S('bd').out()
    sleep(0.5)
    S('hh').out()
    sleep(0.5)
    S('bd').out()
    sleep(0.5)
    S('sn').out()
    a(sonorous_cake, d=2, i=i+1)
```

### Declarative style

Make your *swimming functions* very dense, write using a mostly declarative style. Spice it up with the patterning system if you'd like:
```python
@swim
def one_line(d=0.5, i=0):
    S('bd, drum, sn, drum:2').out(i)
    a(one_line, d=0.5, i=i+1)
```
