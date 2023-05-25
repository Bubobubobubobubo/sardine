# Low Frequency Oscillators

These functions are implementing low-frequency oscillators whose period is based on a selectable number of clock beats. They offer another better flavor to the basic technique involving `sin()` or `cos()` functions. 

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">

<colgroup>

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left"><b>Function</b></td>
<td class="org-left"><b>Arguments</b></td>
<td class="org-left"><b>Description</b></td>
<td class="org-left"><b>Return type</b></td>
</tr>


<tr>
<td class="org-left"><b>lsin</b></td>
<td class="org-left">period</td>
<td class="org-left">sinusoïdal low-frequency oscillator (-1, 1)</td>
<td class="org-left">int|float</td>
</tr>


<tr>
<td class="org-left"><b>ltri</b></td>
<td class="org-left">period</td>
<td class="org-left">triangular low-frequency oscillator (-1, 1)</td>
<td class="org-left">int|float</td>
</tr>

<tr>
<td class="org-left"><b>lsaw</b></td>
<td class="org-left">period</td>
<td class="org-left">sawtooth low-frequency oscillator (-1, 1)</td>
<td class="org-left">int|float</td>
</tr>

<tr>
<td class="org-left"><b>lrect</b></td>
<td class="org-left">period, <em>PWM/Duty</em></td>
<td class="org-left">rectangular low-frequency oscillator. Argument for pulse width modulation. (-1, 1)</td>
<td class="org-left">int|float</td>
</tr>

<tr>
<td class="org-left"><b>alsin</b></td>
<td class="org-left">period</td>
<td class="org-left">unipolar sinusoïdal low-frequency oscillator (0, 1)</td>
<td class="org-left">int|float</td>
</tr>


<tr>
<td class="org-left"><b>altri</b></td>
<td class="org-left">period</td>
<td class="org-left">unipolar triangular low-frequency oscillator (0, 1)</td>
<td class="org-left">int|float</td>
</tr>


<tr>
<td class="org-left"><b>altri</b></td>
<td class="org-left">period</td>
<td class="org-left">unipolar sawtooth low-frequency oscillator (0, 1)</td>
<td class="org-left">int|float</td>
</tr>

</tbody>
</table>

Remember that you can do math operations on these oscillators such as clamping (`clamp`), scaling (`scale`), etc. You can also pattern the `period` or `pwm` for extra weirdness or for doing custom shapes. Folding and wrapping operations can be very useful to generate interesting shapes on a large time scale. 
