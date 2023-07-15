let about_tutorial = `# 0.0: About this code editor

# Shift + Enter -> evaluate a line
# Ctrl + Enter -> evaluate a block
# 0-9 -> code editors (w. auto-save)
# D -> embedded documentation
# C -> configuration pane
# Look at the buttons up there!

Pa * d('bd hh sn hh') # Line: Shift + Enter

@swim
def test():
    print('Ctrl+Enter to evaluate the block')
    again(test)

# The logs below only show printed elements
# They are throttled: they will appear after
# a few milliseconds, not immediately!

clock.tempo # look at your terminal

print(clock.tempo) # now printed in the logs!


# Ctrl+Space -> switch to VIM mode (expert)
# You can turn it off by switching to another
# pane and coming back.

# Folder icon -> Open Sardine Folder
# Save icon -> Save current text buffer
# Help Button -> Help about keybindings

# There are other code editors for Sardine!
# Check the documentation website.
` 

let time_tutorial = `# 1.0: Time, Period and Clocks

# The clock variable is a reference to the clock:

clock.tempo # Get tempo
clock.tempo = 130 # Set tempo
clock.cps = 0.5 # Set tempo in cycles per second (see Vortex)

# You can get more useful information from the clock:

print(clock.bar) # Current bar
print(clock.beat) # Current beat (float)
print(clock.phase) # Current phase (0.0 -> 1.0)
print(clock.beat_duration) # Duration of a beat in seconds

# You can control the transport:

clock.pause() # Pause the clock
clock.resume() # Continue playback

# And you can start/stop it:

clock.stop() # Stop the clock
clock.start() # Start the clock

# Time in Sardine is mesured in "periods" or "p":

@swim # Ctrl+Enter to evaluate the block
def counting_time(p=1, i=0):
  print(f"Time : {clock.beat}")
  again(counting_time, p=1, i=i+1)

Pa * d('bd') # By default, a player will repeat every period (p=1)

Pa * d('bd', p='0.5 0.25') # But you can change the period and even pattern it!

Pa * d('bd', period=2) # You can even write 'period' in full if you prefer!

# You can also do the same thing in a swimming function:

@swim # Ctrl+Enter to evaluate the block
def counting_time(p=1, i=0):
  print(f"Time : {clock.beat}")
  again(counting_time, p=P('0.5 0.25', i), i=i+1)
`

let sound_tutorial = `# Playing your first sounds

# By default, Sardine can make use of SuperDirt to play sound/synths:
# (SuperDirt is a sequencer/scheduler running inside SuperCollider)

D('bd') # Play a bass drum

D('cp') # Play a clap sound

# Any sound can receive an arbitrary number of arguments
# to refine how the playback is done:

D('cp', speed=0.5, room=0.5) # Half speed roomy clap sound

# Here is a short list of default audio samples, try some of them: 
# (More sounds are available, check the documentation)

# (Numbers show how many samples in each bank.)
# ades4 (6) alex (2) alphabet (26) amencutup (32) armora (7) arp (2) arpy (11)
# auto (11) baa (7) baa2 (7) bass (4) bass0 (3) bass1 (30) bass2 (5) bass3 (11)
# birds3 (19) bleep (13) blip (2) blue (2) bottle (13) breaks125 (2) breaks152 (1)
# chin (4) circus (3) clak (2) click (4) clubkick (5) co (4) coins (1) control (2)
# dist (16) dork2 (4) dorkbot (2) dr (42) dr2 (6) dr55 (4) dr_few (8) drum (6)
# feelfx (8) fest (1) fire (1) flick (17) fm (17) foo (27) future (17) gab (10)
# gretsch (24) gtr (3) h (7) hand (17) hardcore (12) hardkick (6) haw (6) hc (6)
# ifdrums (3) incoming (8) industrial (32) insect (3) invaders (18) jazz (8)
# latibro (8) led (1) less (4) lighter (33) linnhats (6) lt (16) made (7) made2 (1) 
# mp3 (4) msg (9) mt (16) mute (28) newnotes (15) noise (1) noise2 (8) notes (15)
# perc (6) peri (15) pluck (17) popkick (10) print (11) proc (2) procshort (8)
# rm (2) rs (1) sax (22) sd (2) seawolf (3) sequential (8) sf (18) sheffield (1)
# speech (7) speechless (10) speedupdown (9) stab (23) stomp (10) subroc3d (11)
# techno (7) tink (5) tok (4) toys (13) trump (11) ul (10) ulgab (5) uxay (3)

D('voodoo', release=0.5, speed='2|3', binshift=0.5)

# Let's use some of these sounds and make a pattern:

Pa * d('drum procshot drum perc', p=0.5, release=0.5)

# You can change your pattern anytime and reevaluate:

Pa * d('drum popkick drum:4 perc', p='0.5 0.25', 
      release=0.5) # Press Ctrl+Enter

# You can also make use of the default synthesizers:

Pa * d('supersaw', n="C4 E4 G4", lpf=2000, p=0.5)
`

