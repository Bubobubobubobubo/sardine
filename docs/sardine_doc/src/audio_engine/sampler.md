# Sampler

Everytime you play an audio sample, this sampler will be invoked. It is pretty powerful and it is worth spending some time studying its behavior.

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
<td class="org-left">amp</td>
<td class="org-left">Sound volume (linear scaling)</td>
<td class="org-left">0-&gt;x</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">gain</td>
<td class="org-left">Sound volume (exponential scaling)</td>
<td class="org-left">0-&gt;1</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">freq</td>
<td class="org-left">Pitch around given frequency</td>
<td class="org-left">0-&gt;x</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">midinote</td>
<td class="org-left">Pitch around given MIDI note</td>
<td class="org-left">0-127</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">note</td>
<td class="org-left">Pitch around given note</td>
<td class="org-left">???</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">octave</td>
<td class="org-left">Pitch up or down depending on octave number</td>
<td class="org-left">0-&gt;x</td>
<td class="org-left">oct</td>
</tr>


<tr>
<td class="org-left">sound</td>
<td class="org-left">Implicit (first argument of <b>D()</b>)</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">begin</td>
<td class="org-left">Start position of audio playback</td>
<td class="org-left">0-&gt;1</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">end</td>
<td class="org-left">End position of audio playback</td>
<td class="org-left">0-&gt;1</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">speed</td>
<td class="org-left">Sample playback, impacts pitch. Negative will play reverse</td>
<td class="org-left">-x-&gt;0-&gt;x</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">accelerate</td>
<td class="org-left">Rising sample playback speed (pitch glissando)</td>
<td class="org-left">-x-&gt;0-&gt;x</td>
<td class="org-left">accel</td>
</tr>


<tr>
<td class="org-left">cps</td>
<td class="org-left">Implicit (cycles per second, inherited from Tidal)</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">loop</td>
<td class="org-left">???</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">delta</td>
<td class="org-left">Unused</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">cut</td>
<td class="org-left">Cut other sounds playing on same orbit, start playing</td>
<td class="org-left">0 or 1</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">legato</td>
<td class="org-left">Play sample for the given duration (without cutting others)</td>
<td class="org-left">0-&gt;x</td>
<td class="org-left">leg</td>
</tr>


<tr>
<td class="org-left">pan</td>
<td class="org-left">Pan sound from left to right speaker (by default)</td>
<td class="org-left">0-&gt;1</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">orbit</td>
<td class="org-left">Play sound/synth on the given audio effect bus (0 - 11)</td>
<td class="org-left">0-&gt;11</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">latency</td>
<td class="org-left">Add a latency to audio playback (in seconds)</td>
<td class="org-left">0-&gt;x</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">lag</td>
<td class="org-left">Similar to latency/offset</td>
<td class="org-left">0-&gt;x</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">offset</td>
<td class="org-left">Similar to latency/lag</td>
<td class="org-left">0-&gt;x</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>

