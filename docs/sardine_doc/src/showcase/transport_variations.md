# Transport Variations
<iframe width="700" height="500" src="https://www.youtube.com/embed/1FM4BhySs1Y?start=22" title="Tranport Variations" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

**Transport Variations** (by HighHarmonics) is a composed live coding work of experimental electronic music. It is loosely an hommage to the early French pioneers of musique concrète, Pierre Schaeffer and Pierre Henry.
- Custom samples are from field recordings of public transportation - light rail, bus hydraulic lift, streetcars. 
- A set of performance presets have been composed and arranged based on each of the main samples.
- Live coding is done in Sardine, with use of Sardine features:
    - [Amphibian Variables](../diving_deeper/amphibian_variables.md)
    - Players and @swim functions
    - [Presets](../diving_deeper/presets.md)
- [Sardine, python, and MaxMSP code files](https://github.com/HighHarmonics2/livecoding/tree/main/sardine/TransportVariations) in GitHub.

## Organization 
Presets are built up (composed) by:
- Generating sample slice values (begin/end points) together with a pulse value ("period" in Sardine) - with a custom python function that uses contrained randomness.
- Adding values or patterns for amplitude, sample speed, frequency, sample duration, pan.
- Adding sample processing and signal processing parameters (fx).

### Preset variations  
- Presets values are assigned to the Sardine Amphibian Variables which are used in the main @swim function.
- Presets values are also saved in the performance code to support alternation and variations of presets. This is how the structure of the performance is built.
- Liveness is maintained through constant experimentation with the preset variations and preset combinations.
- Put simply - *I first generate and compose the presets, then in a performance session, play and vary the presets.*

### Audio processing  
- Output from SuperCollider is routed to MaxMSP, which acts as a mixer.
- An EQ type filter is added to each channel using FabFilter Pro-Q3.
- EQ filters also have presets, which are changed with a Midi Controller.
- Display of the filter output during performance shows how the filter changes impact the audio.

## Transport Variations in Sardine
Code files available in [HighHarmonics Github](https://github.com/HighHarmonics2/livecoding/tree/main/sardine/TransportVariations)

- Sardine Players (Pa, Pb, etc) are set up to play the transport sample files. Multiple players for each sound allow for variants with different parameter and pattern values. These work well for playback where the sound source is more recognizable. 
    ```python
    # rail car rattles
    Pa * d('trimet:0', p=2, legato=2, amp='[0.1:1,0.12] [1:0.1,0.12]', pan='[0:1,0.1] [1:0,0.15]', **rev1, orbit=4)
    Pa * d('trimet:0', p=2, legato=1.2, amp='.8', speed= 1, pan='[0:1,0.1]', **rev1, orbit=0)

    # air blast
    Pb * d('trimet:3', p='2 3 1', legato='0.8 2 0.4', amp='0.4~0.8', freq='260!2 280', pan='rand', comb='[.1~.4]', **rev1, orbit=5)

    # streetcar
    Pc * d('trimet:5', p=2, pan='[0:1,.2]', amp='0.5 0.9 0.2', legato=8, **rev0, orbit=6)
    ```

- Sardine @swim functions are setup with a group of 9 Amphibian variables controlling parameter values of sample, begin, end, speed, frequency, amp, pan, legato, period. Presets for reverb and effects processing parameters are included in the @swim.
    ```python
    @swim
        def slicerA1(p=1, i=0):
        D(V.s, chance='often',
        begin=V.b, end=V.e, speed=V.S, amp=V.A, pan=V.P, freq=V.F,
        legato=V.L, 
        **rev1, # del0,
        **fx, 
        d=1, rate=1, orbit=0, i=i)
        again(slicerA1, p=P('(v p)', i), i=i+1) 
    ```

- The Amphibian Variable presets are grouped into a python dictionary (presetsTrimet). Calling a dictionary key is used to assign all of the values into the Amphibian Variables and FX parameters. Executing on this while the @swim is running will change all of the Amphibian Variables and FX values at once. It does this on the next @swim iteration and is not subject to the normal rule of change happens only at the next bar. Example:

    ```python
    V.s, V.b, V.e, V.p, V.A, V.S, V.F, V.L, V.P, fx, desc = presetsTrimet['speed1']
    fx = {'accelerate': 0, 'comb':0.4, 'shape':0.5, 'vowel':'0 e a', 'hpf':'200 300 800 1200 300', 'hresonance':'0.4' }
    ```

- Presets are also replicated in the execution code so that individual parameter changes can be easily accomplished. Example:

    ```python
    V.s, V.b, V.e, V.p, V.A, V.S, V.F, V.L, V.P, fx, desc = ['trimet:0', 0.5397, 0.775, .4, 0.8, 1, 260, 0.5, '[0 1]', {'accelerate':1, 'comb':0.1, 'shape':0.2, 'vowel':'e a'}, 'speed1']
    ```

- This results in a large amount of code that is essentially only for variable and preset assignment. But it makes the act of evolving the variations much easier.
- The end result is that large or small changes can be made instantly building a musical structure or shaping the constantly evolving variations. 