let exploring_sound_tutorial = `# Exploring sounds

# The SuperDirt audio engine is full of surprises.
# There is a large number of parameters to play
# with. Let's browse through the essential ones.

# The first parameter, implicit, always refer to 
# the sample name or synthesizer name:
#################################################

Pa * d('drum', p=0.5)

# Sample names are 'folder' names and you can pick
# another sample in the same folder
Pa * d('drum:4', p=0.5)

Pa * d('drum:8 drum:4 drum:3', p=0.5)

Pa * d('drum:[0:10]', p=0.5)

# Some parameters are used to control the volume:
#################################################

Pa * d('bd', gain=1) # Sound volume (exponential scaling)
Pa * d('bd', amp=1) # Sound volume (linear scaling)

# In the same category, distortion and saturation:
Pa * d('bd', shape=0.5) # Smooth saturation (0 to 1)
Pa * d('bd', triode='rand') # More agressive distortion (0 to x)
Pa * d('bd', distort='rand') # Distortion!
Pa * d('bd', squiz=2) # aggressive distortion (multiples of 2)
Pa * d('bd', crush=2) # Sound destruction


# Some parameters are used to control playback:
#################################################

# Playback control:
Pa * d('bev', attack=0.2, release=2) # release after 2 secs 
                                     # control over the attack

Pa * d('bev', cut=1) # cut the sound when re-triggered

Pa * d('bev', begin=0.5, release=2) # beginning of sound file (0.0 to 1.0)

Pa * d('bev', end=0.5, release=2)   # end of sound file (0.0 to 1.0)

Pa * d('bev', speed=4, release=2)   # audio playback speed (0.0 to x)

Pa * d('bev', legato=1)  # similar but more aggressive than release 

# Of course, you can also play pitched samples. 
# There are multiple methods to do so:
#################################################

Pa * d('jvbass', p=0.25, freq='200 400 800', release=1) # Choose a frequency in hertz

Pa * d('jvbass', p=0.25, midinote='60 64 65', release=1) # MIDINote for a MIDI Note Number

Pa * d('jvbass', p=0.25, n='60 64 65', release=1) # n for note is shorter

# note and octave for melodies with 0 referring to 
# the tonic and handling octaves using the octave parameter.  
Pa * d('jvbass', p=0.25, note='0 4 5', octave=4, release=1) 


Pa * d('jvbass', p=0.25, accel='1 2 4') # Weird ascending pitchshifting effect 
                                        # Long parameter name: accelerate


# You can modify the panoramic (pan) of samples: 
#################################################

Pa * d('jvbass', p=0.25, pan='0 0.5 1')
`

let exploring_effects_tutorial = `# About audio effects

# The trip continues, now exploring different effects.
# There are a lot of different basic effects you can play 
# with and you can also declare your own using SuperCollider.

# SuperDirt comes with basic audio filters:
#################################################

# Low-pass filter with resonance 
Pa * d('hh', p=0.125, lpf='2000 4000 6000', lpq=0.5) 
Pa * d('hh', p=0.125,
       cutoff='2000 4000 6000',
       resonance=0.5) 

# High-pass filter with resonance 
Pa * d('hh', p=0.125, hpf='2000 4000 6000', hpq=0.5) 
Pa * d('hh', p=0.125,
       hcutoff='2000 4000 6000',
       hresonance=0.5) 

# Band-pass filter with resonance
Pa * d('hh', p=0.125, bpf='2000 4000 6000', bpq=0.5) 
Pa * d('hh', p=0.125,
       bandf='2000 4000 6000',
       bandq=0.5) 

# And also a performance oriented DJ filter:
#################################################

# LFO over the whole DJ filter range 
Pa * d('bd sn hh sn', djf='(alsin 2)')


# There is a simple but efficient reverberation:
#################################################

Pa * d('clap',
      room=0.5, # Size of the room   (0 -> x)
      dry=0.4,  # Size of the reverb (0 -> 1)
      size=0.9  # Dry / Wet balance  (0 -> 1)
)

# There is also a weird delay effect module:
#################################################

Pa * d('hh',
  speed='1|2|4',
  delay=1/2, # Injection amount of delayed signal (0 -> 1)
  delaytime=1/(2/3), # Delay time
  delayfeedback='0.5+(rand/4)', # Feedback (0 -> .99)
  amp=1
)


# The other creative effects are included:
#################################################

# A phaser
Pa * d(
    'jvbass',
    midinote='C|Eb|G|Bb',
    phaserrate='1~10', # Phaser speed      (0 -> 1)
    phaserdepth='(sin $*2)', amp=1 # Depth (0 -> 1)
)

# A Leslie cabinet
Pa * d('jvbass', amp=1,
       leslie=0.9, # Dry / Wet amount (0 -> 1)
       lrate=0.1,  # Rotation speed   (0 -> 1)
       lsize='0.1+rand*2' # Size      (0 -> x)
)

# A tremolo effect
Pa * d('amencutup:[1:20]',
        p=0.5,
        tremolorate='16|32',
        tremolodepth='[0.0~1.0 0.25]',
)

# There are other effects and technique to explore.
# Be sure to read the "Audio Engine" section of the
# documentation.
`


