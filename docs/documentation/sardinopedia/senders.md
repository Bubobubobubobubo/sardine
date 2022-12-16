The second most important aspect of **Sardine** is the concept of **Senders**. **Senders** are the main objects used to communicate with the outside world. There are three basic **senders**:

- **Sound Sender**: play sounds/synths using **SuperCollider** and the **SuperDirt** engine.

- **MIDI Sender**: trigger/control MIDI capable software / hardware.

- **OSC Sender**: send or receive *Open Sound Control* messages.

Naturally, people are thinking about adding more and more senders. Hopefully, **Sardine** will make integrating new **senders** easier as time goes by. For now, these three *I/O* tools cover most of the messages used by *live-coders* and *algoravers*. **Python** packages can be imported to deal with other things that **Sardine** is not yet covering. You can turn the software into an ASCII art patterner or hack your way around to deal with DMX-controlled lights.

You will see that learning how to *swim* was kind of the big deal. Things will now be easier to learn. **Senders** and *swimming functions* are enough to already make pretty interesting music. The rest is just me sprinkling goodies all around :)

## I - Anatomy of Senders

A **Sender** is an *event generator*. It describes one event. This event can mutate depending on multiple factors such as patterns, randomness, chance operations, clever **Python** string formatting, etc... A single sender can be arbitrarily long depending on the precision you want to give to each event. This sender can also take some optional *tail arguments*. Wait? A long function, and tail arguments? Does it ring a bell? It looks... just like a sardine.

```
       /`-._                   /`-._
     _/,.._/                 _/,.._/
  ,-'   ,  `-:,.-')       ,-'   ,  `-:,.-')        
 : D(...):';  _  {    +  : N(...):';  _  {    +  ... and more
  `-.  `' _,.-\`-.)      `-.  `' _,.-\`-.)     
     `\\``\,.-'             `\\``\,.-'

```

### Writing the body

Every sender (`N()`, `O()`, `D()`) is a function taking *arguments* and *keyword arguments*. **Arguments are mandatory**, and keyword arguments optional. These arguments will define your event:

```python
D('bd', speep='[1:2,0.5]', legato=1, shape=0.5) # Heavy drumbass
N(note='C@min7^1', dur=2, channel=0)            # Short MIDI chord
```

You will have to learn what *arguments* each sender can receive. They all have a speciality. Despite the fact that they look and behave similarly, the event they describe is very different in nature depending on the type.

### Precising the tail

The tail of a sender consists of optional arguments specifying when and how to send events. We have already seen the tail in the *swimming functions* section. If you are here because of it, you've found the right place to look at! These arguments are:

- `iterator (i for short)` (*int*): the iterator for patterning. **Mandatory** for the two other arguments to work properly. This **iterator** is the index of the values extracted from your linear list-like patterns (your **arguments** and **keyword arguments**). How this index will be interpreted will depend on the next two arguments.

- `divisor (d for short)` (*int*): **a timing divisor**. It is very much alike a modulo operation. If `p=4`, the event will be emitted once every 4 iterations. The default is `p=1`, where every event is a hit! Be careful not to set a `p=1` on a very fast *swimming function* as it could result in catastrophic failure / horrible noises. There is no parachute out in the open sea.

- `rate (r for short)` (*float*): a speed factor for iterating over pattern values. It will slow down or speed up the iteration speed, the speed at which the pattern values are indexed on. For the pattern `1, 2, 3` and a rate of `0.5`, the result will be perceptually similar to `1, 1, 2, 2, 3, 3`.

I know, it doesn't make any sense written like so.. That's something you have to see represented differently. Take a look at `tail` arguments values. Notice how different values will produce different iteration speeds:

![outmethod](images/sardine_out_method.png){align=center}

Now, try exploring this idea using this dummy pattern:
```python
@swim
def ocean_periodicity(p=0.5, i=0):
    D('bd, hhh, sn, hhh', speep='1,2', freq='r*800', i=i, d=2, r=0.5)
    a(ocean_periodicity, p=0.5, i=i+1)
