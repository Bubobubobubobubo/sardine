**Sardine** users refer to the functions they use as **swimming functions**. This section will teach you how to use them! *Swimming functions* must dance before your eyes like sardines in the ocean. You must fell comfortable writing them and manipulating them. These functions are the foundation of **Sardine** and nothing really makes sense without them.

Joking aside, and for those of you who already know how to program, **swimming functions** are temporally recursive functions. These functions run and schedule themselves later in time instead of returning. This is a very primitive but very powerful mechanism that has been harnassed by *live-coders* in multiple programming environments since the inception of that type of computer music performance.

## I - Swimming Functions

### Out-of-time

```python3
D('bd')
```

This command will play a single bassdrum with the **SuperDirt** sound engine. We are not currently using a *swimming function*, this event is atomic and non-repeating. It is a one-shot event, a single instruction sent to the **Python** interpreter. We haven't learned anything yet, you don't know anything about **Senders**, *swimming functions*, etc... Just note that these one-letter objects are constantly and repeatedly used to trigger different types of messages. We will need to *pattern* them and to *arrange* or *compose* them in time. You can use **Sender** objects outside of a recursive function. It will work, but you will be *un-timed*, or *out-of-time*, just like your regular **Python** script that doesn't really care about time or about when or how things happen.

By using **Python** with **Sardine**, you will constantly run into things that either are *timed* or *un-timed*. It can help if you like manipulating only certain parts of your interactive programs with time constraints or if you like to store options and configuration in a part of your script, apart from your musical patterns.

### Swimming

```python3
@swim # or @die
def basic():
    print('I am swimming now!')
    again(basic)

silence(basic) # or panic()
```
This is the most basic and iconic *swimming function* you can write. We will surely make a sweatshirt out of it one day. It is just like your regular **Python** function to the exception of two little details:

- the `@swim` or `@die` decorators.

- the `again` final recursive call.

Behind the stage, the `@swim` decorator will provide all the necessary plumbing to properly handle time and repetition. The `again(...)` function is pretty much the same thing as `@swim`. It is how the recursion happens, where the function enters the infinite time loop defined by the clock. Updating the function with the `@die` decorator will stop the recursivity, ending the production of sound.

Using `silence(function_name)` or just `silence()` will halt the function execution. There is also `panic()` which is a bit more extreme but needed in some cases where sound doesn't stop after running `silence()`. `silence()` will just stop the function / all functions while `panic()` will do the same but also violently stop every sound sample / synthesizer currently being used. This is useful if you feel that you are loosing control when playing with loud or very long samples.


### Swimming with style

```python3
@swim
def basic(p=0.5, i=0):
    print('I am swimming now!')
    again(basic, p=0.5, i=i+1)

silence(basic)
```

This is a *swimming function* with some minor improvements. The function is passed a period (`p`) and an iterator (`i`) as arguments. This is the function you will want/need to save as a snippet somewhere in your text editor. **Sardine** users write this skeleton constantly, mechanically, without even thinking about it.

- The period (`p`) is the function's **duration**, the `0.5` value representing half of a beat.

- The `i` parameter is an hand-crafted **iterator** progressively incremented by recursion. Don't be scared by all this jargon. It just means that the value increases by one each time the function is repeated.

### Drowning in numbers

```python3
@swim
def basic(p=0.5, i=0, j=0, k=0):
    print(f'I am swimming with {i}, {j}, and {k}!')
    again(basic, p=0.5, i=i+1, j=j+2, k=P('rand*10', i))

silence(basic)
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

silence(basic)
```
A *swimming function* can call a regular function (*i.e.* a function with no **Sardine** decorator). This example is boring as hell but it demonstrates one thing: **Sardine** is just regular **Python** with a twist. Be creative, import your favorite packages and make your computer crash in rhythm!

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
def first(p=0.5, rng=0):
    print(f"Received: {rng}")
    rng = randint(1,10)
    print(f"Sending: {rng}")
    again(second, p=0.5, rng=rng)

# evaluate me first
def second(p=0.5, rng=0):
    print(f"Received: {rng}")
    rng = randint(1,10)
    print(f"Sending: {rng}")
    again(first, p=0.5, rng=rng)
