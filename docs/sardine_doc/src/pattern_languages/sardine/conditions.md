# Conditions

Every function from the function library can be applied conditionally. To do so, use the special `cond` keyword. This keyword is available to every function. There are many types of conditions you can apply on your pattern and you can even create conditions manually. Conditions are working by providing them binary values:

- `1` represents truth: `True`.
- `0` represents false: `False`.

The function above will turn the sequence into a palindrome but only on beats 1 and 3:

```python
Pa >> d('(pal F A C E ::cond (beat 0 2))')
```

In the Sardine Pattern Language, everything is a function, including the logical constructs themselves (`if`, `while`). It means that you can also add conditions to your conditions, etc&#x2026;

## If condition

The `if` condition is a binary condition: it will execute something if true, something else if false. In the following example, the function will play a clap for every pair bar (2, 4, etc.) and another sample on every odd bar.
 ```python   
Pa >> d('(if (every 2) cp sid')
```
    
The `nif` function can be used to reverse the logic (*not if*).

## While condition

The `while` condition is an unary condition: it will execute something if true, nothing at all if false. In the following example, the function will sometimes play a clap:
    
```python
Pa >> d('(while rand*5>2 cp)')
```
    
In that specific case, as a demonstration, we craft our own condition by using the greater-than (`>`) operator.
In the semblance of `if` and `nif`, there is also a `nwhile` condition to reverse the condition logic.

## Special condition functions

Some functions from the library can be used to build more complex conditions in conjunction with `if` or `while`. Use them wisely:
    
<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Function name</td>
<td class="org-left">Arguments</td>
<td class="org-left">Result</td>
</tr>


<tr>
<td class="org-left">beat</td>
<td class="org-left">1 or more beats numbers to match</td>
<td class="org-left">True or False</td>
</tr>


<tr>
<td class="org-left">every</td>
<td class="org-left">1 or more bars to match (modulo)</td>
<td class="org-left">True or False</td>
</tr>


<tr>
<td class="org-left">phase</td>
<td class="org-left">low and high phase value (0.0 &lt; x &lt; 1.0)</td>
<td class="org-left">True or False</td>
</tr>


<tr>
<td class="org-left">proba</td>
<td class="org-left">Simple probability in %</td>
<td class="org-left">True or False</td>
</tr>
</tbody>
</table>
    
The `beat` function is a great place to start. Let&rsquo;s play a clap on the start of the bar:
```python 
Pa >> d('(if (beat 0) cp)')
```
    
Let's add another beat to the equation. It will now also play on the following beat of the bar:
       
```python
Pa >> d('(if (beat 0 1) cp)')
```
    
You get it. Other functions work similarly.
These functions are cool but you might have guessed already that you can craft your own functions yourself if you are clever enough :) If you think of some cool functions to add, I&rsquo;ll be more than happy to include them into Sardine.

