# Patterns

Creating, extending, and modifying patterns is the most essential part of using Sardine. Here we illustrate different patterns and simple ways to modify and extend them. Explanations, references, and usage details will come in later sections of the docs (Basics, Pattern Languages, Diving Deeper). If you want to try different sounds, go back to the samples page and substitute different sample names and index numbers: (drum:2, hh27:4, stomp:0, noise2:7, etc.)

These examples all use a "Player" (Pa) which is the simplets way to start making sound with Sardine. 

## Simple patterns

```python
Pa >> d('bd cp')
```

change period ('p'), add samples, repeat samples in a pattern
```python
Pa >> d('bd cp', p=0.5)
Pa >> d('bd cp hh27:2', p=0.5)
Pa >> d('bd cp hh27:2', p=0.25)
Pa >> d('bd!2 cp hh27:2 .', p=0.25)
silence(Pa)
```

## Adding parameters
new sounds, period ('p) as a pattern, sample playback pattern (speed)
```python
Pa >> d('reverbkick east:4 yeah:2 mt', speed='1 2', shape=0.5, p='0.5')
Pa >> d('reverbkick east:4 yeah:2 mt cr', speed='1 2', shape=0.5, p='0.5!4  0.25') #note the meter is now in 5
silence(Pa)
```
## Multiple players

Play one line at a time or select all and evaluate together. 
```python
Pa >> d('bd cp', p=0.5)
Pb >> d('bd cp hh27:2', p=0.5)
Pc >> d('bd cp hh27:2', p=0.25)
Pd >> d('bd!2 cp hh27:2 .', p=0.25)
silence()
```

## Tempo

Tempo in BPM is set by default in your Sardine config. It can be changed at any time. See more details about the clock in Basics > Tempo and Playback

```python
clock.tempo # prints the current clock tempo value
clock.tempo = 135 # sets a new clock tempo in BPM
```

