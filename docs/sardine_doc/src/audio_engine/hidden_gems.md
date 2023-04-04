# Hidden Gems

There are hidden gems in the **SuperDirt** engine. Note that you can also customize it with your own effects. This documentation, thus, is only covering the tip of the iceberg.

### Vowel
Vowel is installed with SuperDirt as a SuperCollider Quark. It uses a formant filter to emulate the sound of vowels applied to the sound. 

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
<td class="org-left">vowel</td>
<td class="org-left">formant filter to simulate vowels</td>
<td class="org-left">a e i o u</td>
</tr>

</tr>
</tbody>
</table>

```python
Pa * d('supersaw', n='40 52 64 52', vowel='e')
```
