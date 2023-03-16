# Mathematical

Simple mathematical functions that can be applied on any number token.
They are generally very simple operations that you might find on a
digital calculator or on any interface capable of computation:

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
 <td class="org-left">sin</td>
 <td class="org-left">x, &#x2026;</td>
 <td class="org-left">Sinusoïd function</td>
 <td class="org-left">1 or more Number</td>
 </tr>
 
 
 <tr>
 <td class="org-left">cos</td>
 <td class="org-left">x, &#x2026;</td>
 <td class="org-left">Cosinus function</td>
 <td class="org-left">1 or more Number</td>
 </tr>
 
 
 <tr>
 <td class="org-left">tan</td>
 <td class="org-left">x, &#x2026;</td>
 <td class="org-left">Tangent function</td>
 <td class="org-left">1 or more Number</td>
 </tr>
 
 
 <tr>
 <td class="org-left">abs</td>
 <td class="org-left">x, &#x2026;</td>
 <td class="org-left">Absolute function</td>
 <td class="org-left">1 or more Number</td>
 </tr>
 
 
 <tr>
 <td class="org-left">max</td>
 <td class="org-left">x, &#x2026;</td>
 <td class="org-left">Maximum function</td>
 <td class="org-left">Number</td>
 </tr>
 
 
 <tr>
 <td class="org-left">min</td>
 <td class="org-left">x, &#x2026;</td>
 <td class="org-left">Minimal function</td>
 <td class="org-left">Number</td>
 </tr>
 
 
 <tr>
 <td class="org-left">mean</td>
 <td class="org-left">x, &#x2026;</td>
 <td class="org-left">Arithmetic mean function</td>
 <td class="org-left">Number</td>
 </tr>
 
 
 <tr>
 <td class="org-left">scale</td>
 <td class="org-left">[], imin, imax, omin, omax</td>
 <td class="org-left">Scaling a list from range to range</td>
 <td class="org-left">List</td>
 </tr>
 
 
 <tr>
 <td class="org-left">quant</td>
 <td class="org-left">[], []</td>
 <td class="org-left">Quantize the first list to values in second</td>
 <td class="org-left">List</td>
 </tr>
 
 
 <tr>
 <td class="org-left">clamp</td>
 <td class="org-left">x, y, z</td>
 <td class="org-left">Simple clamping function (x between y and z)</td>
 <td class="org-left">List or Number</td>
 </tr>
 </tbody>
 </table>
    
**Example of application:**

```python
@swim
def demo(p=1/4, i=0):
    D('moog:5', lpf='(sin $*2500)', res='(cos $)/2', i=i, legato=0.1)
    D('cp', speed='0+(abs -rand*5)', d=8, i=i)
    again(demo, p=1/8, i=i+1)
```   

These functions are the bread and butter of a good high-speed **Sardine** pattern. They will allow you to create **signal-like** value generators (*e.g* **Low frequency oscillators**). They are also very nice to use in connjunction with `$` or any timed value. You will find many creative ways to use them (especially by combining with arithmetic operators).


