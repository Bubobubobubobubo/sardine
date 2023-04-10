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
<th scope="col" class="org-left">alias</th>
<th scope="col" class="org-left">Brief description</th>
<th scope="col" class="org-left">Typical range</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">cutoff</td>
<td class="org-left">lpf</td>
<td class="org-left">Low-pass filter: cutoff freq (hertz)</td>
<td class="org-left">0-&gt;x us. &gt;2Khz</td>
</tr>

<tr>
<td class="org-left">resonance</td>
<td class="org-left">lpq res</td>
<td class="org-left">Low-pass resonance Q</td>
<td class="org-left">0.0 - 1.0 </td>
</tr>

<tr>
<td class="org-left">hcutoff</td>
<td class="org-left">hpf</td>
<td class="org-left">High-pass filter: cutoff freq (hertz)</td>
<td class="org-left">0-&gt;x us. &lt;1Khz</td>
</tr>

<tr>
<td class="org-left">hresonance</td>
<td class="org-left">hpq</td>
<td class="org-left">High-pass resonance Q</td>
<td class="org-left">0.0 - 1.0 </td>
</tr>

<tr>
<td class="org-left">bandf</td>
<td class="org-left">bpf</td>
<td class="org-left">Bandpass filter - cutoff freq (hertz)</td>
<td class="org-left">0-&gt;x</td>
</tr>

<tr>
<td class="org-left">bandq</td>
<td class="org-left">bpq</td>
<td class="org-left">Bandpass resonance Q</td>
<td class="org-left">0.0 - 1.0 </td>
</tr>

<tr>
<td class="org-left">djf</td>
<td class="org-left">djf</td>
<td class="org-left">DJ Filter: Low pass: 0 - 0.5, High pass: 0.5 - 1.0</td>
<td class="org-left">0.0 - 1.0</td>
</tr>

<tr>
<td class="org-left">hbrick</td>
<td class="org-left"></td>
<td class="org-left">Spectral high pass <a href="https://madskjeldgaard.dk/">Mads Kjeldgaard</a> </td>
<td class="org-left">0.0 - 1.0</td>
</tr>

<tr>
<td class="org-left">lbrick</td>
<td class="org-left"></td>
<td class="org-left">Spectral low pass <a href="https://madskjeldgaard.dk/">Mads Kjeldgaard</a> </td>
<td class="org-left">0.0 - 1.0</td>
</tr>


</tbody>
</table>

**Note:** Take caution with filter resonance. Values > 0.5 can be harsh!

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
