# Distortion

Nobody knows why but **SuperDirt** is full of distortion effects. I suppose that saturation
and distortion are good effects to apply to audio samples. Don't be afraid and try them all.


### Squiz

Will distort your signal, combination of multiple effects put together. It works better if you input multiples of two as parameters.

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
<td class="org-left">squiz</td>
<td class="org-left">amount</td>
<td class="org-left">0.2-&gt;x</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25):
    D('tabla:rand*200', cut=1,
            squiz='0|2|4|8',
            midinote='C|F|Bb|E5b', amp=1)
    again(test_fx, p=0.5)
```

### Triode

Another type of distortion. Emulating a triode distortion unit.

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
<td class="org-left">triode</td>
<td class="org-left">Distortion amount</td>
<td class="org-left">0-&gt;x</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25):
    D('tabla:rand*200', cut=1,
            triode='rand', # comment me
            midinote='C|F|Bb|Eb5', amp=1)
    again(test_fx, p=0.5)
```

### Distort

Heavy distortion that will/can wildly change the spectrum of your sound.

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
<td class="org-left">distort</td>
<td class="org-left">Distortion amount</td>
<td class="org-left">0-&gt;x</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25):
    D('sd:rand*200', cut=1,
            distort='0|0.5',
            midinote='C|G', amp=1)
    again(test_fx, p=0.5)
```

### Shaping

One of my favorites. It adds some warness (and loudness) to any sound. It sounds more natural
than just pushing `gain` or `amp` up. Use it if you want to be loud and gritty, not if you just
want to play something louder.

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
<td class="org-left">shape</td>
<td class="org-left">Amplification amount</td>
<td class="org-left">0-&gt;x</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25, i=0):
    D('amencutup:[1:20]', shape='[0:1,0.1]', i=i)
    again(test_fx, p=0.5, i=i+1)
```

### Crush

Crush will.. crush your sound. You get it!

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
<td class="org-left">crush</td>
<td class="org-left">Crushing Factor</td>
<td class="org-left">0-&gt;x</td>
</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25, i=0):
    D('bd sn hh sn', crush=4, i=i)
    again(test_fx, p=0.5, i=i+1)
```