let midi_tutorial = `# About MIDI

# Sardine will always boot with a MIDI connexion. This is 
# the bare minimum you need to make sound with Sardine even
# if you don't want to rely on SuperCollider or anything else
# to generate sound.

# You will need to connect a synthesizer (virtual or hardware) 
# to continue further. Once done setting up, continue reading.

# Let's check the status of the default MIDI port:
##################################################

print(midi) # Print the MIDI port currently in use
midi.nudge = 0.5 # Nudge the MIDI output (for synchronisation)
print(midi.nudge) # Check the current MIDI Nudge

# Playing MIDI notes: 
##################################################

N(60) # Playing a C Note at fourth octave
N('C4') # This is exactly the same thing
N('C4', vel='50~120') # Changing velocity
N('C4', vel=50, chan=2) # Now on channel 2

# Note that all the notes currently have the
# same duration. To change duration, use 'dur'
N('C4', dur=0.1, vel='50~120')

# Just like before, you can make patterns of 
# MIDI notes, using the n() player
Pa * n('C Eb G Bb', dur=0.25, vel=110, chan=0)

# Everything can be patterned
Pa * n('C|G3 Eb G Bb', 
       dur='0.25 0.5!2 0.125|0.25',
       vel='[0:100,10]',
       chan=0)

# Playing MIDI Control Changes: 
##################################################

# Sending a simple control change
CC(chan=0, control=50, value=20)

# Transforming this into a pattern
Pa * cc(chan=0,
        control=50,
        value='20 40 50 80'
)

# Playing MIDI Program Changes: 
##################################################

# Sending a simple program change
PC(chan=0, program='1~80')

# Pattern version
Pa * pc(chan=0, program='1~80')

# This is just covering the basics of MIDI usage.
# There is much to learn about MIDI by reading the
# full documentation such as how to create your own
# custom controllers and/or MIDI instruments.
`

let spl_tutorial = `# The Sardine Pattern Language

# Sardine comes with an internal programming language
# that you will often see referred as SPL, an acronym
# that stands for "Sardine Pattern Language". We will
# explore it using a very simple pattern.

# This pattern is already using SPL (the string in green)
Pa * d('drum sn drum hh', p=0.5)

# Adding silence using the . operator
Pa * d('. sn drum hh', p=0.5) # silence on beat 1
Pa * d('... sn drum hh', p=0.5) # three silences
Pa * d('....... sn drum hh', p=0.5) # too much silence

# Repeating an element n times using !
Pa * d('drum!3 sn drum hh', p=0.5)

# Selecting a different sample using :
Pa * d('drum sn:1 drum:4 hh', p=0.5)

# Selecting a different sample using :
Pa * d('drum sn:1 drum:4 hh', p=0.5)

# Random choice between n elements
Pa * d('drum|sn|drum|hh', p=0.5)

# Random choice between n elements
Pa * d('drum|sn|drum|hh', p=0.5)

# You can make lists of elements using brackets:
###################################################

# No difference, so what is the point?
Pa * d('[drum sn drum hh]', p=0.5)

# Repeating each element n times
Pa * d('[drum sn drum hh]!!4', p=0.5)

# Repeating the list n times
Pa * d('[drum sn drum]!2 hh', p=0.5)

# Get the element at index n in list
Pa * d('[drum sn drum hh]&[3]', p=0.5)

# You can also generate lists of numbers using SPL:
###################################################

# Get the element at index n in list
Pa * d('[drum sn drum hh]&[3]', p=0.5)
`

export const generalTutorials = {
  "help-tutorial": about_tutorial,
  "help-time": time_tutorial,
  "help-sound": sound_tutorial,
  "help-samples": exploring_sound_tutorial,
  "help-effects": exploring_effects_tutorial,
  "help-midi": midi_tutorial,
  "help-patterns": spl_tutorial,
}