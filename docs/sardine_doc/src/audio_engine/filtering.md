# Filtering

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
<colgroup>
<col  class="org-left" />
<col  class="org-left" />
<col  class="org-left" />
<col  class="org-left" />
</colgroup>

<thead>
<tr>
<th scope="col" class="org-left">Parameter</th>
<th scope="col" class="org-left">Brief description</th>
<th scope="col" class="org-left">Typical range</th>
<th scope="col" class="org-left">alias</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">cutoff</td>
<td class="org-left">Low-pass filter cutoff frequency (in hertz)</td>
<td class="org-left">0-&gt;x us. &gt;2Khz</td>
<td class="org-left">lpf</td>
</tr>

<tr>
<td class="org-left">hcutoff</td>
<td class="org-left">High-pass filter cutoff frequency (in hertz)</td>
<td class="org-left">0-&gt;x us. &lt;1Khz</td>
<td class="org-left">hpf</td>
</tr>

<tr>
<td class="org-left">bandf</td>
<td class="org-left">Bandpass filter cutoff frequency (in hertz)</td>
<td class="org-left">0-&gt;x</td>
<td class="org-left">bpf</td>
</tr>

<tr>
<td class="org-left">resonance</td>
<td class="org-left">Filter resonance</td>
<td class="org-left">0-&gt;.99</td>
<td class="org-left">res</td>
</tr>

<tr>
<td class="org-left">bandqf</td>
<td class="org-left">Bandpass resonance</td>
<td class="org-left">0-&gt;.99</td>
<td class="org-left">???</td>

<tr>
<td class="org-left">djf</td>
<td class="org-left">Low pass: 0 - 0.5, High pass: 0.5 - 1.0</td>
<td class="org-left">0.0 - 1.0</td>
<td class="org-left">djf</td>
</tr>
</tbody>
</table>

```python
# low pass randomized
@swim
def test_fx(p=0.25):
    D('jvbass',
        midinote='C|C|Eb|G|Bb',
        cutoff='rand*7000', resonance='rand/2', amp=1
    )
    again(test_fx, p=0.5)

# djf
@swim
def djf(p=1, i=0):
    D('supersaw', n='40 52 64 52', 
    djf=random(), i=i)
    again(djf, p=1, i=i+1)
```

### Spectral comb filter
Included in Superdirt, engineered by [Mads Kjeldgaard](https://madskjeldgaard.dk/). Width and number of teeth are controlled by one floating point number. Note that as you increase the comb, more frequencies will be filtered out, resulting in reduced gain. 

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
<td class="org-left">comb</td>
<td class="org-left">Spectral comb filter</td>
<td class="org-left">0.0 - 1.0</td>
</tr>

</tr>
</tbody>
</table>

```python
@swim
def test_fx(p=0.25):
    D('jvbass',
        midinote='C|C|Eb|G|Bb',
        cutoff='rand*7000', resonance='rand/2', amp=1
    )
    again(test_fx, p=0.5)
```
