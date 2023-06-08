# Time Functions

Some functions can return information about the Sardine clock. The information will be updated everytime you evaluate an expression. Depending on the moment when your loop takes place, you might see some values recurring because you are not polling time continuously but at predictible rythmic moments. 

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
<td class="org-left">time</td>
<td class="org-left">year month day hour minute second micro</td>
<td class="org-left">Return information about wall clock time. No argument will return current Sardine internal time.</td>
<td class="org-left">int</td>
</tr>


<tr>
<td class="org-left">bar</td>
<td class="org-left"></td>
<td class="org-left">Current bar</td>
<td class="org-left">int</td>
</tr>


<tr>
<td class="org-left">phase</td>
<td class="org-left"></td>
<td class="org-left">Current phase</td>
<td class="org-left">float</td>
</tr>


<tr>
<td class="org-left">beat</td>
<td class="org-left"></td>
<td class="org-left">Current beat</td>
<td class="org-left">float</td>
</tr>


<tr>
<td class="org-left">unix</td>
<td class="org-left"></td>
<td class="org-left">Current Unix Time</td>
<td class="org-left">int</td>
</tr>

</tbody>
</table>
