# Advanced Python - Sample Slicer 

**NOTE:** this article was using _amphibian variables_, a deprecated feature. Rely on the `set` and `get` functions for a similar behavior.

**Using custom python functions to multiple amphibian variables**

This example uses custom functions to generate 4 amphibian variables at once. It also uses presets, initialized values, and sample lists. The Sample Slicer is a complete livecoding program, ready to use. You can also extend it, add more samples to slice, add more amphibian variables, add more parameters, etc. 

## Description

- Custom functions randomize the selection of which sample file to use and then randomize start and end points in the sample file (sample slicing).
- Output of the functions is assigned to Amphibian values for `sampleName:index`, `begin`, `end`, `period`. 
- Amphibian variables are referenced in the @swim function. 
- There is a simple command to "reset" the amphibian variables, based on which sampleList you choose. 
- During a running @swim, reseting will change the sample slice and @swim period -- which can dramatically alter the sound. 

 ```python
""" 
Sample Slicer: llustrates the use of custom python functions that generate Sardine amphibian variable values. 

Instructions
1. Load Presets, Initialize, and Functions.
2. Set the amphibian variables once before starting @swim. You will see the values print out. 
3. Start the @swim function.
4. Reset amph variables and change @swim parameters at will.
5. Try adding your own sampleList -> have fun! 
"""
########## PRESETS #########################
rev0 = {'room':1.5, 'size':0.8, 'dry':0.8}
verb0 = {'verbwet':0.8, 'verbtime':0.7, 'verbgain':0.8}
del0 = {'delay':0.5, 'delaytime':0.4, 'delayfeedback':0.6}

########## Initialize ######################
from random import * 
clock.tempo=60 # assumed for period calculations

# Sample lists - fm:3 is the ~dirt.samples format. Floats values are the sample length in secs.
# Any list of samples loaded in SuperDirt will work.
sampleListFm = [["fm:3", 4.197], ["fm:4", 1.92], ["fm:7", 1.97], ["fm:9", 4.42], ["fm:14", 1.73] ]
sampleListBirds = [["birds:0", 2.0], ["birds:1", 2.0], ["birds:2", 3.0], ["birds:3", 2.5], ["birds:4", 4.0], ["birds:5", 1.0], ["birds:8", 1.75], ["birds:9", 1.75] ]
sampleListDiphone = [["diphone:0", 0.9], ["diphone:1", 0.9], ["diphone:2", 0.9], ["diphone:3", 0.9], ["diphone:4", 0.9], ["diphone:5", 0.9], ["diphone:8", 0.9], ["diphone:9", 0.9], ["diphone:10", 0.9], ["diphone:11", 0.9] ]

########## FUNCTIONS #############################
def setSampleVals(sampleDurIn, directionIn):
# generates random start and end points and calculates the period duration
    endRand = random()
    beginRand = random() * endRand
    periodDur = (endRand - beginRand) * sampleDurIn # sets period length
    if (directionIn == -1):
        return(endRand, beginRand, periodDur) # switch end and begin for reverse play
    else:
        return(beginRand, endRand, periodDur)

def genSampSlice(sampListIn, directionIn):
# random selects the sample from the sample list
    sampListIndex = randint(0, len(sampListIn)-1) # rand pick a sample from list
    sampName = sampListIn[sampListIndex][0]
    beginN, endN, periodDurT = setSampleVals(sampListIn[sampListIndex][1], directionIn)
    print(sampListIn[sampListIndex], round(beginN,3), round(endN,3), round(periodDurT,4))
    return(sampName, beginN, endN, periodDurT)

######### LIVE CODING Section  #############################
### set / reset Amphibian Variables - execute one of the Amph Variables assignment statements
# Amph Variables: V.s = sampleName:index, V.b = begin, V.e = end, V.p = period
# execute one line to initialize all amphibian variables before starting the @swim 
# execute one line while @swim is playing to reset the amph vars - this will change the sound and rhythm, often radically
# change the direction argument: 1=forward, -1=reverse

# Execute any one of these statements before and then when @swim is playing.
V.s, V.b, V.e, V.p = genSampSlice(sampleListFm, 1) # drum beats
V.s, V.b, V.e, V.p = genSampSlice(sampleListDiphone, 1) # speech 
V.s, V.b, V.e, V.p = genSampSlice(sampleListBirds, 1) # birds

V.s, V.b, V.e, V.p = ['diphone:4', 0.662, 0.902, 0.21] # hard code the amph vars

# @swim function: start play, then execute one of the lines above to change parameters.
# Uncomment / comment lines to change parameter values. Adjust clock.tempo.

@swim
def sampleSlicer(p=1, i=0):
    D('(v s)', 
    begin='(v b)', end='(v e)', **rev0, 
    #**del0, # delay preset
    speed='1 0.5 1.5',
    #freq=randint(150,400), 
    #freq='[150:270,10] [270:240,4] [240:270,4] [272:150,15]',
    pan='0 1', amp=0.9, d=1, rate=1, i=i)
    again(sampleSlicer, p=P('(v p)'), i=i+1)

clock.tempo=60
silence(sampleSlicer)
 ```