```
Don't touch to the pattern itself, just change values in the tail arguments. Try to be more familiar with it. You can change the recursion speed to notice more clearly how the pattern will evolve with time.

### Tips for writing Senders

Python is *extremely* flexible and expressive. The language makes it a breeze to compose arguments and keyword arguments in very fun and creative ways. I don't even have to code anything to support this and I'm very grateful that the language takes care of everything for me! Let's take an example. You can for instance store parameters common to multiple messages in a list/dictionary before sticking them to your patterns using the `*` and `**` idiom:

```python
params = {'loud': {'amp': 2, 'shape': 0.9}, 'soft': {'amp': 0.1, 'legato': 0.1}}
D('bd', **params['loud'])
```

This example looks very verbose, but try to imagine cases where *it will save you from an even more verbose situation*. It can happen very quickly when you try to play with many events at the same time, or when you will start imagining grouping sounds together or modifying multiple parameters in different events at the same time.


## II - The Dirt Sender

The **Dirt** or **SuperDirt** sender is a sender specialised in talking with **SuperCollider** and more specifically with the sound engine used by [TidalCycles](https://tidalcycles.org). I'm using the synthesis / sampling backend written and supported by [Julian Rohrhuber](https://www.rsh-duesseldorf.de/en/institutes/institute-for-music-and-media/faculty/rohrhuber-julian/) that many live-coders worldwide are also using. It is very stable, very flexible and highly-configurable.

This sender is the most complex you will have to interact with and it is entirely optional if you wish to use **Sardine** only to sequence MIDI and OSC messages. If we dive into its architecture, we will soon find out that this sender is a specialised OSC sender that talks exclusively with **SuperDirt** using special timestamped messages.

The body of the sender is always:

```python
D('sound', keyworp=value_or_pattern, keyword2=value_or_pattern)
```

The first argument defining the sound or synthesizer you are willing to trigger is not optional. Without it, you can be sure that the sender will crash because it cannot apply parameters to something that is not defined. The keyword parameters are the names of your **SuperDirt** parameters. It can be standard parameters, orbit parameters (audio bus) or parameters related to the synthesizer you are using. You will find more about this in the Reference section that is listing pretty much all of them!

You will feel a bit lost at first but this is a case where you learn a lot by doing and from experience. Take a look at the following examples.

### Simple Bassdrum

```python3
@swim
def bd(p=0.5):
    D('bd')
    again(bd, p=0.5)
```
A simple bassdrum playing on every half-beat. This is the most basic sound-making function you can write.

### Complex Bassdrum

```python3
@swim
def bd(p=0.5):
    D('bd', speep='r*4', legato='r', cutoff='100+0~4000')
    again(bd, p=0.25)
```
A simple bassdrum but some parameters have been tweaked to add some randomness to the result. See how patterns can be used to make your keyword arguments more dynamic. The additional parameters are :

- `speed` will reverse (<0), slow (0-1), or accelerate the sample (>1) by altering the playback speed. The `r` token provides randomization between `0.0` and `1.0` (*float*).
- `legato` defines the maximum duration of the sample before cutting it, here randomized in the `0` to `1` range.
- `cutoff` will attenuate some frequencies. This is the cutoff frequency of a lowpass filter that shuts down frequencies higher to the frequency cutoff. The cutoff frequency is guaranteed to be at least `100` plus a certain amount between `0` and `4000`.

### Simple Breakbeat

```python3
@swim
def bd(p=0.5, i=0):
    D('amencutup:0~20', i=i)
    again(bd, p=0.25, i=i+1)
```
Picking a random sample in a folder containing slices of the classic [amen break](https://en.wikipedia.org/wiki/Amen_break). You could have a successful career doing this in front of audiences. Once again, the *magic* happens with the `sample:r*X` notation, which randomizes which sample is read on each execution, making it unpredictable.

### Sample sequencing

```python3
@swim
def bd(p=0.5, i=0):
    D('bd,hh,sn,hh', i=i)
    again(bd, p=0.5, i=i+1)
```
Your classic four-on-the-floor written on one line. One sound is played after the other. All arguments and keyword arguments can be patterned.

### Piling up / Polyphony

```python3
@swim
def pluck(p=0.5, i=0):
    D('pluck', i=i)
    D('pluck:1', i=i)
    D('pluck:2', i=i)
    D('pluck:3', i=i)
    again(pluck, p=0.5, i=i+1)
