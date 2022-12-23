# Solstice

## Description

This is a 20 minutes performance that I did for the TidalCycles annual solstice stream. Three of the four tracks were rapidly composed before the stream. I've tried to highlight some of the new features we have worked on for the `v.0.2.1`. I am sometimes playing additional keyboard on top of the live code.

## Performance

<iframe width="1351" height="495" src="https://www.youtube.com/embed/bM5FXw-5N8s" title="Solstice Night Stream December 2022 - Bubo - 2022-12-21 17:00" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Source code

```python
padcc = { 'timbre': {'control' : 18, 'chan': 2},
        'time': {'control' : 19, 'chan': 2},
        'metal': {'control' : 16, 'chan': 2},
        'fx': {'control' : 17, 'chan': 2}}
basscc = { 'timbre': {'control' : 18, 'chan': 0},
        'time': {'control' : 19, 'chan': 0},
        'cutoff': {'control' : 16, 'chan': 0},
        'fx': {'control' : 17, 'chan': 0}}
jupcc = { 'decay': {'control' : 81, 'chan': 1},
        'time': {'control' : 19, 'chan': 1},
        'cutoff': {'control' : 74, 'chan': 1},
        'resonance': {'control' : 71, 'chan': 1}}
dirt._ahead_amount = 0.4

#######################################################################
#█▀▀ █▀█ █▀▀ █▄░█ █▀▀ █░█   ▀█▀ █▀█ █░█ █▀▀ █░█   █▀ ▄▀█ █▀▄▀█ █▄▄ ▄▀█#
#█▀░ █▀▄ ██▄ █░▀█ █▄▄ █▀█   ░█░ █▄█ █▄█ █▄▄ █▀█   ▄█ █▀█ █░▀░█ █▄█ █▀█#
#######################################################################

PE >> d('long:3', cut=1, begin="[0.0:0.6,0.1]")

Pc >> d('ff:4!3, gg:12', cut=1, p=0.25, orbit=1, shape=0.5)

Pb >> d('f!7', cut=0, p=1, orbit=2, shape=0.5)

Pd >> d('g:10', p='.5, .5, .25', orbit=2, shape=0.5, speed='2,2,1!2,4')

Pb >> None
Pc >> None
Pc >> d('bip:r*20', speed=2, 
        cut=0, p=0.25, orbit=1, shape=0.5, hcutoff='[500:15000,1000]')

# --- 

PE >> d('long:3', cut=1, begin="[0.0:0.6,0.1]")
Pc >> d('ff:4!3, gg:12', cut=1, p=0.25, orbit=1, shape=0.5)
Pb >> d('f!7', cut=0, p=1, orbit=2, shape=0.5)
Pd >> d('g:10', p='.5, .5, .25', orbit=2, shape=0.5, speed='2,2,1!2,4')
Pf >> d('bip:r*50', speed=2, midinote='C5,C5,G5,A5',
        cut=1, p=0.25, orbit=1, shape=0.5)
Pg >> d('bip:r*50', squiz=4, speed=1, midinote='C3,C4,G3,G4,A4,A5', shape=0.5,
        cut=1, p=0.25, orbit=1)

# --- 

Pa >> None
Pb >> None
Pc >> None
Pd >> None

PE >> d('long:3', cut=1, begin="[0.0:0.6,0.1]")
Pc >> d('ff:4!3, gg:12', cut=1, p=0.25, orbit=1, shape=0.5)
Pb >> d('f!7', cut=0, p=1, orbit=2, shape=0.5)
Pd >> d('g:10', p='.5, .5, .25', orbit=2, shape=0.5, speed='2,2,1!2,4')
Pf >> d('bip:r*50', speed=2, midinote='C5,C5,G5,G5',
        cut=1, p=0.25, orbit=1, shape=0.5)
Pg >> d('bip:r*50', squiz=4, speed=1, midinote='C5@fifths', shape=0.5,
        cut=1, p=0.25, orbit=1)

Pa >> None
Pb >> None
Pc >> None
Pd >> None
PE >> d('long:3', cut=1, begin="[0.0:0.6,0.1]", speed='2!4,4!4')


PE >> d('long:3', cut=1, begin="[0.0:0.6,0.1]")
Pc >> d('ff:4!3, gg:12', cut=1, p=0.25, orbit=1, shape=0.5)
Pb >> d('f!7', cut=0, p=1, orbit=2, shape=0.5)
Pd >> d('g:10', p='.5, .5, .25', orbit=2, shape=0.5, speed='2,2,1!2,4')
Pf >> d('bip:r*50', speed=2, midinote='C5,C5,G5,G5',
        cut=1, p=0.25, orbit=1, shape=0.5)
Pg >> d('bip:r*50', squiz=4, speed=1, midinote='C5@fifths', shape=0.5,
        cut=1, p=0.25, orbit=1)

###################################################################
# █▀▀ ▄▀█ █▀█ █▀█ ▀█▀ ▀█▀ █▀▀   █ █▄░█ ▀█▀ █▀▀ █▀█ █░░ █░█ █▀▄ █▀▀#
# █▄▄ █▀█ █▀▄ █▄█ ░█░ ░█░ ██▄   █ █░▀█ ░█░ ██▄ █▀▄ █▄▄ █▄█ █▄▀ ██▄#
###################################################################

panic()

@swim 
def baba(p=0.5, i=0): 
    D('juppad:54, juppad:55', cutoff=2000, begin=0.1, 
      orbit=2, cut=0, legato=1.1, i=i, d=8, r=0.25)
    again(baba, p=1/4, i=i+1)

@swim 
def baba(p=0.5, i=0): 
    D('juppad:54, juppad:55', cutoff=5000, begin=0.1, 
      orbit=2, cut=0, legato=1.1, i=i, d=8, r=0.25)
    D('boop:r*20', shape=0.4, 
      midinote='G4|G5,Bb5,F6, G4|G5,Bb5,G6', i=i, r=0.25, d=2)
    D('boop:r*40')
    again(baba, p=1/4, i=i+1)

@swim 
def baba(p=0.5, i=0): 
    # D('f', shape=0.4, i=i, d=4)
    # D('f:3', amp='[0:0.4,0.05]', legato='0.01~0.2', i=i)
    D('.., p:5, .', legato=0.5, shape=0.7, i=i, d=1)
    D('juppad:54, juppad:55', cutoff=5000, begin=0.1, 
      orbit=2, cut=0, legato=1.1, i=i, d=8, r=0.25)
    D('.., p:6, ., .., p:3, ..', legato=0.5, shape=0.7, i=i)
    D('bip:r*20', midinote='adisco((G|[G,G|Ab|G5])!2)', i=i, d=2)
    again(baba, p=1/4, i=i+1)

@swim 
def baba(p=0.5, i=0): 
    D('f, f, ..', shape=0.4, i=i, d=4)
    D('f:4', amp='[0:0.4, 0.05]', legato='0.1~0.5', i=i)
    D('.., p:5, .', legato=0.5, shape=0.7, i=i)
    D('juppad:54, juppad:55', cutoff=5000, begin=0.1, 
      squiz=2, orbit=2, cut=0, legato=1.1, i=i, d=8, r=0.25)
    again(baba, p=1/4, i=i+1)

@swim 
def baba(p=0.5, i=0): 
    D('f', shape=0.4, i=i, d=4)
    D('f:8~12', speed='4~8', amp='[0:0.4, 0.05]', legato='0.1~0.5', i=i)
    D('.., p:5, .', legato=0.5, shape=0.7, i=i, d=1)
    D('laz:r*20', 
            speed="1, 2,4",  hcutoff='3000~6000',
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4, i=i, d=0.25)
    D('juppad:54, juppad:55', cutoff=5000, begin=0.1, 
      squiz='0!4,2',
      orbit=2, cut=0, legato=1.1, i=i, d=8, r=1)
    again(baba, p=1/4, i=i+1)

@swim 
def baba(p=0.5, i=0): 
    # D('f', shape=0.4, i=i, d=4)
    # D('f:3', speed=4, amp='[0:0.4, 0.05]', legato='0.1~0.5', i=i)
    D('.., p:5, .', legato=0.5, shape=0.7, i=i)
    D('laz:r*20', 
            speed="1, 2,4",  hcutoff=6000,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4, i=i, d=1, r=0.25)
    D('juppad:54, juppad:55', cutoff=5000, begin=0.1, 
      pan='r', speed='1|2|4', leslie=1, lesliespeed=8,
      orbit=2, cut=0, legato=1.1, i=i, d=8, r=0.25)
    again(baba, p=1/4, i=i+1)

@swim 
def baba(p=0.5, i=0): 
    D('f', shape=0.4, i=i, d=4)
    D('.., p:5, .', legato=0.5, shape=0.7, i=i)
    D('conga:r*20', speed="[1,2,4]/4", hcutoff='500~1000', shape=0.4,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.5, i=i, d=1, r=0.25)
    D('kit2:3', shape=0.5, i=i, d=8)
    D('., kit2:10, ., kit2:9!2', shape=0.5, i=i, d=2)
    again(baba, p=1/4, i=i+1)


@swim 
def baba(p=0.5, i=0): 
    D('f', shape=0.4, i=i, d=4)
    D('.., p:5, .', legato=0.5, shape=0.7, i=i)
    D('conga:r*20', speed="[1,2,4]/4", hcutoff='500~1000', shape=0.4,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.5, i=i, d=1, r=0.25)
    D('conga:r*20', speed="[1,2,4]/2", hcutoff='2000', shape=0.4,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.5, i=i, d=2, r=0.5)
    D('kit2:3', shape=0.5, i=i, d=8)
    D('., kit2:10, ., kit2:9!2', shape=0.5, i=i, d=2)
    again(baba, p=1/4, i=i+1)

# Ici on joue uniquement avec les percus et on lave les oreilles

@swim 
def baba(p=0.5, i=0): 
    D('f:3', amp='[0:0.2,0.01]', legato='0.1~0.5', i=i)
    D('.., p:(5|10), .', legato=0.5, i=i, d=1)
    D('m|c:[4:9]', legato=0.2, i=i, d='4!12, 3!12')
    D('jupbass:[1:100]', # -> lost into jupfx
            cutoff=3000, # ->
            shape=0.5,
            pan='sin($/40)', # -> X
            legato=0.2, # ->
            begin='r', i=i)
    again(baba, p=1/4, i=i+1)


@swim 
def baba(p=0.5, i=0): 
    D('a', shape=0.7, i=i, d=4)
    D('c', shape=0.7, i=i, d=3)
    D('d:7', orbit=3, room=0.2, size=0.8, dry=0.2, i=i, d=8)
    D('hhh:3', amp='[0:0.2, 0.01]', legato='0.1~0.5', i=i)
    D('f:3', amp='[0:0.2,0.01]', legato='0.1~0.5', i=i)
    D('.., p:(5|10), .', legato=0.5, i=i, d=1)
    D('m|c:[4:9]', legato=0.2, i=i, d='4!12, 3!12')
    D('jupbass:[1:100]', # -> lost into jupfx
            cutoff=3000, # ->
            shape=0.5,
            pan='sin($/40)', # -> X
            legato=0.2, # ->
            begin='r', i=i)
    again(baba, p=1/4, i=i+1)

panic()
D('girls:2')


#####################################################################
# █▀▀ █▀█ █▀▄▀█ █▀█ █░█ ▀█▀ █▀▀ █▀█   █░░ ▄▀█ █▀▄▀█ █▀▀ █▄░█ ▀█▀ █▀█#
# █▄▄ █▄█ █░▀░█ █▀▀ █▄█ ░█░ ██▄ █▀▄   █▄▄ █▀█ █░▀░█ ██▄ █░▀█ ░█░ █▄█#
#####################################################################

@swim
def structure(p=0.5, i=0):
    N("C2,C3", chan=2, vel=120, i=i)
    N("G5,G4", chan=2, vel=120, i=i, r=0.25/4)
    N("[G6]-[0:12]", chan=2, vel=120, i=i, r=0.25/2)
    CC(**jupcc['cutoff'], value=100)
    CC(**jupcc['decay'], value=80)
    N("[G6]-[0:12]", chan=1, vel=120, i=i, r=0.25/2)
    again(structure, p=0.5, i=i+1)

@swim
def structure(p=0.5, i=0):
    N("C2,C3", chan=2, vel=120, i=i)
    N("G5,G4", chan=2, vel=120, i=i, r=0.25/4)
    N("[G6|D5]-[0:12]", chan=2, vel=120, i=i, r=0.25/2)
    again(structure, p=0.5, i=i+1)

@swim
def structure(p=0.5, i=0):
    CC(**padcc['timbre'], value='50~120')
    N("C2,C3", chan=2, vel=120, i=i)
    N("G5,G4", chan=2, vel=120, i=i, r=0.25/4)
    N("[G6]-[0:12]", chan=2, vel=120, i=i, r=0.25/2)
    again(structure, p=0.5, i=i+1)

@swim
def structure(p=0.5, i=0):
    N("C2,C3", chan=2, vel=120, i=i)
    N("G5,G4", chan=2, vel=120, i=i, r=0.25/4)
    N("[G6]-[0:12]", chan=2, vel=120, i=i, r=0.25/2)
    N("[G7]-[0:12]", chan=2, vel=120, i=i, r=0.25/1)
    again(structure, p=0.5, i=i+1)

@swim
def structure(p=0.5, i=0):
    CC(**padcc['timbre'], value='(90~100)-10') # go down
    N("C2,C3", chan=2, vel=120, i=i)
    N("G5,G4", chan=2, vel=120, i=i, r=0.25/4) # middle voice
    N("Eb4, F4, G4", chan=2, vel='50~100', i=i, r=0.25/2)
    N("pal(C|C5|C6@minor)", d=2, 
      chan=2, vel='50~100', i=i, r=0.25/2)
    again(structure, p=0.5, i=i+1)

@swim
def structure(p=0.5, i=0):
    CC(**padcc['timbre'], value='(70~110)') # go down
    N("C2,C3", chan=2, vel=120, i=i)
    N("G5,G4", chan=2, vel=120, i=i, r=0.25/4)
    N("Eb4, F4, G4", chan=2, vel='50~100', i=i, r=0.25/2)
    N("pal(C|C5|C6@minor)", d=2, 
      chan=2, vel='50~100', i=i, r=0.25/2)
    CC(**basscc['timbre'], value='r*127')
    CC(**basscc['fx'], value='80')
    CC(**basscc['cutoff'], value='[1:127,20]')
    N("disco(pal(C3|C5|C4@minor))", d=1, 
      chan=0, vel='(50~100)-30', i=i, r=0.25)
    again(structure, p=0.5, i=i+1)

@swim
def structure(p=0.5, i=0):
    N("C2,C3", chan=2, vel=120, i=i)
    N("G5,G4", chan=2, vel=120, i=i, r=0.25/4)
    N("Eb4, F4, G4", chan=2, vel='50~100', i=i, r=0.25/2)
    CC(**basscc['cutoff'], value=127, i=i)
    N("pal(C|C5|C6@minor)", d=2, 
      chan=2, vel='50~100', i=i, r=0.25/2)
    N("disco(pal(C3|C5|C4@minor))", d=1, 
      chan=0, vel='50~100', i=i, r=0.25)
    D('ff', d='3, 3, 2', i=i, cutoff=2500)
    D('s, u, n, d, o, w, n', d='3, 3, 2', i=i, p=0.5)
    D('kk:2~8, bb:1~9', legato=0.2, d='2, 3, 1!4', i=i, 
      speed='0.25, 0.5!5, 1!8')
    again(structure, p=0.5, i=i+1)


@swim
def structure(p=0.5, i=0):
    N("C2,C3", chan=2, vel=120, i=i)
    N("G5,G4", chan=2, vel=120, i=i, r=0.25/4)
    N("Eb4, F4, G4", chan=2, vel='50~100', i=i, r=0.25/2)
    CC(**basscc[pick('timbre', 'cutoff')], value='20~120', i=i)
    CC(**basscc[pick('time')], value='20', i=i)
    N("pal(C|C5|C6@minor)", d=2, 
      chan=2, vel='50~100', i=i, r=0.25/2)
    N("disco(pal(C4|C6|C5@minor))", d=1, 
      chan=0, vel='50~100', i=i, r=0.25)
    D('ff', d='3, 3, 2', i=i, cutoff=2500)
    D('s, u, n, d, o, w, n', d='3, 3, 2', i=i, p=0.5)
    D('kk:2~8, bb:1~9', legato=0.2, d='2, 3, 1!4', i=i, 
      speed='0.25, 0.5!5, 1!8')
    again(structure, p=0.5, i=i+1)

Pb >> d('g,o,o,d,b,y,e,t,r,a,c,k', d='1', p=0.5, orbit=2, cut=0)

@swim
def structure(p=0.5, i=0):
    N("C2,C3, F2, F3", chan=2, vel=120, i=i)
    N("G5,G4, Ab5, Ab4", chan=2, vel=120, i=i, r=0.25/4)
    N("Eb4, F4, G4, Eb4, Eb5, Eb4, Eb5", chan=2, vel='50~100', i=i, r=0.25/2)
    N("pal(F|F5|G6@minor)", d=2, 
      chan=2, vel='50~100', i=i, r=0.25/2)
    again(structure, p=0.5, i=i+1)


Pc >> d('s, u, n, d, o, w, n', d='3, 3, 2', p='0.25!16, 0.5!4', orbit=3, cut=1, speed='2,4')

@swim
def structure(p=0.5, i=0):
    N("pal(F|F4|G3@minor)", d=2, 
      chan=2, vel='100~120', i=i, r=0.25/2)
    N("pal(F|F5|G6@minor)", d=2, 
      chan=2, vel='100~120', i=i, r=0.25/2)
    again(structure, p=0.5, i=i+1)

############################################################
# IDEE POUR UN TROISIEME MORCEAU
############################################################

silence(structure)
Pc >> None
@swim(snap=0)
def baba(p=0.5, i=0):
    D('ff', i=i, d=4, shape=0.5)
    D('s:[1:20]', i=i, d=3, speed='1|1|2|4', legato=0.4, pan='r')
    D('l:[1:20]', i=i, d=2, speed='1|1|2|4', legato=0.2, pan='r')
    D('jupfx:[0:20]', midinote='rev(C3, Eb3, G, Bb4|Bb5)',
      room=0.5, size=0.21, dry=0.12, orbit=3, amp=0.25,
      i=i, d=2, speed='1|1|2|4', legato=0.08, pan='r')
    again(baba, p=0.25, i=i+1)


Pb >> None
@swim(snap=0)
def baba(p=0.5, i=0):
    D('long', orbit=3, cut=1, begin='r', i=i)
    D('ff', i=i, d=4)
    D('kit2:[1,20]', legato=0.1, i=i, d='3!32, 4!16', speed='1,2')
    again(baba, p=0.25, i=i+1)


@swim(snap=0)
def baba(p=0.5, i=0):
    D('ulh:60', orbit=3, cut=1, begin='r', i=i)
    D('ff', i=i, d=4)
    D('ff:9', i=i, d=8, orbit=2)
    if sometimes():
        D('ff:r*40', i=i, d=2, orbit=2, legato=0.1)
    else:
        D('bb|gg:r*40', speed='<1,2>,4', i=i, d=1, orbit=2, legato='0.01~0.2')
    D('kit2:[1,20]', legato=0.1, i=i, d='3!32, 4!16', speed='1,2')
    again(baba, p=0.25, i=i+1)
# Change p to 2, I don't know why but it is working

panic()


##################################################################
# █░█ █▀█ █░░ ▄▀█ █ █░░ █░░ █▀▀   █▀▄ █▀▀   █▄▄ █▀█ █▀▀ █▀ █▀ █▀▀#
# ▀▄▀ █▄█ █▄▄ █▀█ █ █▄▄ █▄▄ ██▄   █▄▀ ██▄   █▄█ █▀▄ ██▄ ▄█ ▄█ ██▄#
##################################################################

Pa >> d('juppad:12|51', begin='r', amp=0.20, speed='1', legato=4,
        room=0.5, orbit=3, dry=0.2, size=0.8,
        midinote='Do,Fa,Ab3,Eb4', cutoff=4000)

Pb >> d('bip:r*50', begin='0,0.2,0.5', amp=0.45, speed='2', 
        room=0.5, orbit=3, dry=0.2, size=0.8,
        legato=0.18, midinote='adisco(Do,Fa,Ab3,Eb4)', cutoff=8000, p=0.5)

Pd >> d('ff:4', shape=0.5, speed=1, p=0.5, cutoff='[200:2000,100]', amp=0.5)


Pa >> d('juppad:12|51', begin='r', amp=0.20, speed='1', legato=4,
        room=0.5, orbit=3, dry=0.2, size=0.8,
        midinote='Do,Fa,Ab3,Eb4', cutoff=4000)
Pb >> d('bip:r*50', begin='0,0.2,0.5', amp=0.45, speed='2', 
        room=0.5, orbit=3, dry=0.2, size=0.8,
        legato=0.18, midinote='adisco(Do,Fa,Ab3,Eb4)', cutoff=8000, p=0.5)
Pc >> d('ff', shape=0.5, speed=1, p=1, cutoff='[2000:5000,100]')
Pc >> d('nn:4~8', legato=0.2, 
        shape=0.5, speed='1,2', p=0.5, cutoff='[2000:5000,100]')
Pe >> d('ff', shape=0.5, speed=1, p=2, cutoff='[200:2000,100]')

Pc >> d('[f,i,s,h,e,s]:[1:20]', shape=0.5, p=0.5, legato=0.02, pan='r')
Pd >> d('euclid([gg:r*20]!8, 5,8)', shape=0.5, speed=4,
        p=0.5, cutoff='5000', resonance='0.1,0.2')

Pb >> None # d('j, a, j, a', orbit=2, p='1,0.5')
Pc >> None # d('f, l, o, w, e, e:r*4', shape=0.5)
Pd >> None # d('bb:5~6', p='0.25, 0.125', legato=0.05)

panic()
```