```
Exchanging data between *swimming functions* just like sardines playing waterpolo. This is just an extension of some on the materials depicted above. There is no limit to the things you can do by recursion. It will only gradually cause more headaches as you go along.

## II - Surfing with surfboards: a concise syntax

Sardine features an alternative *swimming function* based mechanism called *surfboards*. *Surfboards* are inspired by [FoxDot](https://foxdot.org/), another cool *live-coding* library for **Python** created by [Ryan Kirkbride](https://ryan-kirkbride.github.io/). Surfboards are great for quick improvisation or for jotting down ideas before composing something larger using *swimming functions*. They also have some features not to be found anywhere else in the system for working with proportional durations, etc... It uses the same syntax and the same philosophy of patterning but it relies on **Sardine**'s temporal foundations. This mode of *swimming* is basically assigning **Senders** to an invisible *swimming function* that runs automatically behind your back.

### Surfboards (Players)

By default, there are 48 `Players` ready for surfing. This is more than you will ever need! Nobody can play with that many patterns live. They are named in a consistent way from `Pa`, to `PZ`: `[Pa, Pb, Pc, Pd, Pe, Pf, ..., PA, PB, PC, ... PZ]`. These objects use a central method: `>>`. In the background, `Players` are just regular *swimming functions*. They are limited as they can only have one call to a `Sender` per instance but this is sometimes more than enough!

```python
# The sun is high, let's go surfing
Pa >> d('bd, ., hh')

# Ok, I'm done surfing for today.. Time to eat marshmallows..
Pa >> None # use none to stop a player
```

Take note of the `d()` method used for assigning a **Sender** to **Players**. If you have already played with Sardine or watched some videos, you might recognize `d()` from its cousin, `D()`. By default, I have mirrored every basic `Sender` with its own method usable by surfboards.

* `d(*args, **kwargs)` (`D()`): the default **SuperDirt** (or **D**) Sender.
* `n(*args, **kwargs)` (`N()`): the default **MIDI Note** (or **N**) Sender.
* `cc(*args, **kwargs)` (`CC()`): the default **MIDI Control Change** (or **CC**) Sender.
* `pc(*args, **kwargs)` (`PC()`): the default **MIDI Program change** (or **PC**) Sender.
* ... any other sender that you will declare yourself!

I repeat, these functions are basically senders with a different name! Uppercase letters versus lowercase letters. You need to learn how to use **Senders** to be truly efficient with the surfing mode. You can spend your life using **Sardine** this way or combine it with *swimming functions*, this is entirely up to you! This mode was initially designed in order to demonstrate the syntax of [FoxDot](https://foxdot.org). I find it to be a fun and efficient way to jam along with friends as well :) You can just fire up a **Sardine** session and write pretty fast.

Note that it is very easy to define your own `Senders`. To do so, follow the following steps:

1) Declare a new Sender. For demonstration purposes, we will open a new MIDI output.

```python
my_super_midi_sender = MidiHandler(port_name="my_cool_midi_output")
bowl.add_handler(midi)
```

2) Reference the `send` function from that sender with a variable

```python
cool_sender = my_super_midi_sender.send
```

3) Compose a partial function following this template:

```python
def custom_sender(*args, **kwargs):
    return play(my_super_midi_sender, cool_sender, *args, **kwargs)
```

4) You can now use *surfboards* and have fun:

```
Pa >> custom_sender(...)
```

### The span argument

*Surfboard* are featuring a special `span` argument that will extend or compress the time taken for a pattern to be read. It is actually quite similar to `p` (for `period`) but it will also transform every value you feed to `p`. It can be quite hard to understand how this mechanism works initially. This has to do with the way we think about time and rhythm.

The `span` argument can receive any integer or floating point number. That number will determine **how long** a surfboard pattern is and this value is **absolute**. Once you set it, your pattern will always cover that specific **timespan**. If you have a pattern of durations (`p`), they will be compressed or extended to **fit** that timespan. Take a look at the following example:

```python
Pa >> d('bd, hh', p='0.5!4, 0.25!4', span=2)
# Change the span value and observe
```

You can mix *surfboards* with different spans, but you might not like what you hear depending on the rhythm you have previously specified.

### The efficiency of surfing

```python
PB >> d('jvbass:rand*8, ..., pluck, ...')
PA >> d('bd, ., hh, sn, hh',
        amp=0.4,
        legato='0.3~1', speed='1')
```
By using the `d()` method and combining it with regular patterns, you can more quickly generate efficient drum patterns without having to type too much! Your drum patterns will only take a few lines, and more complex *swimming functions* can be reserved for more complex tasks.

## III - Fast swimming functions

This section requires a good understanding of general **Sardine** concepts. You need to understand **patterns**, **senders**, and a few other concepts. You need to have at least a very vague idea about the temporal system **Sardine** is using and how patterns are written/interpreted, etc... It will open up a very cool world of polyrythmic patterns, rhythmic divisions, etc...

### Swimming really fast

The recursion you define in a *swimming function* is usually rather slow compared to how fast your computer is running the asynchronous loop. If you feel adventurous, you can speed up the recursion and enter the high speed zone. The faster you go, the better the rhythmic precision. The faster, the merrier! Fast *swimming functions* will allow you to have a finely grained control over time and events, making it easier to generate groovy or swinging code. It will also make your LFOs and signal-like patterns feel more natural as they will be sampled more frequently.

```python
@swim
def fast(p=0.25, i=0):
    D('bd', speed='0.5,2', legato=0.1, i=i, d=4, r=2)
    D('hh, jvbass:(0|8|4)',
            pan='[0:1,0.1]', legato=0.1,
            i=i, r=2, d=8 if rarely() else 5)
    D('cp', legato=0.1, i=i, d=8)
    again(fast, p=1/8, i=i+1)