```

You can stack events easily by just calling `D()` multiple times. In the above example, it happens that `pluck` samples are nicely order and are generating a chord if you struck them in parallel. How cool! But wait, there is more to it:

```python3
@swim
def pluck(p=0.5, i=0):
    D('<pluck:[0:4]>', octave=6, i=i)
    again(pluck, p=0.5, i=i+1)
```

You can also stack sounds by using polyphony. With **Sardine**, polyphony is not a concept reserved to notes. Every pattern can be polyphonic (sample names, speeds, adresses, etc...).

### More examples...

Check out the `Demos` section to find out how people are using the **D** sender.

## II - MIDI Notes Sender

The **MIDI Notes** or **N** sender is a sender specialised for emitting **MIDI** *note-on* and *note-off* messages just like on a music tracker or DAW. It does not have a lot of arguments, and if you have some degree of familiarity with the **MIDI** protocol, you will feel at home pretty quickly:

- **note**: your note number, between `0` and `127`. You can of course use patterns, and patterns can be patterns of notes (special syntax for writing chords, scales, notes, etc...). Values are clamped. If you enter an incredibly big number, it will be clamped to `127`. The same thing goes for small or negative numbers that will be brought back to `0`.

- **channel**: your **MIDI** channel from `0` to `15` (`1` to `16` in human parlance).

- **velocity**: amplitude of your note, between `0` and `127`.

- **dur**: duration of your note. Time between the *note-on* and *note-off* messages. This time, unlike almost everything else, is calculated in **clock ticks**. `dur=40` means that the *note-off* will only come after 40 clock ticks, which can be a long time or a very short time depending on your current timing context. You will notice that the **Link** clock is ticking really fast compared to the **MIDI** one.

That's it! You might wonder: where are my other MIDI messages? We got them covered too and you can pattern them of course. For now, the syntax is a bit old school and each MIDI message will have its own function but it won't last long :)

- `cc(channel: int, control: int, value: int)`: control change message.
- `pgch(channel: int, program: int)`: program change message.
- `pwheel(channel: int, pitch: int)`: pitch wheel message.
- `sysex(data: list)`: custom SYSEX message.

!!! info

    Note that since version 0.2 **Sardine** has senders for *control changes* and *program changes*, respectively named `CC` and `PC`!


### Sending a note

```python3
@swim
def midi(p=0.5, i=0):
    N()
    again(midi, p=0.5, i=i+1)
```
No argument required to send a **MIDI** Note (`60`) at full velocity (`127`) on the first default **MIDI** channel. Arguments are only used to specify further or to override default values.

### Playing a tune

```python3
@swim
def midi(p=0.5, i=0):
    N(note='C5,D5,E5,G5,E5,D5,G5,C5', i=i)
    again(midi, p=0.5, i=i+1)
```
Playing a little melody by tweaking the `note` argument.

### A bit better

```python3
@swim
def midi(p=0.5, i=0):
    N(channel='0,1,2,3',
      velocity='20 + (r*80)',
      dur=0.4,
      note='C5,D5,E5,G5,E5,D5,G5,C5',
      i=i)
    again(midi, p=0.5, i=i+1)
```
The same melody spreaded out on three **MIDI** channels (one per note) with random velocity.

### Other messages

```python3
@swim
def midi(p=0.5, i=0):
    N(channel='0,1,2,3',
      velocity='20 + (r*80)',
      dur=0.4,
      note='C5,D5,E5,G5,E5,D5,G5,C5',
      i=i)
    pgch(P('1,2,3,4', i)) # switching
    cc(channel=0, control=20, value=50) # control
    again(midi, p=0.5, i=i+1)
