# Solstice

2 performances were made with Sardine during the TidalCycles Annual Solstice Stream. The former by Bubobubo, the latter by Ralt144MI.

# Bubo

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
Pc >> d('bip:rand*20', speed=2,
        cut=0, p=0.25, orbit=1, shape=0.5, hcutoff='[500:15000,1000]')

# ---

PE >> d('long:3', cut=1, begin="[0.0:0.6,0.1]")
Pc >> d('ff:4!3, gg:12', cut=1, p=0.25, orbit=1, shape=0.5)
Pb >> d('f!7', cut=0, p=1, orbit=2, shape=0.5)
Pd >> d('g:10', p='.5, .5, .25', orbit=2, shape=0.5, speed='2,2,1!2,4')
Pf >> d('bip:rand*50', speed=2, midinote='C5,C5,G5,A5',
        cut=1, p=0.25, orbit=1, shape=0.5)
Pg >> d('bip:rand*50', squiz=4, speed=1, midinote='C3,C4,G3,G4,A4,A5', shape=0.5,
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
Pf >> d('bip:rand*50', speed=2, midinote='C5,C5,G5,G5',
        cut=1, p=0.25, orbit=1, shape=0.5)
Pg >> d('bip:rand*50', squiz=4, speed=1, midinote='C5@fifths', shape=0.5,
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
Pf >> d('bip:rand*50', speed=2, midinote='C5,C5,G5,G5',
        cut=1, p=0.25, orbit=1, shape=0.5)
Pg >> d('bip:rand*50', squiz=4, speed=1, midinote='C5@fifths', shape=0.5,
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
    D('boop:rand*20', shape=0.4,
      midinote='G4|G5,Bb5,F6, G4|G5,Bb5,G6', i=i, r=0.25, d=2)
    D('boop:rand*40')
    again(baba, p=1/4, i=i+1)

@swim
def baba(p=0.5, i=0):
    # D('f', shape=0.4, i=i, d=4)
    # D('f:3', amp='[0:0.4,0.05]', legato='0.01~0.2', i=i)
    D('.., p:5, .', legato=0.5, shape=0.7, i=i, d=1)
    D('juppad:54, juppad:55', cutoff=5000, begin=0.1,
      orbit=2, cut=0, legato=1.1, i=i, d=8, r=0.25)
    D('.., p:6, ., .., p:3, ..', legato=0.5, shape=0.7, i=i)
    D('bip:rand*20', midinote='adisco((G|[G,G|Ab|G5])!2)', i=i, d=2)
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
    D('laz:rand*20',
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
    D('laz:rand*20',
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
    D('conga:rand*20', speed="[1,2,4]/4", hcutoff='500~1000', shape=0.4,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.5, i=i, d=1, r=0.25)
    D('kit2:3', shape=0.5, i=i, d=8)
    D('., kit2:10, ., kit2:9!2', shape=0.5, i=i, d=2)
    again(baba, p=1/4, i=i+1)


@swim
def baba(p=0.5, i=0):
    D('f', shape=0.4, i=i, d=4)
    D('.., p:5, .', legato=0.5, shape=0.7, i=i)
    D('conga:rand*20', speed="[1,2,4]/4", hcutoff='500~1000', shape=0.4,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.5, i=i, d=1, r=0.25)
    D('conga:rand*20', speed="[1,2,4]/2", hcutoff='2000', shape=0.4,
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
    CC(**basscc['timbre'], value='rand*127')
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
        D('ff:rand*40', i=i, d=2, orbit=2, legato=0.1)
    else:
        D('bb|gg:rand*40', speed='<1,2>,4', i=i, d=1, orbit=2, legato='0.01~0.2')
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

Pb >> d('bip:rand*50', begin='0,0.2,0.5', amp=0.45, speed='2',
        room=0.5, orbit=3, dry=0.2, size=0.8,
        legato=0.18, midinote='adisco(Do,Fa,Ab3,Eb4)', cutoff=8000, p=0.5)

Pd >> d('ff:4', shape=0.5, speed=1, p=0.5, cutoff='[200:2000,100]', amp=0.5)


Pa >> d('juppad:12|51', begin='r', amp=0.20, speed='1', legato=4,
        room=0.5, orbit=3, dry=0.2, size=0.8,
        midinote='Do,Fa,Ab3,Eb4', cutoff=4000)
Pb >> d('bip:rand*50', begin='0,0.2,0.5', amp=0.45, speed='2',
        room=0.5, orbit=3, dry=0.2, size=0.8,
        legato=0.18, midinote='adisco(Do,Fa,Ab3,Eb4)', cutoff=8000, p=0.5)
Pc >> d('ff', shape=0.5, speed=1, p=1, cutoff='[2000:5000,100]')
Pc >> d('nn:4~8', legato=0.2,
        shape=0.5, speed='1,2', p=0.5, cutoff='[2000:5000,100]')
Pe >> d('ff', shape=0.5, speed=1, p=2, cutoff='[200:2000,100]')

Pc >> d('[f,i,s,h,e,s]:[1:20]', shape=0.5, p=0.5, legato=0.02, pan='r')
Pd >> d('euclid([gg:rand*20]!8, 5,8)', shape=0.5, speed=4,
        p=0.5, cutoff='5000', resonance='0.1,0.2')

Pb >> None # d('j, a, j, a', orbit=2, p='1,0.5')
Pc >> None # d('f, l, o, w, e, e:rand*4', shape=0.5)
Pd >> None # d('bb:5~6', p='0.25, 0.125', legato=0.05)

panic()
```
# Ralt144MI

## Description

Playing with Sardine with all my gear and visual setup. I'm controlling a lot of synths through MIDI: A Yamaha Electone c35, Marimba MIDI Controller, Korg MS2000R, Yamaha TX7, Behringer Model D, Roland PMA-5, Alesis MIDIVERB 3, Marantz CP130, a circuit bent Panasonic Ave5, bespoke scuba-diving mask repurposed as a microphone, a very special **livecodinD** keyboard, a shitty Behringer mixing console, lots of audio and composite cables, three webcams and an analog video to digital converter.

## Performance


<iframe width="560" height="315" src="https://www.youtube.com/embed/0LJhukm8-kY" title=" Solstice Night Stream December 2022 - Ralt144MI - 2022-12-21 17:40 " frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Source code

```
#-------------------------------------------------------------
#------ooooo  oooooo oo   oooooo oo oo     oo     o   o oo----
#------oo  oo oo  oo oo     oo   oo oo oo  oo oo  oo oo oo----
#------ooooo  oooooo oo     oo   oo oooooo oooooo o o o oo----
#------oo  oo oo  oo oooooo oo   oo    oo     oo  o   o oo----
#-------------------------------------------------------------
#-------------------------------------------------------------
#----------------------------------------- <^[[[>< ------_____
#------------------------------------------------------_/-----
#Salut moi c'est Ralt144MI----------___---------------/-_-----
#----------------------------------[ooo]--------(---3)>[#]----
#-----------------------------------(-(-------)-)-(--|--------
#------------------------------------)-)----_-(-(-)-|---------
#------------------------------------------/-\)-)-(/----------


tx7_params = {
        "Algorithme": lambda x: midi._sysex([67,16,1,6,(int(x)%31)+1]),
        "Feedback": lambda x: midi._sysex([67,16,1,7,(int(x)%7)+1]),
        # FreqCourse
        "FreqCourseOp1": lambda x: midi._sysex([67,16,0,123,int(x)%32]),
        "FreqCourseOp2": lambda x: midi._sysex([67,16,0,102,int(x)%32]),
        "FreqCourseOp3": lambda x: midi._sysex([67,16,0,60, int(x)%32]),
        "FreqCourseOp4": lambda x: midi._sysex([67,16,0,60, int(x)%32]),
        "FreqCourseOp5": lambda x: midi._sysex([67,16,0,39, int(x)%32]),
        "FreqCourseOp6": lambda x: midi._sysex([67,16,0,18, int(x)%32]),
        # FreqFine
        "FreqFineOp1": lambda x: midi._sysex([67,16,0,124,int(x)%127]),
        "FreqFineOp2": lambda x: midi._sysex([67,16,0,103,int(x)%127]),
        "FreqFineOp3": lambda x: midi._sysex([67,16,0,82, int(x)%127]),
        "FreqFineOp4": lambda x: midi._sysex([67,16,0,61, int(x)%127]),
        "FreqFineOp5": lambda x: midi._sysex([67,16,0,40, int(x)%127]),
        "FreqFineOp6": lambda x: midi._sysex([67,16,0,19, int(x)%127]),
        # Detune
        "DetuneOp1": lambda x: midi._sysex([67,16,0,125,int(x)%14]),
        "DetuneOp2": lambda x: midi._sysex([67,16,0,104,int(x)%14]),
        "DetuneOp3": lambda x: midi._sysex([67,16,0,83,int(x)%14]),
        "DetuneOp4": lambda x: midi._sysex([67,16,0,62,int(x)%14]),
        "DetuneOp5": lambda x: midi._sysex([67,16,0,41,int(x)%14]),
        "DetuneOp6": lambda x: midi._sysex([67,16,0,20,int(x)%14]),
        # Level
        "LevelOp1" : lambda x: midi._sysex([67,16,0,121,int(x)%99]),
        "LevelOp2" : lambda x: midi._sysex([67,16,0,100,int(x)%99]),
        "LevelOp3" : lambda x: midi._sysex([67,16,0,79,int(x)%99]),
        "LevelOp4" : lambda x: midi._sysex([67,16,0,58,int(x)%99]),
        "LevelOp5" : lambda x: midi._sysex([67,16,0,37,int(x)%99]),
        "LevelOp6" : lambda x: midi._sysex([67,16,0,16,int(x)%99]),
        # LFO
        "LFOWave":  lambda x: midi._sysex([67,16,1,14,int(x)%6]),
        "LFOSpeed": lambda x: midi._sysex([67,16,1,9,int(x)%99]),
        "LFODelay": lambda x: midi._sysex([67,16,1,10,int(x)%99]),
        "LFOPMD":   lambda x: midi._sysex([67,16,1,11,int(x)%99]),
        "LFOAMD":   lambda x: midi._sysex([67,16,1,12,int(x)%99]),
        "LFOSync":  lambda x: midi._sysex([67,16,1,12,int(x)%1]),
        "LFOPMS":   lambda x: midi._sysex([67,16,1,15,int(x)%5]),
        # Portamento
        "Retain/Follow" : lambda x: midi._sysex([67,16,8,67,int(x)%1]),
        "GlissandoOffOn"          : lambda x: midi._sysex([67,16,8,68,int(x)%1]),
        "Time"                    : lambda x: midi._sysex([67,16,8,69,int(x)%99]),
        "Poly/Mono"               : lambda x: midi._sysex([67,16,8,64,int(x)%1]),
}


def tx7(algo, pattern: Union[int, str], iterator=None,
        div:int = 1, rate:int = 1) -> midi._sysex:
    """
    Custom function for Rémi Georges. Allows the patterning of a Yamaha TX7.
    A pattern can be written for each and every declared Sysex parameter.
    """
    if isinstance(pattern, int):
        return tx7_params[algo](pattern)
    elif isinstance(pattern, str):
        return tx7_params[algo](int(Pat(pattern, i=iterator, div=div, rate=rate)))

def E(step: int, maximum: int, index: int) -> bool:
    pattern = euclid(step, maximum)
    return True if pattern[index % len(pattern)] == 1 else False

def print_param():
    print(tx7_params.keys())

def print_scales():
    print(qualifiers.keys())

Pp >> tx7("Algorithme", 12)


####################################################
####################################################
####################################################
HI Im Ralt144MI, :)
################################################################
################################################################
################################################################
################################################################
si soucis
dirt ahead 0.3 ?

dirt._ahead_amount = 0.20

silence()

Po >> d("leCASIO:[0,2,1,2,0,2,1,3]", #-8 #^[0~4]
        speed ="[1, 2, 3, 4, 5]/[2~3]",
        p="0.50!4",
        gain = 1.1,
            #p = "[1:8]", #KIller
            #span = 8, #Killer
        span = 2,
        legato = 1)

Po >> None

#MODEL ACID BASS RIGHT EAR


@swim
def labass(p=0.5, i=0):
    N(
            "bass(F3@maj7)^[1~2]",
            #"adisco(F3@maj7)^[1~2]",
            #"disco(F3@maj7)^[1~2]",
            #"pal(F3@maj7)^[2~3]",
            vel = '[45~85]',
            dur = 0.05,
            chan = 2,
            d="0.5!3,0.25!2",
            i=i,
            r=0.25/2
            )
    again(labass,p=0.5,i=i+1)


#GRUSIN  ENSUIT AUG
Pn >> n(note= "euclid(<F2@aug>!8,5,8)",
        vel=70,
        p=0.5,
        span=1)

Pn >> None

#mute CASIOTIME

Po >> None

################MEDLERS###############
@die
def tempomedler(p=0.5, i = 0):
    if clock.tempo < 150 :
        clock.tempo = clock.tempo*1.02
    else :
        clock.tempo = 60
    again(tempomedler, p=0.5, i=i+1)

@die
def algomedler(p=0.5, i=0):
    tx7("Algorithme",i)
    again(algomedler, p=0.5, i=i+1)

@die
def bouncer(p=0.5, i=0):
    tx7('Retain/Follow', 1,i)
    tx7('GlissandoOffOn', 1,i)
    tx7('Time', 40,i) #descendre pour plus de fun
    again(bouncer, p=0.5, i=i+1)


Pi >> None
Po >> None

Pn >> None

silence()

Pb >> d("morgan:0", begin ="rand*0.8",
        legato = 4, p = "1,0.5", span = 4,
        bandf = 300, #300
        )

Ps >> d("morgan:0",
        scram = "r",
        legato = 4, begin = 0.425,
        room= .4, cutoff = 4500, shape = 0.25,
        p=32
        #p="8!2,16!4"
        )

Pf >> d(".,morgan:1",
        scram = "r",
        legato = 4.5, begin = 0.430,
        cutoff = 4500, hcutoff = 250,
        shape = 0.45,
        p=9
        #p="4.5"
        )

Pl >> d("long:[24~59]", p="2,1",
        legato = 0.5, pan = "r",
        scram = 0.2, gain = 0.9,
        room = .4
        )

#reduire les cutoff de Morgan
Ps >> None
Pf >> None



Pi >> d("long:42", p=4,
        legato =2, gain = 0.8,
        speed = "2,1,0.5,0.25",
        room = .6
        )

PL >> d("long:45",
        room = .4,
        p = 8,
        legato =1)

Pn >> None

PM >> d("long:40", p=0.25,
        span = 2, #1
        legato = 0.5)

clock.tempo = 135

Pl >> None
PL >> None
Pb >> None

silence()

dirt._ahead_amount = 0.20


Pk >> d("leKICK:2",
        p="0.5!4",
        span=4
        )

Pk >> None

#                  [x|.]       .5
Ps >> d('.,laSNARE:6', span = 1,gain= 0.9, p=1)

Ph >> d("leHIHAT:$%5", cutoff = 6000, legato = 0.1, p=0.25)

#C15 DISCO BASS
Pn >> n(note="pal(disco(E4@min7))^[1~3]",
        p="1,1,0.5,0.5,0.25,0.25,0.25,0.25",
        span = 4, dur = 0.1,
        chan="1"
        )

Pn >> None
#SYNELECPNO CMB18
Pt >> n(note="pal(adisco(E4@min7)),<E4@min7>",
        p = "[1!3,0.5!2]",
        span = 2,
        chan=0, dur = 0.1
        )

Pt >> None


silence()

Pn >> d("laPERC:10!2, laSNARE:12, laPERC:2",
        p = "1,0.5",
        shape= 0.4 ,legato = 1,
        span = 2,
        #speed = "0.84,0.13,1,1" #"0.84,0.43,1,1"
        )

#mets le vocode

Ph >> d("leHIHAT:6", p=0.25, pan = "r",
        gain = .9)

D("ralt144mi,.!7", accelerate = "1",
        gain = 1.2,enhance = .2, legato = 2)

silence()

Pi >> None

Pi >> n(note = "[<F'@maj>!2,<C'@maj>!8]", p=0.5,
        span= 2,
        chan = 1)


Pk >> d("leKICK:2!4",
        shape =0.4,
        legato = 0.2,
        #cutoff = 1000,
        resonance = 0.2,
        #p=8 #8
        p = 8, span =1
        )

Pc >> d(#"[.,.,laSNARE:4!2]!4",
        "[.,.,laSNARE:4!2]!3,[.,.,laSNARE:[rand*16]!2]",
        p=1, accelerate= "0!12,0.5,0.75,0.80,1",
        span = 1)


Pc >> None



Pi >> None



silence()
###DOIT BIZAR
Pi >> d("son:[1]",
        speed = "euclid(([[1,2,3,4,5,6,7,8]/7]^[0.5~-1]),7,1)",
        shape = 0.5, gain =0.8,
        p="(0.125*r)!2", pan = "[1:7]",
        span = 1,
        accelerate =1,
        legato=0.7)

clock.tempo = 152

#VIBRATIME ORGANTIME VIDEOTIME

Pu >> n("euclid(<C3,E3,C4,E4>!8,5,8)",
        p = "0.25",
        vel = 65, span  = 0.5,
        chan = "0", dur = 0.25)

Pi >> None

n("apal(disco(F2@maj7))^[(1)~5]",
        vel=65,p="0.5!7,0.25!2",
        span = 4,
        #chan = "15,0,1,2",
        chan="0",
        dur = 0.15)

Pa >> None

Pa >> n("euclid(<E7>!8,3,5,2)",
        p = "0.125",
        vel = 85, span  = 0.5,
        chan = "0", dur = 0.25)

silence()


Pk >> d("leKICK:2!4",
        shape =0.4,
        legato = 0.2,
        #cutoff = 1000,
        resonance = 0.2,
        #p=8 #8
        p = 8, span =1
        )

Pk >> None

Pk >> d("leKICK:2!4",
        shape =0.4,
        legato = 0.2,
        #cutoff = 1000,
        resonance = 0.2,
        #p=8 #8
        p = 8, span =1
        )
```



