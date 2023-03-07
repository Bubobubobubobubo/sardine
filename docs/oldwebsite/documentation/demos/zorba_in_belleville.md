# Zorba in Belleville (11/11/2022)

## Description

This code is taken from an algorave that took place at the **Zorba** (*Belleville*, Paris) in early november (2022). It is a very straightforward dance oriented performance that plays a lot with simple audio sample manipulations. As stated in the opening banner, this performance was meant to test the stability of **Sardine** after introducing new features and control mechanisms. Everything lives in the `baba` function, meaning that you only need to keep track one function during the whole performance.

Sounds are extracted from a very heavy sound library, lazy-loaded when needed. This is how I like to make music, extracting a lof of raw audio files from my hard disk :)

## Performance

<iframe width="1440" height="627" src="https://www.youtube.com/embed/YR-xFDouP_o" title="Zorba in Belleville (Algorave fragments)" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Source code

```python
# ██████████████████████████████████████████████████████████████████████████████████████████████████████████████████
# █░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░███░░░░░░░░░░░░███░░░░░░░░░░█░░░░░░██████████░░░░░░█░░░░░░░░░░░░░░█
# █░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀▄▀░░░░█░░▄▀▄▀▄▀░░█░░▄▀░░░░░░░░░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█
# █░░▄▀░░░░░░░░░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░▄▀░░███░░▄▀░░░░▄▀▄▀░░█░░░░▄▀░░░░█░░▄▀▄▀▄▀▄▀▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█
# █░░▄▀░░█████████░░▄▀░░██░░▄▀░░█░░▄▀░░████░░▄▀░░███░░▄▀░░██░░▄▀░░███░░▄▀░░███░░▄▀░░░░░░▄▀░░██░░▄▀░░█░░▄▀░░█████████
# █░░▄▀░░░░░░░░░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░▄▀░░███░░▄▀░░██░░▄▀░░███░░▄▀░░███░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█
# █░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀░░██░░▄▀░░███░░▄▀░░███░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█
# █░░░░░░░░░░▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░▄▀░░░░███░░▄▀░░██░░▄▀░░███░░▄▀░░███░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█
# █████████░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█████░░▄▀░░██░░▄▀░░███░░▄▀░░███░░▄▀░░██░░▄▀░░░░░░▄▀░░█░░▄▀░░█████████
# █░░░░░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░░░░░█░░▄▀░░░░▄▀▄▀░░█░░░░▄▀░░░░█░░▄▀░░██░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░░░░░░░░░█
# █░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀░░░░█░░▄▀▄▀▄▀░░█░░▄▀░░██░░░░░░░░░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█
# █░░░░░░░░░░░░░░█░░░░░░██░░░░░░█░░░░░░██░░░░░░░░░░█░░░░░░░░░░░░███░░░░░░░░░░█░░░░░░██████████░░░░░░█░░░░░░░░░░░░░░█
# ██████████████████████████████████████████████████████████████████████████████████████████████████████████████████

# █▀▀ █▀█ ▄▀█ █▀ █░█   ▀█▀ █▀▀ █▀ ▀█▀   █░█ █▀▀ █▀█ █▀ █ █▀█ █▄░█   ▄▀█ █░░ █▀█ █░█ ▄▀█   █▀█ ░ █▀█ █▀█ █▀█ █▀█ ▄█
# █▄▄ █▀▄ █▀█ ▄█ █▀█   ░█░ ██▄ ▄█ ░█░   ▀▄▀ ██▄ █▀▄ ▄█ █ █▄█ █░▀█   █▀█ █▄▄ █▀▀ █▀█ █▀█   █▄█ ▄ █▄█ █▄█ █▄█ █▄█ ░█

# @@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@....,.....,..,,,,,,,,,,,,,*(&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@&.,,,,/*//////////**,*.*,*..,***,,,,**********/(%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@(..,*//**/***,,,,,(%((%%,/,%%%%(****,,.,,********,,,*/*/*****///(%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@ .,(/////*,,,,,,,/%%%(*.((,/%%(/.((/%/%//,//,/#%(*****************,,*****///////(&@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@ ./(//*,*,,**,,,,,,,,,,*,*,,**,*/#%%%%%,*#(*(,,(*%(,(*,/*(%(#,/%%/****************,*//*//****/&@@@@@@@@@@@@
# @@@@@@@ .(##***,*,,,,,,,,,,,,,,,,,,,,,*,*,,****,*,****,*(%%%/##/(%,./*//(%(,(%(./((/,*%**************.,****%@@@@@@@
# @@@@@@.*///*********,*,**,,*,,,,,,,%%%%%((#%%%%%,,(%%%%%%%%%%%##%%#,,**/%&%%(/,&(,((/#%%%*,,,,,,,,,,,,,,,..***(@@@@
# @@@@@%/**/*****,,***,,,,,,,,,,,%%%%##/##%%%%%%%%%%%#((**###%%%%####%#####%#(,,********/#%***,,,,,,,,,,,,,,,,.,**/@@
# @@@@@,/**,**************,,,,,*%%%/.((*%*/,/((*#./*. .. ..*,/(##/*,,###*/#/(#%%%#(#,*,#%%%%%%%%%/,,*,,,,,,,,,,..***@
# @@@@ ,/**********,*******,,,,*,% #*,,//#%(.#*,,**#,(##(/**##%##%##/,/#%(//(//,.(#(#%#((,#%%##*##%%%,,,,,,,,,,,. ***
# @@@ .,///*******,*,*,**,,**,,*,,*./ /((..((/(%,,/#(/(/*,*#,.*#/###%%##/**/(/(/.(//%%%%%/###%##,,,%%%***,,,,,,.. .**
# @@@...////*************,***,,,/(((((*.(., #*(  *(..#/(/*(///(##(#(####(/#(*##%(/((%%%%%%%/((#%%%%%%%#***,,,**,   ,*
# @@,..../(//********,,***,,,***(((((( ((*((,,##,,,/###(//*(##((((((#(,       ,(%%#%%,.,(####%###,/%&******,*,*,   .(
# @@*/.,..*(*/***********,*,,*,,,,,**(.((.(((((((((**,(%%%%%%%%###########(*//(#((//*/. *,/(#%##,.,******,**,*,,   ,%
# @@,/*,*.,..(***************,,*,,,*,#*&(**(,* ((  .(((((..((((/********,,*,****/((((((,***********************,   *(
# @/,*/**,,*,,...,*,,*,*,..,,*,,,,,,*,*,**,(#&(,*,/((./(( (( /(. ...(((*../( (#((((((((((**********************  .*#,
# @, *//********/.,,.........,,,,,,,,,,*,,..,,,**,,**##(%&#*****/((#(((((((((((/*,***************************,...**%#
# @% ,*/******//////////**/****,.,,.........,,**/*,,,,,,,,,,,*,*******,************************************,.. **,#,@
# @@* .********/*///////////*/////////*********,,,,,,***//*//////***,*,,,,,,****************************,... ,***/#/@
# @@@#/..********///////////**/*,*,/#.//////////////**********,,.,,**********//*,,,,,,,.,***********,.....,*/*,*(#(&@
# @@@@@&(*,,******///////./,//**/.**//////,/***,/#,,//**,/.////////******/***,,..,,*,...,,**/*,,**,*//*/*****/((#%*@@
# @@@@@@@@%/(/,,,***///////*,,**/**////,**/*/,,**////**///***./*//.*/////////////*******/*,,******,,*//#/(//(((##*%@@
# @@@@@@@@@@@@@((/(((((/*,,,**//****///**,*//****///***.*//**////***////*(%%##%%/&&&///////////////(((((((((((###*@@@
# @@@@@@@@@@@@@@@@@@@@@@&#/(#####(((//*,,,,**/***//******,,***///**./*/**%%&&&###((&&%**//////////(((((((((((((/*@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&#/(####((((/**,,,,**/////****////****/%###%/%&***////////(((((((((((((/,(@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&#/#####(((/(/*,,,,***///****///****/////////(((((((((/**(&@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&(/#####(((((/*,,,******///////((((//**#(%@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&((#####((((#%&%%##%%#%@@@@@@@@@@@@@@

# ███████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#
# █▀▄▀█ █▀▀ █▀█ █▀▀ █   ▀█▀ █░█ █▀▀ █▀█ █▀█ █░█ █ █░░ █▀▀   █░█░█ ▄▀█ █░░ █░░ █▀▀ ▀█   █  █  █
# █░▀░█ ██▄ █▀▄ █▄▄ █   ░█░ █▀█ ██▄ █▄█ █▀▀ █▀█ █ █▄▄ ██▄   ▀▄▀▄▀ █▀█ █▄▄ █▄▄ ██▄ █▄   ▄  ▄  ▄
#
# ███████████████████████████████████████████████████████████████████████████████████████████████████████████████████


# ██████████████████████████████████████████████████████████████████████████████
# █                                                                            █
# █  █   ▄▄   █▀█ ▄▀█ █▀▄▀█ █▀▀ █▀█   █▀ ▄▀█ █▄░█ █▀   █▀█ ▄▀█ █▀▄▀█ █▀▀       █
# █  █   ░░   █▀▄ █▀█ █░▀░█ ██▄ █▀▄   ▄█ █▀█ █░▀█ ▄█   █▀▄ █▀█ █░▀░█ ██▄       █
# █                                                                            █
# ██████████████████████████████████████████████████████████████████████████████

@swim
def baba(d=0.5, i=0):
    S('juppad:3, juppad:4', cutoff=5000, begin=0.1, orbit=2, cut=0, legato=1.1).out(i, 8, 0.25)
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('juppad:3, juppad:4', cutoff=5000, begin=0.1, orbit=2, cut=0, legato=1.1).out(i, 8, 0.25) # up
    # S('bip:rand*20', shape=0.4, midinote='quant([0,3,10]+50, C@minor), quant([0,3,10]+50, F@minor)').out(i, 1, 0.25)
    S('boop:rand*40').out()
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    # S('f', shape=0.7).out(i, 4) # -> monter shape pour les harmoniques
    # S('hhh:3', amp='[0:0.4,0.05]', legato='0.1~0.5').out(i) # -> hhh ramp
    S('.., p:5, .', legato=0.5, shape=0.7).out(i, 1)
    # S('.., p:6, ., .., p:3, ..', legato=0.5, shape=0.7).out(i, 1)
    S('juppad:3, juppad:4', begin=0.1, orbit=2, cut=0, legato=1.1).out(i, 8, 0.25)
    # S('bip:rand*20', midinote='adisco((C|[C,F|Ab])!2)').out(i, 2) # petit surplus harmonique
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('f, f, ..', shape=0.7).out(i, 4) # -> monter shape pour les harmoniques
    S('hhh:3', amp='[0:0.4, 0.05]', legato='0.1~0.5').out(i) # -> hhh ramp
    S('.., p:5, .', legato=0.5, shape=0.7).out(i, 1)
    S('juppad:3, juppad:4', begin=0.1, orbit=2, cut=0,
            legato=1.1, speed='1',
            crush=4).out(i, 8, 0.25) # -> ici il y a de la réduction
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('f', shape=0.7).out(i, 4) # -> monter shape pour les harmoniques
    S('hhh:3', amp='[0:0.4, 0.05]', legato='0.1~0.5').out(i) # -> hhh ramp
    S('.., p:5, .', legato=0.5, shape=0.7).out(i, 1)
    S('laz:rand*20',
            speed="1, 2,4",  hcutoff=6000,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4).out(i, 1, 0.25)
    S('juppad:3, juppad:4', begin=0.1, orbit=2, cut=0,
            legato=1.1, speed='1, 2',
            crush=4).out(i, 8, 0.25) # -> ici il y a de la réduction
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('f', shape=0.7).out(i, 4) # -> monter shape pour les harmoniques
    S('hhh:3', amp='[0:0.4, 0.05]', legato='0.1~0.5').out(i) # -> hhh ramp
    S('.., p:5, .', legato=0.5, shape=0.7).out(i, 1)
    S('laz:rand*20',
            speed="1, 2,4",  hcutoff=6000,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4).out(i, 1, 0.25)
    S('juppad:3, juppad:4', begin=0.1, orbit=2, cut=0,
            pan='r',
            legato=1.1, speed='1|2|4', leslie=1, lesliespeed=8,
            crush=12).out(i, 8, 0.25) # -> ici il y a de la réduction
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('., f', shape=0.7).out(i, 4) # -> monter shape pour les harmoniques
    S('.., p:5, .', legato=0.5, shape=0.7).out(i, 1)
    # S('juppad:3, juppad:4', orbit=2, cut=0, legato=1.1).out(i, 8, 0.25)
    S('laz:rand*20',
            speed="1, 2,4",  hcutoff=3000, legato=1,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4).out(i, 1, 0.25)
    S('juppad:3, juppad:4',
            speed=0.75, squiz=2,
            orbit=2, cut=0,
            legato=1.1).out(i, 8, 0.25)
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('f', shape=0.7).out(i, 4)
    S('.., p:5, .', legato=0.5, shape=0.7).out(i, 1)
    S('conga:rand*20', speed="[1,2,4]/4", hcutoff=2000, shape=0.7,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4).out(i, 1, 0.25)
    S('juppad:3, juppad:4',
            speed=0.75, squiz=2,
            orbit=2, cut=0,
            legato=1.1).out(i, 8, 0.25)
    S('kit2:3', shape=0.5).out(i, 8)
    S('., kit2:10, ., kit2:9!2', shape=0.5).out(i, 2)
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('f', shape=0.7).out(i, 4)
    S('.., p:5, .', legato=0.5, shape=0.7).out(i, 1)
    S('conga:rand*20', speed="[1,2,4]/4", hcutoff=2000, shape=0.7,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4).out(i, 1, 0.25)
    S('conga:rand*20', speed="[1,2,2]/2", hcutoff=1000, shape=0.7,
              room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4).out(i, 1, 0.5)
    # S('juppad:3, juppad:4', # commenter ce bloc
    #         speed=0.75, squiz=2,
    #         orbit=2, cut=0,
    #         legato=1.1).out(i, 8, 0.25)
    S('kit2:3', shape=0.5).out(i, 8)
    S('., kit2:10, ., kit2:9!2', shape=0.5).out(i, 2)
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    # S('f', shape=0.7).out(i, 4)
    S('.., p:5, .', legato=0.5, shape=0.7).out(i, 1)
    S('conga:rand*20', speed="[1,2,4]/4", hcutoff=2000, shape=0.7,
            room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4).out(i, 1, 0.25)
    # S('euclid(conga:rand*20, 12,16)', speed="[1,2,4]/2", hcutoff=1000, shape=0.7,
    #         room=0.5, size=0.2, dry=0.1, orbit=3, amp=0.4).out(i, 1, 0.25)
    # S('juppad:3, juppad:4', # commenter ce bloc
    #         speed=0.75, squiz=2,
    #         orbit=2, cut=0,
    #         legato=1.1).out(i, 8, 0.25)
    S('kit2:3', shape=0.5).out(i, 8)
    S('., kit2:10, ., kit2:9!2', shape=0.5).out(i, 2)
    a(baba, d=1/8, i=i+1)

# Remonter à la ligne 167 pour plus de fun

#############################################################################
## ICI RUPTURE VERS L'INCLUSION DES FOUND SOUNDS
#############################################################################

@swim
def baba(d=0.5, i=0):
    # S('f', shape=0.7, cutoff=100).out(i, 8)
    S('hhh:3', amp='[0:0.2,0.01]', legato='0.1~0.5').out(i) # -> hhh ramp
    S('.., p:(5|10), .', legato=0.5).out(i, 1)
    S('m|c:[4:9]', legato=0.2).out(i, P('4!12, 3!12', i))
    S('lost:[1:100]', # -> lost into jupfx
            cutoff=9000, # ->
            shape=0.5,
            pan='sin($/40)', # -> X
            legato=0.3, # ->
            begin='r').out(i) # -> begin r ou {0, 1, 0.1}
    a(baba, d=1/8, i=i+1)

# Inclure
@swim
def baba(d=0.5, i=0):
    S('a', shape=0.7).out(i, 4) # -> monter shape pour les harmoniques
    S('c', shape=0.7).out(i, 3) # -> monter shape pour les harmoniques
    S('d:7', orbit=3, room=0.2, size=0.8, dry=0.2).out(i, 8)
    S('hhh:3', amp='{0, 0.2, 0.01}', legato='0.1~0.5').out(i) # -> hhh ramp
    S('.., p:5, .', legato=0.5).out(i, 1) # -> refaire entrer ça
    S('m|c:[4:9]', legato=0.2).out(i, P('4!12, 3!12', i))
    S('lost:[1:100]', # -> lost into jupfx
            cutoff=9000, # ->
            shape=0.5,
            pan='sin($/40)', # -> X
            legato=0.9, # ->
            begin='r').out(i) # -> begin r ou {0, 1, 0.1}
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0): # potentiomètre du réel
    S('a', shape=0.7).out(i, P('4!12, 5!12', i)) # -> monter shape pour les harmoniques
    S('c', shape=0.7).out(i, 3) # -> monter shape pour les harmoniques
    # S('c', shape=0.7).out(i, P('3!12, 2!12, 5!12',i)) # -> monter shape pour les harmoniques
    # S('hhh', amp='{0, 0.2, 0.01}', legato='0.1~0.5').out(i) # -> hhh ramp
    S('d:4, d:5, .', legato=0.5).out(i, 3)
    S('m|g:[4:9]', legato=0.2).out(i, P('4!12, 1!24', i))
    S('long|(lost:rand*8)', # -> lost into jupfx
            midinote='C',
            cutoff=4000, # ->
            pan='[0:0.5, 0.1], [0.5:1, 0.1]', # -> X
            legato='0.1|0.2|0.7|0.1',
            cut=1, orbit=2, room=0.5, size=0.2, dry=0.1,
            begin='[0:1,0.01], [1:0,0.01]').out(i) # -> begin r ou {0, 1, 0.1}
    a(baba, d=1/8, i=i+1)

# Ici on peut explorer des choses plus ambient et se perdre un peu

@swim
def baba(d=0.5, i=0): # potentiomètre du réel
    S('a', cutoff=200, shape=0.7).out(i, P('4!12, 5!12', i))
    # S('c', cutoff=100, shape=0.7).out(i, 3)
    # S('c', shape=0.7).out(i, P('3!12, 2!12, 5!12',i))
    # S('hhh', amp='{0, 0.2, 0.01}', legato='0.1~0.5').out(i) # -> hhh ramp
    # S('d:4, d:5, .', legato=0.5).out(i, 3)
    S('m|g:[4:9]', legato=0.2).out(i, P('4!12, 1!24', i))
    S('long|(lost:rand*8)', # -> lost into jupfx
            midinote='C',
            cutoff=4000, # ->
            pan='[0:0.5, 0.1], [0.5:1, 0.1]', # -> X
            legato='[0.1|0.2|0.7|0.1]+0.6', # -> facteur de fun
            cut='1|0, 1|0, 1!4', orbit=2, room=0.5, size=0.2, dry=0.1,
            begin='[0:1,0.01], [1:0,0.01]').out(i) # -> begin r ou {0, 1, 0.1}
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    # S('f', shape=0.5).out(i, 4)
    # S('hhh', amp='{0, 0.2, 0.01}', legato='0.1~0.5').out(i) # -> hhh ramp
    # S('d:4, d:5, .', legato=0.5).out(i, 3)
    # S('d:{4,9}', legato=0.5).out(i, 4)
    # S('z', shape=0.8).out(i, 4)
    S('hhh:12', hcutoff=500, speed='[1:10]', shape=0.8).out(i, 1)
    # S('kit5:[6!4,7!2,5!5,4]', shape=0.8).out(i, 3)
    # S('q:rand*8', shape=0.4).out(i, P('1!12, 2!8', i))
    S('long:1', # -> lost into jupfx
            midinote='C',
            cutoff=4000, # ->
            pan='[0:0.5, 0.1], [0.5:1, 0.1]', # -> X
            legato='0.1|0.2|0.3|0.1',
            begin='[0:1,0.01], [1:0,0.01]').out(i) # -> begin r ou {0, 1, 0.1}
    a(baba, d=1/8, i=i+1)


@swim
def baba(d=0.5, i=0):
    # S('f', shape=0.5).out(i, 4)
    # S('hhh', amp='{0, 0.2, 0.01}', legato='0.1~0.5').out(i) # -> hhh ramp
    # S('d:4, d:5, .', legato=0.5).out(i, 3)
    # S('d:{4,9}', legato=0.5).out(i, 4)
    # S('z', shape=0.8).out(i, 4)
    S('hhh:12', hcutoff=500, speed='[1:10]', shape=0.8).out(i, 1)
    # S('kit5:[6!4,7!2,5!5,4]', shape=0.8).out(i, 3)
    # S('q:rand*8', shape=0.4).out(i, P('1!12, 2!8', i))
    S('long:1', # -> lost into jupfx
            midinote='C',
            cutoff=4000, # ->
            pan='[0:0.5, 0.1], [0.5: 1, 0.1]', # -> X
            legato='0.1|0.2|0.3|0.1',
            begin='[0:1,0.01], [1:0,0.01]').out(i) # -> begin r ou {0, 1, 0.1}
    a(baba, d=1/8, i=i+1)

panic()

S('lost').out()

S('lost:2').out()

# Fêter Halloween

S('lost:7', legato=7, speed=0.5, release=7).out()

S('lost:0', legato=7, speed=0.5, release=7).out()

S('lost:3', legato=7, speed=0.5, release=7).out()

panic()

# ██████████████████████████████████████████████████████████████████████████████
# █                                                                            █
# █     █ █   ▄▄   █░█ ▄▀█ █░█ ▄▀█ █░░ █ █▄░█ ▄▀█                              █
# █     █ █   ░░   █▀█ █▀█ ▀▄▀ █▀█ █▄▄ █ █░▀█ █▀█                              █
# █                                                                            █
# ██████████████████████████████████████████████████████████████████████████████


@swim
def baba(d=0.5, i=0):
    # S('bip:rand*20', shape=0.4, midinote='quant([0+12|24,3,6,10]+50, C@minor), quant([0,3,10]+50, F@minor)').out(i, 1, 0.25)
    # S('bip:rand*20+20', shape=0.4, midinote='quant([0+12|24,3,6,10]+62, C@minor), quant([0,3,10]+62|74, F@minor)').out(i, 3, 0.25)
    S('boop:rand*40').out()
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('bip:rand*20',
            orbit=2, room=0.7, size='r', dry='0.1',
            shape=0.4, midinote='quant([0+12|24,3,6,10]+50, C@minor), quant([0,3,10]+50, F@minor)').out(i, 1, 0.25)
    S('bip:rand*20+20',
            orbit=2, room=0.5, size='r', dry='0.1',
            shape=0.4, midinote='quant([0+12|24,3,6,10]+62, C@minor), quant([0,3,10]+62|74, F@minor)').out(i, 3, 0.25)
    S('boop:rand*40').out()
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('bip:rand*20',
            orbit=2, room=0.7, size='r', dry='0.1', legato=1,
            shape=0.4, midinote='quant([0+12|24,3,6,10]+50, C@minor), quant([0,3,10]+50, F@minor)').out(i, 1, 0.25)
    S('bip:rand*20, boop:rand*200',
            orbit=2, room=0.7, size='r', dry='0.1', legato=1,
            shape=0.4, midinote='quant([0+12|24,1~20,6,0~20]+80, C@minor), quant([0~20,3,10]+50, F@minor)').out(i, 3, 1)
    S('(ff):rand*20', # ulh electrowave ff
            orbit=2, room=0.7, size='r', dry='0.1', legato=0.2, hcutoff=500,
            shape=0.4, midinote='quant([0+12|24,1~20,6,0~20]+50, C@minor), quant([0~20,3,10]+50, F@minor)').out(i, 2, 1)
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('ff', shape=0.5).out(i, 4)
    S('ll', shape=0.5).out(i, 4)
    S('gameboysnare', cutoff=800).out(i, 8)
    S('., hhh:rand*40', hcutoff=9000).out(i, 1)
    S('., hhh:rand*40', hcutoff=9000, speed='1~50').out(i, 1)
    S('bip:rand*20',
            orbit=2, room=0.7, size='r', dry='0.1', legato=1,
            shape=0.4, midinote='quant([0+12|24,3,6,10]+50, C@minor), quant([0,3,10]+50, F@minor)').out(i, 1, 0.25)
    S('bip:rand*20, boop:rand*200',
            orbit=2, room=0.7, size='r', dry='0.1', legato=1,
            shape=0.4, midinote='quant([0+12|24,1~20,6,0~20]+80, C@minor), quant([0~20,3,10]+50, F@minor)').out(i, 3, 1)
    S('(ulh):rand*20', # ulh electrowave ff
            orbit=2, room=0.7, size='r', dry='0.1', legato=0.2, hcutoff=500,
            shape=0.4, midinote='quant([0+12|24,1~20,6,0~20]+50, C@minor), quant([0~20,3,10]+50, F@minor)').out(i, 2, 1)
    a(baba, d=1/8, i=i+1)

# <-> des allers retours

@swim
def baba(d=0.5, i=0):
    # S('ff, gg:rand*29', shape=0.8, leslie=1, leslierate=5, lesliespeed=2).out(i, 2)
    # S('ll', shape=0.8).out(i, 4)
    S('gameboysnare', cutoff=800).out(i, 8)
    # S('., hhh:rand*40', hcutoff=9000).out(i, 1)
    S('., hhh:rand*40', hcutoff=9000, speed='1~50').out(i, 1)
    # S('bip:rand*20', lesliespeed='2*8', leslierate='rand*5', leslie=1,
    #         orbit=2, room=0.7, size='r', dry='0.1', legato=1,
    #         shape=0.4, midinote='quant([0+12|24,3,6,10]+50, C@minor), quant([0,3,10]+50, F@minor)').out(i, 1, 0.25)
    S('bip:rand*20, boop:rand*200', lesliespeed='2*8', leslierate='rand*5', leslie=1,
            orbit=2, room=0.7, size='r', dry='0.1', legato=1,
            shape=0.4, midinote='quant([0+12|24,1~20,6,0~20]+80, C@minor), quant([0~20,3,10]+50, F@minor)').out(i, 3, 1)
    S('(ulh):rand*20', # ulh electrowave ff
            orbit=2, room=0.7, size='r', dry='0.1', legato=0.2, hcutoff=500,
            shape=0.4, midinote='quant([0+12|24,1~20,6,0~20]+50, C@minor), quant([0~20,3,10]+50, F@minor)').out(i, 2, 1)
    a(baba, d=1/8, i=i+1)

# --|--> transition du coq à l'âne

@swim
def baba(d=0.5, i=0):
    S('m, ..., m, ...', shape=0.5).out(i, 2)
    S('rev([s,a,l,u,t, z,o,r,b,a]:rand*8)',
            legato=0.1, pan='tan(r/100)', accelerate=0.2,
            room=0.1, dry=0.1, size=0.1,
    ).out(i, 2)
    S('perca:[1:20], ..',
            speed=2 if rarely() else 'rand*4',
    ).out(i, 2)
    a(baba, d=1/16, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('m, ..., m, ...', shape=0.5).out(i, 2)
    S('long:13', shape=0.5,
            begin='0.5, 0.5, 0.42, 0.5!2, 0.6', orbit=3,
            cut=1, legato=2).out(i, 8, 0.25)
    S('perca:[1:20], ..', speed=2).out(i, 2)
    a(baba, d=1/16, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('f, ..., f, ...').out(i, 2)
    S('gg, ...', shape=0.5, orbit=4, room=0.2, size=0.2, dry=0.2).out(i, 2)
    S('perca:[1: 20], ..', speed='1+rand*4', cutoff='200+rand*8000').out(i, 2)
    S('perca:[20: 1], .', speed='0.1+sin($)', cutoff='200+rand*8000').out(i, 3)
    S('long:13', shape=0.7,
            begin='0.1, 0.2, 0.3, 0.5',
            orbit=3,
            cut=1).out(i, 8, 0.25) # 0.5 0.6
    a(baba, d=1/16, i=i+1)


@swim
def baba(d=0.5, i=0):
    S('m, ..., m, ...', shape=0.5).out(i, 2)
    S('hhh:rand*49', amp=0.3, hcutoff='sin(i.i/40)*7000').out(i, 2)
    S('long:13', shape=0.5,
            begin='0.6, 0.5, 0.42, 0.6, 0.7', orbit=3,
            cut=1, legato=2).out(i, 8, 0.25)
    S('q:[1:20], ..', speed=2).out(i, 2)
    a(baba, d=1/16, i=i+1)


@swim
def baba(d=0.5, i=0):
    S('m, ..., m, ...', shape=0.5).out(i, 2)
    S('hhh:rand*49', amp=0.3, hcutoff='sin(i.i/40)*7000').out(i, 2)
    S('long:13', shape=0.5,
            begin='0.5, 0.5, 0.42, 0.5!2, 0.6', orbit=3,
            cut=1, legato=2).out(i, 8, 0.25)
    S('q:[1:20], ..', speed=2).out(i, 2)
    a(baba, d=1/16, i=i+1)

# une petite transition jsp

@swim
def baba(d=0.5, i=0):
    # S('m, ..., m, ...', shape=0.5).out(i, 2)
    # S('hhh:rand*49', amp=0.3, hcutoff='sin(i.i/40)*7000').out(i, 2)
    S('jupfx:rand*20', shape=0.5, hcutoff='200 + rand*8000',
            begin='0.5, 0.5, 0.42, 0.5!2, 0.6', orbit=3,
            cut=1, legato=2).out(i, 8, 0.25)
    S('q:[1:20], ..', speed=2).out(i, 2)
    a(baba, d=1/16, i=i+1)

# Débrouille toi


# ██████████████████████████████████████████████████████████████████████████████
# █                                                                            █
# █ █ █ █   ▄▄   ▀█▀ ▄▀█ █▀█ ▀█▀ █▀▀   █ █▄░█ ▀█▀ █▀█   ▀█▀ █▀▀ █▀█            █
# █ █ █ █   ░░   ░█░ █▀█ █▀▄ ░█░ ██▄   █ █░▀█ ░█░ █▄█   ░█░ ██▄ █▀▄            █
# █                                                                            █
# █ █▀ ▄▀█ █ █▄░█ ▀█▀ ▄▄ █▀▀ ▀█▀ █ █▀▀ █▄░█ █▄░█ █▀▀                           █
# █ ▄█ █▀█ █ █░▀█ ░█░ ░░ ██▄ ░█░ █ ██▄ █░▀█ █░▀█ ██▄                           █
# █                                                                            █
# ██████████████████████████████████████████████████████████████████████████████

,*,,,,,,,,,,,,.,,,,..*****,,.  .. ,*,.   . ..        ........,,,.,,,,,,,,,,.,,.*
*(**/**,/*(**,**///**,,*////*,,..,,//.. ..,       . ....,,,,,,,,**********(//(((
*/***/***,/******/,. . ....,,,,..,,**.   ...     ..,.....,,.,,,,,*********(((//*
*((*//**,,/,,,,,*,.  .. ....,,,.../#%%%%#(,..    .,,,....,...,,,,.,,,,**,,****(/
*****/,,*,**,**,,,...,.,.,*/#%%%%%%%%%%%%%%%#(. .,,..,,...,...,..,..,,,,****/***
*//,**//*****/**,.....%#%&&%%&&&&%&%%%%%%%%%%%%##%#...... ,,..,..*.,,,,/**/*,,**
*//*,,*,,******,,/,,.#%&&&&&&&&&&&&&%#%&%%&%%%%###%( .. ..,,..,,,..,,..,.****,**
*//*,,,,****,,,,,,,,#%&&&&&&&%&%&%%%%&&&%&&&%%%%%###(#*  ....,,,,.,........,,**,
*//*****,***...... #%&%&&&%&%%&%%%%#%%%&&&&&%%%%%%%%%%%#**,*,....,,.,*.......,,,
*/*******,,,......#%%&%&%&&&%%%&&%%%%%#%%%%%%%%%###%%#%%(,,,,*, ....   ,..,,,,./
*/*****,,*,.....,(&&&%&&&%(***(&**,****,,*((##%/#/#%%%#%%(////**,,......,,,,,.*,
*/*,,,,,,.,*, ..#%%&&&&%#/***************,**,... .*#%%%%%#//*.,..........,*/*,.,
*/****,,,...,.,.#%&&&&%(/********,,,****,***,...   ,/%%#(*.............,.,,,..,*
*/**,,,,,,,,....,%%%&&&/**/////***,**/***,,*,*,...  ./(#,...,..,.,,..,,,,...,,,*
*/****,**,**,*,..*%&&&/**#(///(//((/*/*,**/////***,..#%(, .....,.....,,. ....,*,
*//**********,,,,//%%%**//(%#&%#////(,,#/*(*###*/*.../#(/,.,.,,.. ... .   .,,..,
*//*///**,,,,***,,//%%***/((((((//((,,,,((/(((//.*...,#/,...,,.,...,.. .,......,
*///(**//*****/***,(%#****///**/****,,,,.,**,,,,,.,,,(#*..,,...,.. ............,
*//*/*,,**,,,,**/***#%(**********/****,....,,,,,.....#(*,,......,.  .,,.,**,,,..
*//*/*,*/**,*,,,,,,.,##//**********,**,,..,,,,....  ,((******//(*.....*,,.,....*
*//*///**//,,.**,..,,,%#***********((/./(,*,,,,. ..,*((,,,....,,..,.,,,*,.,...,*
/#/((***/,***,,,.,,,**(((***,*,****((#/*/,,,...   .,(#,,.......  ..,,,***,,,.,.*
*((/(/***.*,,,..,.,*,//(#(//****//(((((/(///.*...,.//(/***,.,*..  ....,***,...,*
*((//*,,,,,.......,,..,*(##(//***//((//(*(*,*,...,*/*,... ..    .  ......,..,.,,
/((((/,,,,...........,,**/(#((/**/***/*,,,***,.,.////*******,,.,,.   .... ...,.,
*(((/*,,,,,,,./, .......*,,/###(/********,,.,*(*,.,,.....,,,..     ..  ......,..
*((//**,,.,,****,.,,,...*%(..(###%#((((((//(#(/.   ,.*,,,,..,..   ..... ......,.
*((///*,.,*,****...,*/.&&&%,.,,*(##%%%%%%%##(/.   .%#((,.,.., ...........,,,,,,.
/(/(**,,,..,,,,,**/**/&&@&&&/*,/.,*((((((((. ...,(%#%%%%%,,,,.......   ...,.,,,,
*(//**,***,**,*****(%&&&@&&@&%*,.,,*//(((/,..,/%%%%%%%%%%##*,*,...............,.
*(//***,,*/,*,,(&&&&@&@@@&&&&(,,,,,,,*(#,,,,,,*#%%%%%%%%%%%%%#**.........,/*****
*(///****,,(&&&&@@@@@@&&@&&&&##%&&&&&&&&&&&&%##%%&&&%%&%%%%%%%#(%(/*....***,*,,,
*((((((&@&&&&@@@@&&@&@&&&&&%%&&&&&@&&&&&@@@&&%%%%%%%%%%%%%#%%#%%*,,...,,,*,,***,
/%&%&@&%&@@@@@&&&&&%%&&@&&&@&&@@&&&#,,,,,##&%(%%&%%%%#%%##%/.  /#/...,,..,,,,...
/&&&%&&&&&%&&@&&&&&&&&&&&&&&%#%&&&&%(.,,,,,,/&&&&%%%%%##**,. ,,/,.,.,.*,*,(#&(..
/&&%#%%%###%&@&&&&&%%%%%%%&&&&&%&%&%*,.,,...%%%&%%%(%#*,,.,,./,,.,,,./(#(*#(%(#(
/&&@&@&%&@@@&@&&&%(#%%%#%&&&&&&&%%&&%#.... %%%%&&%#(*,,...(/,,,*,(%%###(####/*%(
/&@@@&@&&#%##&%(/*/(#%%%#%&@&&%#%%&&%&%,./&&&%%%#***....**,*/*%%%%&%(#%#####(/(*
/#%&@%%##&&&%(/((,,(%&%#%%%&&%%#%#%%&%&%&&&&%%(*.....(.*.,/#%%%&%%%%###%#%%###(.
/######/(%%&%(%%#(((/#%&@&&&&&%&&%%&&%&&&&&%/,,.. ,.,.,(#%&%&%%%&%%%#%%%(((//%%(
/%%%#(#%%%%%%%%#######(((%&&@&&%%%%%&&%%%(,,,,..,,,(%%&&%#%%%####((%#%(/(#%#(#**
/%%%%%%%&&&%&&%%%%#(((((((#*%&@&%%&&%%%/,*,,.*,//&%%&%%%%&&%####(/*#%(/(#%%#**,*
/&&%&%%%%%%%##%%###(#((#*#%((//(////***/*.**##%%%#%##%&%#(##%%%%#*/#//*/#(/#(***
# C'EST PIERRE BONNARD, IL FAUT ALLER LE VOIR.


@swim
def baba(d=0.5, i=0):
    M(velocity='90~110', note='inrot(C@maj7, F@maj7)-12').out(i, 2)
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    M(velocity='90~110', dur=1, note='inrot(C@maj7, F@maj7)-12').out(i, 2)
    M(velocity='90~110|70', dur='15~20', note="F', ..., G'', ..., [D, E, F, A]+12").out(i, 2)
    a(baba, d=1/8, i=i+1)


@swim
def baba(d=0.5, i=0):
    M(velocity='90~110', dur=1, note='inrot(C@maj7, F@maj7)-12').out(i, 2)
    M(velocity='90~110|90', dur='15~20', note="F., ..., F.., ...").out(i, 2)
    M(velocity='90~110|90', dur='15~20', note="F., A, .., F.., ...").out(i, 2)
    a(baba, d=1/8, i=i+1)

# <-> alterner

@swim
def baba(d=0.5, i=0):
    M(dur='2~5', note='inrot(C@maj7, F@maj7)-12').out(i, 2)
    M(dur='2~5', note='disco(inrot(C@maj7, F@maj7))').out(i, 5)
    M(dur='2~12', note='adisco(inrot(inrot(C@maj7, F@maj7), G@fifths))').out(i, 4)
    a(baba, d=1/8, i=i+1)

@swim
def baba(d=0.5, i=0):
    M(note='inrot(C@maj7, F@maj7)-12').out(i, 2)
    if rarely():
        M(note='disco(inrot(C@maj7, F@maj7))').out(i, 5)
    if sometimes():
        M(note='adisco(inrot(inrot(C@maj7, F@maj7), G@fifths))').out(i, 4)
    a(baba, d=1/8, i=i+1)


c._midi_nudge = 0.30

@swim
def baba(d=0.5, i=0):
    S('ff').out(i, 4)
    M(velocity='90~110', dur=1, note='inrot(C@maj7, F@maj7)-12').out(i, 2)
    M(velocity='90~110|90', dur='15~20', note="F., ..., F.., ...").out(i, 2)
    M(velocity='90~110|90', dur='15~20', note="F., A, .., F.., ...").out(i, 2)
    a(baba, d=1/8, i=i+1)



# ██████████████████████████████████████████████████████████████████████████████
# █                                                                            █
# █  █ █░█   ▄▄   █░░ █▀▀   █▀█ █ ▄▀█ █▄░█ █▀█   ▄▀█ █▄░█ ▄▀█ █░░ █▀█          █
# █  █ ▀▄▀   ░░   █▄▄ ██▄   █▀▀ █ █▀█ █░▀█ █▄█   █▀█ █░▀█ █▀█ █▄▄ █▄█          █
# █                                                                            █
# ██████████████████████████████████████████████████████████████████████████████

panic()


@swim
def baba(d=0.5, i=0):
    S('kit3:[1,2,1,2,4,5,4,6]', legato=1).out(i, 8)
    S('long:42', begin='r', cut=1).out(i, 8)
    a(baba, d=1/32, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('jupbass:28|44, jupbass:28', octave=4,
        legato=1, cut=1, orbit=3).out(i, 24, 1)
    if sometimes():
        S('z:6' if random() > 0.5 else 'z:7', shape=0.9, hcutoff=7000).out(i, 4)
    a(baba, d=1/32, i=i+1)


@swim
def baba(d=0.5, i=0):
    S('kit3:[1,2~10,1,2,4~10,5,4,6]', legato=1).out(i, 8)
    S('long:42', begin='r', cut=1).out(i, 8)
    a(baba, d=1/32, i=i+1)

@swim
def baba(d=0.5, i=0):
    # Ce truc est quand même giga fade :'(((((((((((((
    S('jupbass:28|44, jupbass:28', octave=4,
        legato=1, cut=1, orbit=3).out(i, 24, 1)
    if sometimes():
        S('z:6' if random() > 0.5 else 'z:7', shape=0.9, hcutoff=7000).out(i, 4)
    # Du du du du dudududududu dudu du du dud udu dudu
    a(baba, d=1/32, i=i+1)

# Réponse :

@swim
def baba(d=0.5, i=0):
    S('kit3:[0, 1,2,1,2,4,5,4,6,7,8, 1, 0]', legato=1).out(i, 8)
    S('long:42', begin='r', cut=1).out(i, 8)
    S('long:42~46', begin='r', cut=1, speed=0.5).out(i, 8)
    S('jupbass:28|44, jupbass:28', octave=4,
        legato=1, cut=1, orbit=3).out(i, 24, 1)
    if sometimes():
        S('z:6' if random() > 0.1 else 'z:7',
                pan='r',
                legato=1, shape=0.9, hcutoff=7000).out(i, 4)
    if sometimes():
        S('dd:6|7|8' if random() > 0.5 else 'j:0~7',
                pan='r',
                legato=1, shape=0.9, hcutoff=7000).out(i, 4)
    a(baba, d=1/32, i=i+1)


@swim
def baba(d=0.5, i=0):
    S('kit3:[1,2,1,2,4,5,4,6,1,2,3,1,2,3,2,3,4,5~8!5]', legato=1).out(i, 8)
    S('long:20~33', begin='r', cut=1).out(i, 8)
    S('long:42~46', begin='r', cut=1, speed=0.5).out(i, 8)
    S('jupbass:28|44, jupbass:28', octave=4,
        legato=1, cut=1, orbit=3).out(i, 24, 1)
    if sometimes():
        S('z:6' if random() > 0.1 else 'z:8~400',
                pan='r',
                legato=1, shape=0.9, hcutoff=7000).out(i, 4)
    if sometimes():
        S('dd:6|7|8' if random() > 0.5 else 'z:7~200',
                pan='r',
                legato=1, shape=0.9, hcutoff=7000).out(i, 4)
    a(baba, d=1/32, i=i+1)


@swim
def baba(d=0.5, i=0):
    S('kit3:[1,2,1,2,4,5,4,6,1,2,3,1,2,3,2,3,4,5~8!5]', legato=1).out(i, 8)
    # S('long:42', begin='{0,2,0.4}', cut=1).out(i, 16)
    S('long:42', begin='[0:1, 0.08]', cut=1).out(i, 16) # -> éplucher comme un oignon (solo de fichier .wav)
    # S('long:42~46', begin='r', cut=1, speed=0.5).out(i, 8)
    # S('jupbass:28|44, jupbass:28', octave=4,
    #     legato=1, cut=1, orbit=3).out(i, 24, 1)
    if sometimes():
        S('z:6' if random() > 0.1 else 'z:8~400',
                pan='r',
                legato=1, shape=0.9, hcutoff=7000).out(i, 4)
    if sometimes():
        S('dd:6|7|8' if random() > 0.5 else 'z:7~200',
                pan='r',
                legato=1, shape=0.9, hcutoff=7000).out(i, 4)
    a(baba, d=1/32, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('kit3:[1,2,1,2,4,5,4,6,1,2,3,1,2,3,2,3,4,5~8!5]', legato=1).out(i, 8)
    S('long:10~33', begin='r', cut=1, speed="1~8").out(i, 8)
    S('long:20~46', begin='r', cut=1, speed="1~8").out(i, 8)
    a(baba, d=1/32, i=i+1)

# Réponse :

@swim
def baba(d=0.5, i=0):
    S('kit2:[0, 1,2, 0, 1,2,4,5,4,0,6,1,2,3,1,2,3,2,3,4,5~8!5]', legato=1).out(i, 8)
    S('kit3:[1,2,1,2,4,5,4,6,1,2,3,1,2,3,2,3,4,5~8!5]', legato=1).out(i, 8)
    S('long:103', begin='0.1, 0.5', cut=1, speed="1~8").out(i, 16)
    S('long:20', begin='0.1, 0.5', cut=1, speed="1~8").out(i, 8)
    a(baba, d=1/32, i=i+1)


@swim
def baba(d=0.5, i=0):
    S('cc').out(i, 12)
    S('kit2:[0, 1,2, 0, 1,2,4,5,4,0,6,1,2,3,1,2,3,2,3,4,5~8!5]', legato=1).out(i, 8)
    S('kit3:[1,2,1,2,4,5,4,6,1,2,3,1,2,3,2,3,4,5~8!5]', legato=1).out(i, 8)
    S('long:103', begin='0.1, 0.5', cut=1, speed="1~8").out(i, 16)
    S('long:20', begin='0.1, 0.5', cut=1, speed="1~8").out(i, 8)
    a(baba, d=1/32, i=i+1)

@swim
def baba(d=0.5, i=0):
    S('jupbass:28|44, jupbass:28', octave=4,
        legato=1, cut=1, orbit=3).out(i, 24, 1)
    S('kit4:rand*20', legato=0.4, begin=0.01).out(i, 12)
    S('kit3:[1,2,1,2,4,5,4,6]').out(i, 8)
    S('long:40', begin='0.60!4, 0.555!2, 0.27!4, 0.25!2', orbit=2, cut=1).out(i, 32)
    S('long:40', speed=1.01, begin='0.60!4, 0.555!2, 0.27!4, 0.25!2', orbit=2, cut=1).out(i, 32)
    if sometimes():
        S('z:6', shape=0.9, hcutoff=5000).out(i, 4)
    a(baba, d=1/32, i=i+1)

panic()

@swim
def baba(d=0.5, i=0):
    S('jupbass:28|44, jupbass:28', octave=4,
        legato=1, cut=1, orbit=3).out(i, 24, 1)
    S('kit4:rand*20', legato=0.4, begin=0.01).out(i, 12)
    S('kit3:[1,2,1,2,4,5,4,6]').out(i, 8)
    S('long:26', amp=0.5, begin='0.60!4, 0.555!2, 0.27!4, 0.25!2', orbit=2, cut=1).out(i, 32)
    S('long:26', speed=1.01, begin='0.60!4, 0.555!2, 0.27!4, 0.25!2', orbit=2, cut=1).out(i, 32)
    if sometimes():
        S('z:6', shape=0.9).out(i, 4)
    a(baba, d=1/32, i=i+1)

# Variation 3
@swim
def baba(d=0.5, i=0):
    S('jupbass:28|44, jupbass:28', octave=4,
        legato=1, cut=1, orbit=3).out(i, 24, 1)
    S('kit4:rand*20', legato=0.4, begin=0.01).out(i, 12)
    S('kit3:[1,2,1,2,4,5,4,6]').out(i, 8)
    S('long:40', begin='0.60!4, 0.555!2, 0.27!4, 0.25!2', orbit=2, cut=1).out(i, 32)
    S('long:40', speed=1.01, begin='0.60!4, 0.555!2, 0.27!4, 0.25!2', orbit=2, cut=1).out(i, 32)
    if sometimes():
        S('z:6', shape=0.9).out(i, 4)
    a(baba, d=1/32, i=i+1)

panic()
```