```

The recipe for *fast swimming* is the following:

- Use a very fast recursion speed (`1/8`, `1/16`, `1/32`), usually a constant with no patterning involved.

- Play a lot with silences and with the *iterator*, *division amount* and *rate factor*. These special arguments will be detailed in this section!

### Fast swimming template

```python
@swim
def fast(p=0.5, i=0):
    # print("Damn, that's fast!")
    again(fast, p=1/32, i=i+1)
```

This is the template for a fast *swimming function*. You can skip the iterator if you don't need it or if you wish to use another iteration tool (such as **amphibian variables**). This function is really fast. Uncomment the `print` statement to notice how fast it is. To learn how to control it efficiently, take a look at the following paragraphs about *divisors* and the *rate* factor.

### Fast swimming parameters

```python

@swim
def fast(p=0.5, i=0):
    D('bd', i=i, d=8)
    again(fast, d=1/16, i=i+1)
```
Every `Sender` can receive three additional arguments that will help you to control patterns:

- `i` (*int*): the iterator for patterning. **Mandatory** for the two other arguments to work properly. This **iterator** is the index of the values extracted from your linear list-like patterns. How this index will be interpreted will depend on the next two arguments.

- `div` (*int*): **a timing divisor**. It is very much alike a modulo operation. If `div=4`, the event will hit once every 4 iterations. The default is `div=1` where every event is a hit! Be careful not to set a `div=1` on a very fast *swimming function* as it could result in catastrophic failure / horrible noises. Nobody is going to come to save you if you do that. Keep the volume knob close to your keyboard.

- `rate` (*float*): a speed factor for iterating over pattern values. It will slow down or speed up the iteration speed, the speed at which the pattern values are indexed on. For the pattern `1, 2, 3` and a rate of `0.5`, the result will be perceptually similar to `1, 1, 2, 2, 3, 3`.

Let's illustrate. In the example below, we are playing with various divisors to generate an interesting rythmic pattern. Combine that with more interesting drumming and boom, you now have the secret recipe for an interesting [algorave](https://algorave.com/).

```python
@swim
def fast(p=0.5, i=0):
    D('bd', i=i, d=8)
    D('hh', i=i, d=7)
    D('sd', i=i, d=16)
    again(fast, p=1/16, i=i+1)
```

### Can we do more?

Of course we can. So far, we only used one patterning speed because every **sender** is iterating over all its patterns at the same speed. You could use the `P()` object for including different iteration speeds inside your main fast swimming rhythm. This is a bit jargon heavy but I hope that you will understand what I mean. If you don't, see for yourself:

```python
clock.tempo = 125
@swim
def there_is_a_light(p=0.5, i=0):
    D('drum', legato=1, speed='1', i=i, d=8)
    D('drum:[1,2,3,4]', legato=1,
        speed=Pat('1,2,3,4,5,1!2,4!4', i+1, 2, 0.5), i=i, d=4)
    again(there_is_a_light, p=1/8, i=i+1)
```
Go slow, read line after line and you will eventually get it! Patterns can become abstract quite fast.

## Conclusion about swimming

The concept of temporal recursion is deep. There are many clever things you can do with it, and it might take some time to see and master different patterning techniques. *Swimming functions* are only the beginning to your temporal voyage with **Sardine**. You will notice that there are multiple ways to speak / think about time even in the context of this very specific framework. Let's go through some examples really quick to whet your appetite.

### Imperative style

Take a *swimming function*, make it long enough, use our special `sleep()` function (which is not the regular **Python** sleep) and you can write code *à la* [Sonic Pi](https://sonic-pi.net/):

```python
@swim
def sonorous_cake(p=0.5, i=0):
    D('bd')
    sleep(0.5)
    D('hh')
    sleep(0.5)
    D('bd')
    sleep(0.5)
    D('sn')
    again(sonorous_cake, p=2, i=i+1)
```

### Declarative style

Make your *swimming functions* very dense, write using a mostly declarative style. Spice it up with the patterning system if you'd like:
```python
@swim
def one_line(p=0.5, i=0):
    D('bd, drum, sn, drum:2')
    again(one_line, p=0.5, i=i+1)
```
