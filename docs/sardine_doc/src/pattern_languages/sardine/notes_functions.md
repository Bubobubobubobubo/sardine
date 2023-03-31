# Notes

Functions that better apply on groups of notes! They can turn a pattern into
a... funky pattern in no time! Most of these are really silly. Have fun.


<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Function name</td>
<td class="org-left"> Arguments</td>
<td class="org-left">Description</td>
<td class="org-left">Return type</td>
</tr>

<tr>
<td class="org-left">sopr</td>
<td class="org-left">[notes]</td>
<td class="org-left">The first note up an octave</td>
<td class="org-left">[notes]</td>
</tr>


<tr>
<td class="org-left">bass</td>
<td class="org-left">[notes]</td>
<td class="org-left">The first note down an octave</td>
<td class="org-left">[notes]</td>
</tr>

<tr>
<td class="org-left">disco</td>
<td class="org-left">[notes](::depth)</td>
<td class="org-left">Every pair note is up or down an octave</td>
<td class="org-left">[notes]</td>
</tr>


</tbody>
</table>

**Example of application:**
```python
@swim
def baba(p=1/2, i=0):
  D('jvbass', n='(disco C F A ::depth -1)', i=i)
  again(baba, p=1/2, i=i+1)
```
