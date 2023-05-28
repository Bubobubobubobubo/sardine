let about_tutorial = `# 0.0: About this code editor

# Shift + Enter -> evaluate a line
# Ctrl + Enter -> evaluate a block
# 0-9 -> code editors (w. auto-save)
# D -> embedded documentation
# C -> configuration pane
# Look at the buttons up there!

Pa * d('bd hh sn hh') # Line: Shift + Enter

@swim
def test():
    print('Ctrl+Enter to evaluate the block')
    again(test)

# The logs below only show printed elements
# They are throttled: they will appear after
# a few milliseconds, not immediately!

clock.tempo # look at your terminal

print(clock.tempo) # now printed in the logs!


# Ctrl+Space -> switch to VIM mode (expert)
# You can turn it off by switching to another
# pane and coming back.

# Folder icon -> Open Sardine Folder
# Save icon -> Save current text buffer
# Help Button -> Help about keybindings

# There are other code editors for Sardine!
# Check the documentation website.
` 

let time_tutorial = `# 1.0: Time, Period and Clocks

# The clock variable is a reference to the clock:

clock.tempo # Get tempo
clock.tempo = 130 # Set tempo
clock.cps = 0.5 # Set tempo in cycles per second (see Vortex)

# You can get more useful information from the clock:

print(clock.bar) # Current bar
print(clock.beat) # Current beat (float)
print(clock.phase) # Current phase (0.0 -> 1.0)
print(clock.beat_duration) # Duration of a beat in seconds

# You can control the transport:

clock.pause() # Pause the clock
clock.resume() # Continue playback

# And you can start/stop it:

clock.stop() # Stop the clock
clock.start() # Start the clock

# Time in Sardine is mesured in "periods" or "p":

@swim # Ctrl+Enter to evaluate the block
def counting_time(p=1, i=0):
  print(f"Time : {clock.beat}")
  again(counting_time, p=1, i=i+1)

Pa * d('bd') # By default, a player will repeat every period (p=1)

Pa * d('bd', p='0.5 0.25') # But you can change the period and even pattern it!

Pa * d('bd', period=2) # You can even write 'period' in full if you prefer!

# You can also do the same thing in a swimming function:

@swim # Ctrl+Enter to evaluate the block
def counting_time(p=1, i=0):
  print(f"Time : {clock.beat}")
  again(counting_time, p=P('0.5 0.25', i), i=i+1)
`

let sound_tutorial = `# Playing your first sounds

# By default, Sardine can make use of SuperDirt to play sound/synths:
# (SuperDirt is a sequencer/scheduler running inside SuperCollider)

D('bd') # Play a bass drum

D('cp') # Play a clap sound

# Any sound can receive an arbitrary number of arguments
# to refine how the playback is done:

D('cp', speed=0.5, room=0.5) # Half speed roomy clap sound

# Here is a short list of default audio samples, try some of them: 
# (More sounds are available, check the documentation)

# (Numbers show how many samples in each bank.)
# ades4 (6) alex (2) alphabet (26) amencutup (32) armora (7) arp (2) arpy (11)
# auto (11) baa (7) baa2 (7) bass (4) bass0 (3) bass1 (30) bass2 (5) bass3 (11)
# birds3 (19) bleep (13) blip (2) blue (2) bottle (13) breaks125 (2) breaks152 (1)
# chin (4) circus (3) clak (2) click (4) clubkick (5) co (4) coins (1) control (2)
# dist (16) dork2 (4) dorkbot (2) dr (42) dr2 (6) dr55 (4) dr_few (8) drum (6)
# feelfx (8) fest (1) fire (1) flick (17) fm (17) foo (27) future (17) gab (10)
# gretsch (24) gtr (3) h (7) hand (17) hardcore (12) hardkick (6) haw (6) hc (6)
# ifdrums (3) incoming (8) industrial (32) insect (3) invaders (18) jazz (8)
# latibro (8) led (1) less (4) lighter (33) linnhats (6) lt (16) made (7) made2 (1) 
# mp3 (4) msg (9) mt (16) mute (28) newnotes (15) noise (1) noise2 (8) notes (15)
# perc (6) peri (15) pluck (17) popkick (10) print (11) proc (2) procshort (8)
# rm (2) rs (1) sax (22) sd (2) seawolf (3) sequential (8) sf (18) sheffield (1)
# speech (7) speechless (10) speedupdown (9) stab (23) stomp (10) subroc3d (11)
# techno (7) tink (5) tok (4) toys (13) trump (11) ul (10) ulgab (5) uxay (3)

D('voodoo', release=0.5, speed='2|3', binshift=0.5)

# Let's use some of these sounds and make a pattern:

Pa * d('drum procshot drum perc', p=0.5, release=0.5)

# You can change your pattern anytime and reevaluate:

Pa * d('drum popkick drum:4 perc', p='0.5 0.25', 
       release=0.5) # Press Ctrl+Enter

You can also make use of the default synthesizers:

Pa * d('supersaw', n="C4 E4 G4", lpf=2000, p=0.5)
`

let midi_tutorial = `# About MIDI
`

let syntax_tutorial = `# About Tutorial 4
`

let pattern_tutorial = `# About Tutorial 5
`

export const tutorialText = {
  "0.0 About": about_tutorial,
  "1.0 Time": time_tutorial,
  "1.1 Play Sound": sound_tutorial,
  "1.2 Play MIDI": midi_tutorial,
  "1.3 Syntax": syntax_tutorial,
  "1.4 Patterns": pattern_tutorial,
}
