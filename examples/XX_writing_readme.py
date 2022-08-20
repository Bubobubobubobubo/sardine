@swim
def hop(d=0.5, i=0):
    M(delay=0.3, note=60, velocity=127, channel=0).out()
    anew(hop, d=0.5, i=i+1)
