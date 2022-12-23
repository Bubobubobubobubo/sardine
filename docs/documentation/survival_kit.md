# Survival Kit

You can copy-paste this file and/or get a copy of it in the repository itself. This file is a grand tour of everything you can do with a basic installation of Sardine. I'll also shoot a video pretty soon where I'll browse through the file commenting some selected examples.

## Tutorial file

```python
# This is a condensed Sardine tutorial. Copy and paste this file in a working buffer.
# You can evaluate pretty much every example and follow along. By the end of this file,
# you should have a better understanding of Sardine.
# Make sure that you have the same configuration as me.
# I have toggled pretty much everything in sardine-conf.
# BPM: 120.0,BEATS: 4 SC: [X], DEFER: [X] MIDI: Sardine

# You can now evaluate every code example I'm providing. 
# Let's start with a basic hello world!

@swim
def hello_world():
    print('Hello World!')
    again(hello_world)

silence() # Silence will stop everything.
panic() # Panic will kill everything (useful when you lost control).

# Let's break it down. This is just a normal Python function.

def hello_world():
    print('Hello World!')

# However, we are adding the swimming decorator. It allows the
# function to loop automatically and will allow you to reevaluate
# it whenever you want.

@swim
def hello_world():
    print('Hello World!')

# This is not enough, because we need to explicitely tell our 
# function to come back around :)

@swim
def hello_world():
    print('Hello World!')
    again(hello_world)

# We call this pattern a 'temporally recursive function' or a 
# 'swimming function' because fishes are funnier.
# Now we are going to replace printing by sounds.

@swim
def hello_world():
    D('bd')
    again(hello_world)

# We now have a kick. Let's change the recursion speed.

@swim
def hello_world(p=0.5):
    D('bd')
    again(hello_world, p=0.5)

# This is twice as fast. Let's add more complex rhythms.

@swim
def hello_world(p=0.5, i=0):
    rhythm = Pat('0.5, 0.25, 1', i)
    D('bd')
    again(hello_world, p=rhythm, i=i+1)

# There is quite a lot of complexity already! Let's break it
# down by falling back to something simpler.

@swim
def hello_world(p=0.5, i=0):
    D('bd, drum:8, cp, drum:8', i=i)
    again(hello_world, p=0.5, i=i+1)

# This is a four on the floor. Note that we are using iterators
# quite a lot. They are super important in Sardine. In the last
# example, we are moving forward in the pattern by incrementing
# the i variable everytime we loop around.


@swim
def hello_world(p=0.5, i=0):
    D('bd, drum:8, cp, drum:8', i=i)
    D('jvbass:[0:10]', i=i)
    again(hello_world, p=0.5, i=i+1)

# Super cool! Let's try to add a random number to the i=i argument.

from random import randint

@swim
def hello_world(p=0.5, i=0):
    D('bd, drum:8, cp, drum:8', i=randint(1,10))
    D('jvbass:[0:10]', i=randint(1,1000))
    again(hello_world, p=0.5, i=i+1)

# We are now randomly peeking in the pattern. Let's now play the 
# pattern in reverse.

@swim
def hello_world(p=0.5, i=0):
    D('bd, drum:8, cp, drum:8', i=-i)
    D('jvbass:[0:10]', i=-i)
    again(hello_world, p=0.5, i=i+1)

# Negative iteration, we are going in the other direction!
# What if we play directly with i=i+1?

@swim
def hello_world(p=0.5, i=0):
    D('bd, drum:8, cp, drum:8', i=i)
    D('jvbass:[0:10]', i=i)
    again(hello_world, p=0.5, i=i+2)

# Now we are skipping some pattern elements! This is yet another easy
# variation on our last pattern. 

@swim
def hello_world(p=0.5, i=0):
    rhythm = Pat('1/3, 2/3', i)
    D('bd, drum:8, cp, drum:8', i=i)
    D('jvbass:[0:10]', i=i)
    again(hello_world, p=rhythm, i=i+2)

# I am using the Pat(pattern, iterator) object to add some rhythm to
# my recursions. Yet another layer of complexity, but you know what?

silence()

Pa >> d('bd, drum:8, cp, drum:8', p='1/3,2/3')
Pb >> d('jvbass:[0:10]', p='1/3,2/3')

# You can also write things like this. We call these 'surfboards'
# because they feel great for surfing around in the system.

Pa >> None
Pb >> None

# To stop these, you can just assign None to them using the >> special
# operator. You can also make them faster or slower by using span=

Pa >> d('bd, drum:8, cp, drum:8', p='1/3,2/3', span=0.5)
Pb >> d('jvbass:[0:10]', p='1/3,2/3', span=0.5)


Pa >> d('bd, drum:8, cp, drum:8', p='1/3,2/3', span=2)
Pb >> d('jvbass:[0:10]', p='1/3,2/3', span=2)

# It can get weird very easily, especially when you start playing with
# the period argument (p). I'll let you try and see for yourself!

Pa, Pb, Pc, Pd, Pe, Pf, Pg, Ph, ...
PA, PB, PC, PD, PE, PF, PG, PH, ...

# There is 48 'Players' to get you running with surfboards. Note that
# we were previously using D, but we use d for surfboards.

silence()
# -------------------------------------------------------------------
# Let's pause for a moment and speak about patterns!
# Let's fallback to our kick pattern

@swim
def pattern101(p=0.5, i=0):
    D('bd')
    again(pattern101, p=0.5, i=i+1)

# Everytime you specify an argument using a string, this is a pattern.

@swim
def pattern101(p=0.5, i=0):
    D('bd', speed='1,2,3,4', i=i)
    again(pattern101, p=0.5, i=i+1)

# You can have multiple patterns in one D() call. A call is like a big
# pattern sandwich.

@swim
def pattern101(p=0.5, i=0):
    D('bd', speed='1,2,3,4', shape='0.1,0.3', room='0.0, 0.2', i=i)
    again(pattern101, p=0.5, i=i+1)

# Keyword arguments are used to change parameters of the sound or 
# event you want to play with!

@swim
def pattern101(p=0.5, i=0):
    D('bd', 
      midinote='C,E,G',
      speed='[1:4]', 
      shape='0.1,0.3', 
      room='0.0, 0.2', i=i)
    again(pattern101, p=0.5, i=i+1)

# Any keyword parameter is accepted by only some will have an effect.
# For a complete list of parameters used by D(), check the reference
# page!

@swim
def pattern101(p=0.5, i=0):
    D('bd', 
      midinote='C,E,G',
      speed='[1:4]', 
      shape='0.1~0.3', 
      room='sin($)', i=i)
    again(pattern101, p=0.5, i=i+1)

# The patterns are written using a small programming language that has
# been specificaly designed for Sardine! There are many things you can
# do with patterns.

@swim
def pattern101(p=0.25, i=0):
    D('jvbass', midinote='adisco(C,Eb,G), C, Eb, F', i=i)
    again(pattern101, p=0.25, i=i+1)

# Here, we are applying the anti-disco function to part of our note.
# pattern. Oh, and we can write notes as well. If you wish, you can
# also use french names for notes.

@swim
def pattern101(p=0.25, i=0):
    D('jvbass', midinote='adisco(Do,Mib,Sol), Do, Mib, Fa', i=i)
    again(pattern101, p=0.25, i=i+1)

# Check out the 'Language' section on the website to learn more about
# the pattern language. I'll just browse through some selected
# features now!


@swim
def pattern101(p=0.25, i=0):
    D('jvbass:[0:10]', i=i)
    again(pattern101, p=0.25, i=i+1)

# [x:y] can be used to create a consecutive list of integers or 
# floating point numbers. The pattern above is actually:
# jvbass:0 jvbass:1 jvbass:2 jvbass:3 jvbass:4, etc...
# Here is what it sounds like with notes!

@swim
def pattern101(p=0.25, i=0):
    D('jvbass', midinote='60+[0:24]', i=i)
    again(pattern101, p=0.25, i=i+1)

# You can actually print these patterns if you are more comfortable
# reading through this!

@swim
def pattern101(p=0.25, i=0):
    print(Pat('[0:10]', i)) # lovely silence
    again(pattern101, p=0.25, i=i+1)

# It would be too long to explain all the things you can do with that pattern language. 
# Be ready, here is a big pattern sandwich you can explore!
# Comment out various parts to check the output of each pattern

@swim
def pattern101(p=0.25, i=0):
    print(Pat('[0:10]', i)) # lists
    print(Pat('[0:10,0.5]', i)) # custom step
    print(Pat('r', i)) # random number between 0.0 and 1.0
    print(Pat('r*20', i)) # but you can do math with it
    print(Pat('sin(r)', i)) # there are functions as well
    print(Pat('1~10', i)) # random integer in range
    print(Pat('1.0~10.0', i)) # random float in range
    print(Pat('1, 1+1, 1*2, 1/3, 1%4, 1+(2+(5/2))', i))
    # Look at me, I can do basic arithmetic!
    again(pattern101, p=0.25, i=i+1)

silence()

# These are very basic tokens you can use but they can bring you 
# really far when you start to apply them to MIDI or audio samples.
# Let's focus a bite more about note-specific tokens!

@swim
def pattern101(p=0.25, i=0):
    print(Pat('C,E,G', i)) # C Major arpeggio
    print(Pat('rev(C,E,G)', i)) # reversing the pattern
    print(Pat('Do, Mi, Sol', i)) # French note names
    print(Pat('Db, Fa, Lab', i)) # Flat note
    print(Pat('Mi,Sol#,Si', i)) # Sharp note
    print(Pat('Mib5', i)) # You can specify octave numbers
    print(Pat('[Do, Mib, Sol]+[1,2,3]', i)) # list arithmetic
    print(Pat('C@minor', i)) # C minor scale!
    print(Pat('C@fifths', i)) # Consecutive fifths!
    # Look at me, I can do basic arithmetic!
    again(pattern101, p=0.25, i=i+1)

silence()

# Note that note names are in reality... numbers. They are automa-
# tically converted to numbers whenever they are parsed by the 
# internal language. You can also use numbers if you prefer!

# Sample names are rather weird as well. There is a lot you can do!

@swim
def pattern101(p=0.25, i=0):
    print(Pat('baba:1', i)) # First sample in 'baba' folder
    print(Pat('baba:1~5', i)) # Random picking in 'baba' folder
    print(Pat('baba:[0:10]', i)) # List of samples from 0 to 10
    print(Pat('baba:r*8', i)) # Yet another random picking method
    again(pattern101, p=0.25, i=i+1)
```

