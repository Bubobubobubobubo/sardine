let time_tutorial = `
# 1.0: Time, Period and Clocks

# The clock variable is a reference to the clock

clock.tempo # Get tempo
clock.tempo = 130 # Set tempo
clock.cps = 0.5 # Set tempo in cycles per second (see Vortex)

# You can get more information from the clock

clock.bar # Current bar
clock.beat # Current beat (float)
clock.phase # Current phase (0.0 -> 1.0)
clock.beat_duration # Duration of a beat in seconds

# You can control the transport

clock.pause() # Pause the clock
clock.resume() # Continue playback

# And you can start/stop it

clock.stop() # Stop the clock
clock.start() # Start the clock

# Time in Sardine is mesured in "periods" or "p"

@swim
def counting_time(p=1, i=0):
  print(f"Time : {clock.beat}")
  again(counting_time, p=1, i=i+1)

Pa * d('bd') # By default, a player will repeat every period (p=1)
`

let superdirt_tutorial = `# About SuperDirt
`

let midi_tutorial = `# About MIDI
`

let tutorial_4 = `# About Tutorial 4
`

let tutorial_5 = `# About Tutorial 5
`

export const tutorialText = {
  "1.0 Time": time_tutorial,
  "1.1 SuperDirt": superdirt_tutorial,
  "1.2 MIDI": midi_tutorial,
  "1.3 Blabla": tutorial_4,
  "1.4 Blibli": tutorial_5,
}
