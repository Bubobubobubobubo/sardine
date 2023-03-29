# Using Python
Sardine is written and executes in python. You can use python code both inside and outside of Players and @swim functions. This is one of most powerful features of Sardine - once you understand how to use it. There are also times where you need to execute python commands.

### Import modules
Importing modules is a standard way to access additional functionality in python. In Sardine, importing from the **random** module is needed whenever you want random values in your expressions. In the example there are two calls to random functions: `randint(<low, high>)` and `random()`. The second generate a random float between 0 and 1. Our example uses random in an expression. It expands the random range 1.5 times and moves it up by 0.4. This yields random values for the speed parameter between `0.4 and 1.9`. 

```python
from random import * 
clock.tempo=90

@swim
def demo(p=1, i=0):
    D('electro1:2 electro1:4 electro1:3 feelfx:2',
    freq=randint(100,400),
    #speed=(random()*1.5)+0.4,
    i=i)
    again(demo, p=0.5, i=i+1)
```

### aliases
Looking for a way to reduce keystrokes? Aliases are simple. This example uses a python assignment so that **a** is an alias for "again."

```python
a=again
@swim
def demo(p=1, i=0):
    D('electro1:2 electro1:4 electro1:3 feelfx:2', i=i)
    a(demo, p=0.5, i=i+1)
```
### calling functions
You can call python functions from within a @swim. 

```python
TBD
```
### Setting amphibian variables
Amphibian variables can have their values set outside of @swim with a python assignment/expression. You can also write a custom function that sets an amphibian variable.

```python
TBD
```

 ### Advanced example - Sample Segment
Below is an example with extended sections of python code, with custom functions, presets, import statements, and initializing values and lists. Sample Segment uses nested lists to contain sample names and durations from 3 SuperDirt sample banks. Custom functions randomize the selection of which sample to use and then randomize start and end points in the sample file. Using the start and end values, the length of the sample is determined. These then are assigned to Amphibian values for `sampleName:index`, `begin`, `end`, `period`. Amphibian variables are referenced in the @swim function. There is a simple command to "reset" the amphibian variables, based on which sampleList you choose. During a running @swim, reseting will change the sample slice and period, which because of the randomizing factor, can dramatically alter the resulting sound. 

See the Instructions section below to play with Sample Segment. 

 ```python
###### Sample Segment - illustrates custom python functions that generate Sardine amphibian variable values. 
### Instructions   #########################
# 1. load Presets, Initialize, and Functions
# 2. set the amphibian variables once before starting @swim. You will see the values print out. 
# 3. start the @swim function
# 4. reset amph variables and change @swim parameters at will
# 5. Try adding your own sampleList -> have fun! 

########## PRESETS #########################
rev0 = {'room':1.5, 'size':0.8, 'dry':0.8}
verb0 = {'verbwet':0.8, 'verbtime':0.7, 'verbgain':0.8}
del0 = {'delay':0.5, 'delaytime':0.4, 'delayfeedback':0.6}

########## Initialize ######################
from random import * 
clock.tempo=60 # assumed for period calculations

# Sample lists - fm:3 is the ~dirt.samples format. Floats values are the sample length in secs.
sampleListFm = [["fm:3", 4.197], ["fm:4", 1.92], ["fm:7", 1.97], ["fm:9", 4.42], ["fm:14", 1.73] ]
sampleListBirds = [["birds:0", 2.0], ["birds:1", 2.0], ["birds:2", 3.0], ["birds:3", 2.5], ["birds:4", 4.0], ["birds:5", 1.0], ["birds:8", 1.75], ["birds:9", 1.75] ]
sampleListDiphone = [["diphone:0", 0.9], ["diphone:1", 0.9], ["diphone:2", 0.9], ["diphone:3", 0.9], ["diphone:4", 0.9], ["diphone:5", 0.9], ["diphone:8", 0.9], ["diphone:9", 0.9], ["diphone:10", 0.9], ["diphone:11", 0.9] ]

########## FUNCTIONS #############################
def setSampleVals(sampleDurIn, directionIn):
# generates random start and end points and calculates the period duration (secs)
    minPeriod = 0.04 # period must be > 0
    endRand = random()
    beginRand = random() * endRand
    periodDur = (endRand - beginRand) * sampleDurIn # sets period length
    # if extend is longer than periodDur, set to minPeriod value, else add extend 
    if (periodDur <= 0): periodDur = minPeriod
    if (directionIn == -1):
        return(endRand, beginRand, periodDur) # switch end and begin for reverse play
    else:
        return(beginRand, endRand, periodDur)

def genSampSeg(sampListIn, directionIn):
# random selects the sample from the sample list, gets values and returns sample Name, begin,end,period duration 
    sampListIndex = randint(0, len(sampListIn)-1) # rand pick a sample from list
    sampName = sampListIn[sampListIndex][0]
    beginN, endN, periodDurT = setSampleVals(sampListIn[sampListIndex][1], directionIn)
    print(sampListIn[sampListIndex], round(beginN,3), round(endN,3), round(periodDurT,4))
    return(sampName, beginN, endN, periodDurT)

######### LIVE CODING Section  #############################
### set / reset Amphibian Variables - execute one of the Amph Variables lines
# V.s = sampleName:index V.b = begin V.e = end V.p = period
# execute one line to initialize all amphibian variables before starting the @swim 
# execute one line while @swim is playing to reset the amph vars - this will change the sound and rhythm, often radically
# change the direction argument: 1=forward, -1=reverse

# sets / resets Amphibian variables. Execute any one of these lines before and then when @swim is playing.
V.s, V.b, V.e, V.p = genSampSeg(sampleListFm, 1) # drum beats
V.s, V.b, V.e, V.p = genSampSeg(sampleListDiphone, 1) # speech 
V.s, V.b, V.e, V.p = genSampSeg(sampleListBirds, 1) # 

V.s, V.b, V.e, V.p = ['diphone:4', 0.662, 0.902, 0.21] # hard code the amph vars

# @swim function: start play, then execute one of the lines above to change parameters.
# Be prepared for wierd things to come out! 
# Uncomment / comment lines to change parameter values.
@swim
def sampleSegment(p=1, i=0):
    D('(v s)', 
    begin='(v b)', end='(v e)', **rev0, 
    #**del0, # delay preset
    speed='1 0.5 1.5',
    #freq=randint(150,400), 
    #freq='[150:270,10] [270:240,4] [240:270,4] [272:150,15]',
    pan='0 1', amp=0.9, d=1, rate=1, i=i)
    again(sampleSegment, p=P('(v p)'), i=i+1)

clock.tempo=60
silence(sampleSegment)
 ```
