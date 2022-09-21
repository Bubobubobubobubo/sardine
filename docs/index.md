# Sardine: Python based live coding library with MIDI and OSC support ✨

```
            ░██████╗░█████╗░██████╗░██████╗░██╗███╗░░██╗███████╗
            ██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝
            ╚█████╗░███████║██████╔╝██║░░██║██║██╔██╗██║█████╗░░
            ░╚═══██╗██╔══██║██╔══██╗██║░░██║██║██║╚████║██╔══╝░░
            ██████╔╝██║░░██║██║░░██║██████╔╝██║██║░╚███║███████╗
            ╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝
```

**Sardine** is a Python library tailored for musical live coding. It can turn Python into a fun music instrument and/or stage control tool for electronic musicians. Sardine is working on Windows/MacOS/Linux using Python 3.8+. It can send and receive MIDI, OSC and SuperDirt messages. **Sardine** is based on the principle of [temporal recursion](http://extempore.moso.com.au/temporal_recursion.html). It allows the execution of recursive functions synchronised with musical time. It means that you can sequence synthesizers, samples, MIDI and OSC signals or even arbitrary Python code with a strict and guaranteed timing! 

<video width="800"  controls>
  <source src="/images/sardinade7.mp4" type="video/mp4">
</video>

<video width="800"  controls>
  <source src="/images/sardinade6.mp4" type="video/mp4">
</video>

<video width="800"  controls>
  <source src="/images/sardinade5.mp4" type="video/mp4">
</video>

<video width="800"  controls>
  <source src="/images/sardinade4.mp4" type="video/mp4">
</video>

<video width="800"  controls>
  <source src="/images/sardinade3.mp4" type="video/mp4">
</video>

```python
@swim
def hop(d=0.5, i=0):
    M(delay=0.3, note='60 46 50 67', 
            velocity=127, channel=0).out(i)
    cc(channel=0, control=20, value=randint(1,127))
    anew(hop, d=0.5, i=i+1)

@swim
def bam(d=0.5, i=0):
    S('k:1_10', 
        cutoff='1_10*100 2000 4000!4', 
        speed='1 0.5').out(i)
    again(bam, d=choice([0.5, 0.25]), i=i+1)
```

