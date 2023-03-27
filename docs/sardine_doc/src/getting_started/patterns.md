# Patterns

Creating, extending, and modifying patterns is the most essential part of using Sardine. Here we illustrate different patterns and simple ways to modify and extend them. Explanations, references, and usage details will come in later sections of the docs ([Basics](../basics.md), [Pattern Languages](../pattern_languages.md), [Diving Deeper](../diving_deeper.md)). If you want to try different sounds, go back to the samples page and substitute different sample names and index numbers: (`drum:2`, `hh27:4`, `stomp:0`, `noise:7`, etc.)

These examples all use a **Player** (`Pa`) which is the simplest way to start making sound with Sardine. Here is a very simple musical pattern alternating between two audio samples (1 per beat):

```python
Pa * d('bd cp')
```

You can change the period of a pattern by using the keyword `p`. The period relates to beats, so when `p=0.5` there are two notes per beat, when `p=2` there are 2 beats per note. 
- Change the first string `bd cp` to play different samples, to repeat them, etc... 
- The character "." in a pattern is a rest (no sound). 
- `'bd!2 cp'` will play the bd sample twice.  
- Pattern elements are delimited by whitespace (no comma) and are enclosed in quotes. 

```python
Pa * d('bd cp', p=0.5) # sets period to 0.5, yields 2 notes per beat
Pa * d('bd cp hh:2', p=0.5) # adds the hh:2 sample, meter is now felt in 3
Pa * d('bd cp hh:2', p=0.25) # period is 0.25, 4 notes per beat, rhythm is twice as fast
Pa * d('bd!2 cp hh:2 .', p=0.25) # adds bd repeat and a rest "." - meter is felt in 5.

silence(Pa)
```
Notice how the basic pattern we started with has expanded, step by step. This is how you start creating patterns, this is livecoding. 

## Adding parameters

Let's try new sounds. Each sender (functions similar to `d`) can accept many arguments. Below, we are using `speed` and `shape` to change the audio playback parameters for our samples. There are many parameters you can tweak. See the [reference](../audio_engine.md) section for an overview.

- In the 2nd version of the Player, we switch the `p=0.5` argument from a single value to a pattern `p='0.5 0.25'`, and similarly for the speed parameter `speed='1.2 2'`. Note how this adds rhythmic variety shifts the pitch. 
- In the 3rd version, we add an additional sample `cr` and vary the rhythm with a less regular period pattern `p='0.5!2 0.25!5'`. The music now shifts around more. 

```python
Pa * d('reverbkick east:4 yeah:2 mt', speed=1.2, shape=0.5, p=0.5) 
Pa * d('reverbkick east:4 yeah:2 mt', speed='1.2 2', shape=0.5, p='0.5 0.25')
Pa * d('reverbkick east:4 yeah:2 mt cr', speed='1.2 2.2', shape=0.7, p='0.5!2 0.25!5')

silence(Pa)
```

## Multiple players

Let's use multiple players! Select all the players and evaluate. You are now playing four different patterns at the same time. They will all start on the first beat of the bar and be synchronised with each other.

```python

Pa * d('bd cp', p=1) # plays every beat, alternating bd and cp
Pb * d('hh27:2', p=0.5) # plays every 1/2 beat
Pc * d('. east:4!2 .', p=0.25) # plays 2nd and 3rd of the 1/4 beat
Pd * d('. . . bleep:0', p=0.25) # plays every 4th of the 1/4 beat

silence()
```

## Tempo

The tempo is set using a *beats per minute* value in your Sardine [configuration](../configuration.md). You can also change it on the fly.
Learn more about time and tempo in the [appropriate section](../basics/tempo_and_playback.md):

```python
clock.tempo # prints the current clock tempo value
#
clock.tempo = 100 # sets a new tempo - try different values
Pa * d('bd cp', p=1)
Pb * d('hh27:2', p=0.5)
Pc * d('. east:4!2 .', p=0.25)
Pd * d('. . . bleep:0', p=0.25)

silence()
```

### Summary 
This concludes the Getting Started section. The Basics section will go into more detail for the components covered here. Before moving on, spend time experimenting with what you have learned. 
- Explore the sample library, subsitute samples in the examples above.
- Use different period values to control the speed of rhythmic changes.
- Add and change parameters to alter pitch and timbre.
- Try different pattern values to get an understanding of what patterns are. 
- Have fun, you are livecoding now!



