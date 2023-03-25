# Patterns

Creating, extending, and modifying patterns is the most essential part of using Sardine. Here we illustrate different patterns and simple ways to modify and extend them. Explanations, references, and usage details will come in later sections of the docs ([Basics](../basics.md), [Pattern Languages](../pattern_languages.md), [Diving Deeper](../diving_deeper.md)). If you want to try different sounds, go back to the samples page and substitute different sample names and index numbers: (`drum:2`, `hh27:4`, `stomp:0`, `noise:7`, etc.)

These examples all use a **Player** (`Pa`) which is the simplest way to start making sound with Sardine. 

## Simple patterns

Here is a very simple musical pattern alternating between two audio samples (1 per beat):

```python
Pa * d('bd cp')
```

You can change the period of a pattern by using the keyword `p`. Change the first string to play different samples, to repeat them, etc... This is how you start creating basic patterns. Pattern elements are delimited by a whitespace.

```python
Pa * d('bd cp', p=0.5)
Pa * d('bd cp hh:2', p=0.5)
Pa * d('bd cp hh:2', p=0.25)
Pa * d('bd!2 cp hh:2 .', p=0.25)
silence(Pa)
```

## Adding parameters

Let's try new sounds. Let's also switch our `p` argument to a pattern. Pretty much everything can be a pattern. Each sender (functions similar to `d`) can accept many arguments. Here, we are using `speed` or `shape` to change the audio playback parameters for our samples. There are many parameters you can tweak. See the [reference](../audio_engine.md) section for an overview.

```python
Pa * d('reverbkick east:4 yeah:2 mt', speed='1 2', shape=0.5, p='0.5')
Pa * d('reverbkick east:4 yeah:2 mt cr', speed='1 2',
        shape=0.5, p='0.5!4  0.25')
silence(Pa)
```
## Multiple players

Let's use multiple players! Select all the players and evaluate. You are now playing four different patterns at the same time. They will all start on the first beat of the bar and be synchronised with each other.

```python
Pa * d('bd cp', p=0.5)
Pb * d('bd cp hh27:2', p=0.5)
Pc * d('bd cp hh27:2', p=0.25)
Pd * d('bd!2 cp hh27:2 .', p=0.25)
silence()
```

## Tempo

The tempo is set using a *beats per minute* value in your Sardine [configuration](../configuration.md). You can also change it on the fly.
Learn more about time and tempo in the [appropriate section](../basics/tempo_and_playback.md):

```python
clock.tempo # prints the current clock tempo value
clock.tempo = 135 # sets a new clock tempo in BPM
```


