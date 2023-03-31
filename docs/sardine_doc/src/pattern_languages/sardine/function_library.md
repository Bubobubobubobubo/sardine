# Function Library


The **Sardine** pattern language also supports&#x2026; function calls! They look a bit like LISP functions. The function library used in **Sardine** is to be considered as a giant playground. It acts as a **de facto** repository for some processes that I find interesting when playing music with patterns. In the future, I hope that more people will come and add their functions to the library.

Function calls are rather simple but there are some rules to follow depending on the function you call. The general rules are:

-   Calling functions work by adding the function name after opening parentheses : `(sopr 1 2 3 4)`.
-   Some functions take any amount of arguments, some have positional arguments.
    -   any amount: `(func 1 2 3 4 5 6 ...)`
    -   positional: `(func 1 2)` where `1` has a meaning and `2` has a meaning.
-   Some functions can take keyword arguments, such as `(disco C4 D4 E4 ::depth 2)`.

To know how to use a function, it is best to refer to this documentation. You can&rsquo;t expect your code editor to tell you because `strings` are not really considered as code! I will always provide indications on how to call the function, telling you the role of each argument. `...` means that the function can take any number of arguments. I will always indicate the return type of the function.

## List of undocumented functions

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
<td class="org-left">quant</td>
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


