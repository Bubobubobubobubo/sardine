# Function Library


The **Sardine** pattern language also supports&#x2026; function calls! They look a bit like LISP functions. The function library used in **Sardine** is to be considered as a giant playground. It acts as a **de facto** repository for some processes that I find interesting when playing music with patterns. In the future, I hope that more people will come and add their functions to the library.

Function calls are rather simple but there are some rules to follow depending on the function you call. The general rules are:

-   Calling functions work by adding the function name after opening parentheses : `(sopr 1 2 3 4)`.
-   Some functions take any amount of arguments, some have positional arguments.
    -   any amount: `(func 1 2 3 4 5 6 ...)`
    -   positional: `(func 1 2)` where `1` has a meaning and `2` has a meaning.
-   Some functions can take keyword arguments, such as `(disco C4 D4 E4 ::depth 2)`.

To know how to use a function, it is best to refer to this documentation. You can&rsquo;t expect your code editor to tell you because `strings` are not really considered as code! I will always provide indications on how to call the function, telling you the role of each argument. `...` means that the function can take any number of arguments. I will always indicate the return type of the function.

## Simple functions

Simple functions are mathematical functions that can be applied on any number token. They are generally very simple operations that you might find on a digital calculator or on any interface capable of computation:

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
    
    @swim
    def demo(p=1/4, i=0):
        D('moog:5', lpf='(sin $*2500)', res='(cos $)/2', i=i, legato=0.1)
        D('cp', speed='0+(abs -rand*5)', d=8, i=i)
        again(demo, p=1/8, i=i+1)
    
These functions are the bread and butter of a good high-speed **Sardine** pattern. They will allow you to create **signal-like** value generators (*e.g* **Low frequency oscillators**). They are also very nice to use in connjunction with `$` or any timed value. You will find many creative ways to use them (especially by combining with arithmetic operators).

## Euclidian and mask functions

This category is made of functions that apply a mask on a pattern. This mask is a boolean mask that will either leave the pattern as is or replace some values by a silence. The euclidian rhythm generator lives in this category. I know that you were looking for it :)
    
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
 <td class="org-left">euclid</td>
 <td class="org-left">x, pulses, steps, rotation</td>
 <td class="org-left">Euclidian rhythm</td>
 <td class="org-left">List</td>
 </tr>
 
 
 <tr>
 <td class="org-left">eu</td>
 <td class="org-left">//</td>
 <td class="org-left">//</td>
 <td class="org-left">//</td>
 </tr>
 
 
 <tr>
 <td class="org-left">neuclid</td>
 <td class="org-left">//</td>
 <td class="org-left">Inverse euclidian rhythm</td>
 <td class="org-left">//</td>
 </tr>
 
 
 <tr>
 <td class="org-left">neu</td>
 <td class="org-left">//</td>
 <td class="org-left">//</td>
 <td class="org-left">//</td>
 </tr>
 
 
 <tr>
 <td class="org-left">mask</td>
 <td class="org-left">[], []</td>
 <td class="org-left">Boolean mask applied on a list</td>
 <td class="org-left">List</td>
 </tr>
 
 
 <tr>
 <td class="org-left">vanish</td>
 <td class="org-left">[], percentage</td>
 <td class="org-left">Remove x% of elements from pattern</td>
 <td class="org-left">List</td>
 </tr>
 </tbody>
 </table>
    
**Example of application:**
    
    @swim
    def demo(p=1/8, i=0):
        D('(eu drum 5 8)', i=i)
        D('(eu [cp linnhats] 3 8)', i=i)
        D('(neu voodoo:rand*5  5 16)', i=i, r=0.5)
        again(demo, p=1/4, i=i+1)
    
You will notice that you can now generate some interesting rhythm by combining the euclidian rhythms with `rate` and `div`. The quirks of the **Sardine** pattern system will also generate very surprising rhythms, especially when playing with lists of audio samples.
    
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
<td class="org-left">dmitri</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">voice</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">sopr</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">quant</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">disco</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">bass</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">sopr</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">invert</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">aspeed</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">expand</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">pal</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">rev</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">leave</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">insertp</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">insert</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">insertprot</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">shuf</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>


