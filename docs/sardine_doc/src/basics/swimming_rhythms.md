# Swimming rhythm

This section will teach you the last basic concepts you need to understand to truly master **Sardine**! By reading what comes before, you should now know:

- how to evaluate and update your code anytime you want.
- how to play sounds and send notes to your synthesizers and instruments.
- how to play with the shorthand syntax and with **swimming functions**.
- how to describe looping processes and how to count in time.

This is where **Sardine** starts to get more creative because we will do something with these new found powers. **Sardine** is basing a lot on two concepts:

- **temporal recursion** aka **swimming functions**
- **iterations**: counting up and down.

### Iterator

Remember about patterns? Patterns were these things that we were writing in `strings` like so:

```python
"C E G B"
"bd!2 cp:rand*20 tabla"
"1 2 3 4"
```

I told you before that you could **use strings in your senders** and that this **would transform them into sequences**. Let&rsquo;s explore that:

```python
@swim
def sequence(p=0.5, i=0):
    D("bd!2 cp:rand*20 tabla")
    again(sequence, p=0.5, i=i+1)
```

All you are hearing is a kick, right? We are looping, but how do we tell **Sardine** to move ahead in time? For that, we will be using that counter we saw earlier. This counter can be fed to a pattern to tell him where we are in time:

```python
@swim
def sequence(p=0.5, i=0):
    D("bd!2 cp:rand*20 tabla", i=i)
    again(sequence, p=0.5, i=i+1)
```

`i` stands for `iterator` and **every sender can receive an iterator**. Your pattern is now alternating between `bd`, `cp` and `tabla`. That is because it plays the first sound in the sequence, then the second one, then the third one, and all over again. Your iterator can be infinitely big, the sequence will just loop around!

Take a look at this musical sequence using patterns of different lengths with a single iterator:

```python
@swim
def sequence(p=0.5, i=0):
    D("bd!2 cp:rand*20 tabla",
        speed='1 2 3 4 5 6',
        lpf="200+rand*2000",
        i=i
    )
    again(sequence, p=0.5, i=i+1)
```

This opens up a new world of complexity because **every parameter can be patterned**, including the ones that you wouldn&rsquo;t have thought about: MIDI channels, instruments, etc&#x2026; You can start patterning every musical information at your fingertips!


### Jumping in time(s)

Time flows. We all know that. With **Sardine**, you can also play with the idea of making time flow backwards, or randomly. Time is only symbolised by a single number, your iterator. It means that by controllign this iterator wisely, you can control the direction to give to your musical sequence:

```python
@swim
def sequence(p=0.5, i=0):
    ...
    again(sequence, p=0.5, i=i-1) # Code changed here
```

It now flow backwards, but let&rsquo;s also make it flow&#x2026; randomly. To do that, we can use the `random.randint()` function from **Python**:

```python
from random import randint
    
@swim
def sequence(p=0.5, i=0):
    ...
    again(sequence, p=0.5, i=randint(1,100)) # Code changed here
```

And it will now jump between 100 different positions. You can also start to play around with different ideas:

- having multiple iterators flowing at different speeds.
- freezing an iterator, resuming it based on a condition.

### Divisor and rate

And now it becomes truly bizarre. What if we had some other tools to control how fast we iterate over our musical sequence?

I told you about `i` (the `iterator`) but it also comes to the party with some friends: `r` (the rate) and `d` (the divisor):

- the `rate` will count how many times you need to increment your number for it to move upwards or backwards by 1. It will basically make it much harder or much easier to increase or decrease the index of your patterns.
- the `divisor` will just refuse to play some events if the iterator `modulo` the `divisor` is equal to zero. Doesn&rsquo;t make sense to you? Think rhythm generator. Try to experiment with this :)


