# Effects

### Reverb

This is a pretty basic metallic sounding reverb. Not very usable but still.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Parameter</th>
<th scope="col" class="org-left">Brief description</th>
<th scope="col" class="org-left">Typical range</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">room</td>
<td class="org-left">Size of the room</td>
<td class="org-left">0-&gt;x</td>
</tr>


<tr>
<td class="org-left">size</td>
<td class="org-left">Size of the reverb - keep below 1 (inf)</td>
<td class="org-left">0-&gt;1</td>
</tr>


<tr>
<td class="org-left">dry</td>
<td class="org-left">Dry/Wet balance</td>
<td class="org-left">0-&gt;1</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25):
    D('hh', amp=1, room='(sin $.S)', dry=0.1, size='(sin $)')
    again(test_fx, p=0.25)
```


### Delay

The delay effect is initially built for **Tidal**, which is based on a cyclical time representation. However, it has been pre-configured here to work properly with **Sardine**. Be careful with the <span class="underline">feedback</span> if you don&rsquo;t want to see things explode!

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Parameter</th>
<th scope="col" class="org-left">Brief description</th>
<th scope="col" class="org-left">Typical range</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">delay</td>
<td class="org-left">Wet / Dry</td>
<td class="org-left">0-&gt;1</td>
</tr>


<tr>
<td class="org-left">delaytime</td>
<td class="org-left">Delay time</td>
<td class="org-left">0-&gt;x</td>
</tr>


<tr>
<td class="org-left">delayfeedback</td>
<td class="org-left">Amount of reinjection of the dry signal</td>
<td class="org-left">0-&gt;.99</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25):
    D('hh',
        speep='1|2|4',
        delay=1/2, delaytime=1/(2/3),
        delayfeedback='0.5+(rand/4)',
        amp=1
    )
    again(test_fx, p=0.25)
```


### Phaser

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Parameter</th>
<th scope="col" class="org-left">Brief description</th>
<th scope="col" class="org-left">Typical range</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">phaserrate</td>
<td class="org-left">Speed of phaser</td>
<td class="org-left">0-&gt;x</td>
</tr>


<tr>
<td class="org-left">phaserdepth</td>
<td class="org-left">Depth of phaser</td>
<td class="org-left">0-&gt;x</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25):
    D('jvbass',
        midinote='C|Eb|G|Bb',
        phaserrate='1~10',
        phaserdepth='(sin $*2)', amp=1
    )
    again(test_fx, p=0.5)
```


### Leslie

This is a simple emulation of a Leslie rotating speaker typically used in music for treating organ sounds, voices, and to add an eary tint to everything that goes through it. This is basically a way to play creatively with doppler effects.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Parameter</th>
<th scope="col" class="org-left">Brief description</th>
<th scope="col" class="org-left">Typical range</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">Leslie</td>
<td class="org-left">Dry / wet</td>
<td class="org-left">0-&gt;1</td>
</tr>


<tr>
<td class="org-left">lrate</td>
<td class="org-left">Rate</td>
<td class="org-left">0-&gt;x</td>
</tr>


<tr>
<td class="org-left">lsize</td>
<td class="org-left">Wooden cabinet size (in meters)</td>
<td class="org-left">0-&gt;x</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25):
    D('jvbass', amp=1, leslie=0.9,
        lrate=0.1, lsize='0.1+rand*2')
    again(test_fx, p=0.25)
```

### Tremolo

A simple tremolo effect.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Parameter</th>
<th scope="col" class="org-left">Brief description</th>
<th scope="col" class="org-left">Typical range</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">tremolorate</td>
<td class="org-left">Tremolo speed</td>
<td class="org-left">0-&gt;x</td>
</tr>


<tr>
<td class="org-left">tremolodepth</td>
<td class="org-left">Depth of tremolo</td>
<td class="org-left">0-&gt;x</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25, i=0):
    D('amencutup:[1:20]',
        tremolorate='16|32',
        tremolodepth='[0.0~1.0 0.25]', i=i
    )
    again(test_fx, p=0.5, i=i+1)
```

### Granular weird

This is a weird granular effect probably intended to serve as a building block for some other effect but you can use it as is nonetheless. It will slice your audio sample into tiny fragments of it while applying some amount of pitch-shifting on every sample.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Parameter</th>
<th scope="col" class="org-left">Brief description</th>
<th scope="col" class="org-left">Typical range</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">psrate</td>
<td class="org-left">Pitch-shift rate</td>
<td class="org-left">0-&gt;x</td>
</tr>


<tr>
<td class="org-left">psdisp</td>
<td class="org-left">Pitch-shift dispersion</td>
<td class="org-left">0-&gt;x</td>
</tr>


<tr>
<td class="org-left">scram</td>
<td class="org-left">Weird spectral effect</td>
<td class="org-left">0-&gt;x</td>
</tr>


<tr>
<td class="org-left">binshift</td>
<td class="org-left">Spectral bin shifter</td>
<td class="org-left">0-&gt;x</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25, i=0):
    D('amencutup:[1:20]',
            psrate='2',
            psdisp='[0:1,0.5]',
            i=i)
    again(test_fx, p=0.5, i=i+1)
```