```
Switching between program `1`, `2`, `3` and `4` on your MIDI Synth. Sending a control change on channel `0`, number `20` for a value of `50`.

### More examples...

Check out the `Demos` section to find out how people are using the **N** sender.

## III - OSC Sender

The **OSC** Sender is the most complex and generic of all. It is a **sender** specialised for the *Open Sound Control* protocol. This is not because there are a lot of arguments and keyword arguments to learn but because using it relies on linking the **sender** to some other objects that will handle incoming or outgoing messages. It has the same body-tail architecture as the others but the arguments are a bit different:

```python
O(osc_connexion, address, keyworp=value_or_pattern, ...)
```

We always need to feed an OSC output port and an address. It perfeclty makes perfect sense if you are already familiar with OSC. You can pattern everything except the osc connexion. If you are clever enough, this won't stop you for long though. You will notice that you can do this if you really need to:

```python
gigantic_gundam = {
    '0': left_arm_connexion,
    '1': right_arm_connexion,
    '2': left_leg_connexion,
    '3': right_leg_connexion,
    '4': head_connexion,
}
O(osc_connexion[P('0~4', i)], 'x_pos', value=50)
```


### Sending OSC

```python3
my_osc = OSC(ip="127.0.0.1", port=23000, name="Bibu", ahead_amount=0.25)
```

This is the command you must use if you would like to create a new OSC client. The `ahead_amount` parameter is used to form the timetamp attached to your OSC message. If you are wondering, this is exactly the same value as the one you can tweak using `c._superdirt_nudge` when configuring your **S** sender.  It can be useful for synchronisation purposes.

Once this is done, you can use `O()` for sending OSC messages to that address:
```python
# Simple address
O(my_osc, 'loulou', value='1,2,3,4')

# Composed address (_ equals /)
O(my_osc, 'loulou/yves', value='1,2,3,4')

```
Note how `O()` takes an additional argument compared to other senders. You must provide a valid OSC client for it to work because you can have multiple senders sending at different addresses. Everything else is patternable like usual.

### Receiving OSC

You can also receive and track incoming OSC values. In fact, you can even attach callbacks to incoming OSC messages and turn **Sardine** into a soundbox so let's do it!

```python
info = Receiver(25000)
def funny_sound():
    D('bip', shape=0.9, room=0.9)
info.attach('/bip/', funny_sound)
```

Yeah, that's everything you need! In the above example, we are declaring a new `Receiver` object that maps to a given port on the given IP address (with `localhost` being the default). All we have to do next is to map a function to every message being received at that address and poof. We now have a working soundbox. Let's break this down and take a look at all the features you can do when receiving OSC.

Let's take a look at the `Receiver`:
```python
info = Receiver(port, ip, name)
```
You will find your usual suspects: `port`, `ip` and `name` (that is not used for anything useful really). There are three methods you can call on your `Receiver` object:

- `.attach(address: str, function: Callable, watch: bool)` : attach a callback to a given address. It must be a function. Additionally, you can set `watch` to `True` (`False` by default) to also run the `.watch` method automatically afterhands.

- `.watch(address: str)` : give an address. The object will track the last received value on that address. If nothing has been received yet, it will return `None` instead of crashing \o/.

- `.get(address)` : retrieve the last received value to that address. You must have used `.watch()` before to register this address to be watched. Otherwise, you will get nothing.

### Blending OSC

If you are receiving something, you can now use it in your patterns to map a captor, a sensor or a controller to a **Sardine** pattern. If you combo this with [amphibian-variables](#amphibian-variables), you can now contaminate your patterns with values coming from your incoming data:

```python
info = Receiver(25000)
info.watch('/sitar/speed/')

@swim
def contamination(p=0.5, i=0):
    v.a = info.get('/sitar/speed/')['args'][0]
    D('sitar', speed='V.a')
    a(contamination, p=0.5, i=i+1)
```

This opens up the way for environmental reactive patterns that can be modified on-the-fly and that will blend code and human interaction. Handling data received from **OSC** can be a bit tricky at first:

- if you wish to carefully take care of the data you receive, please use the `.attach()` method to attach a callback to every message received and properly handle the data yourself. Use the form `callback(*args, **kwargs)` and examine what data you receive in the *args* and *kwargs*. Map this to global variables, etc...

- if you don't care and just want to watch values as they go, please use the `.watch()` value but you will have to resort to using dictionnary  key access just like I do in the example above. You will have to handle cases where no data is received or cases where the received value is not of the right type. There is no memory of old messages, only the most recent one is kept in memory!

This is not ideal for some of you who do a lot of things with **OSC**. Please provide suggestions, open issues, etc... We will sort this out together!
