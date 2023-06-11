# Conditions

Every function in the **Sardine Pattern Language** can be applied conditionally. To do so, use the special `cond` keyword argument. This keyword is available for every function. There are many types of conditions you can apply on your pattern and you can even create your own types of conditions. 


There is no `True` or `False` statement in **SPL**. Conditions are created by using binary values:
- `1` represents truth: `True`.
- `0` represents false: `False`.

The function above will turn the sequence into a palindrome but only on beats 1 and 3:

```python
Pa * d('(pal F A C E ::cond (beat 0 2))')
```

Of course, the rabbit goes down and you go after it. Any condition can receive conditions, etc...

## If condition

The `if` condition is a binary condition: it will execute something if true (`1`), something else if false (`0`). In the following example, the function will play a clap for every pair bar (2, 4, etc.) and another sample on every odd bar.
 ```python   
Pa * d('(if (every 2) cp sid')
```

The `nif` function can be used to reverse the logic (*not if*) just by typing one letter Saving 20 milliseconds is important because life is too short.

## While condition

The `while` condition is an unary condition: it will execute something if true (`1`), nothing at all if false (`0`). In the following example, the function will sometimes play a clap:

```python
Pa * d('(while rand*5>2 cp)')
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
<td class="org-left">Description</td>
<td class="org-left">Result</td>
</tr>


<tr>
<td class="org-left">beat</td>
<td class="org-left">... numbers</td>
<td class="org-left">1 or more beats numbers to match</td>
<td class="org-left">Boolean</td>
</tr>

<tr>
<td class="org-left">phase</td>
<td class="org-left">low high </td>
<td class="org-left">Check if currently in-between range of phase (between 0.0 and 1.0)</td>
<td class="org-left">Boolean</td>
</tr>

<tr>
<td class="org-left">every</td>
<td class="org-left">... bar_numbers </td>
<td class="org-left">Similar to TidalCycles every function. Will be true every x bars.</td>
<td class="org-left">Boolean</td>
</tr>

<tr>
<td class="org-left">proba</td>
<td class="org-left">probability</td>
<td class="org-left">Simple probability in %</td>
<td class="org-left">Boolean</td>
</tr>

<tr>
<td class="org-left">modbar</td>
<td class="org-left">choice faces</td>
<td class="org-left">Simulation of a dice with n faces.</td>
<td class="org-left">Boolean</td>
</tr>

<tr>
<td class="org-left">obar</td>
<td class="org-left">None</td>
<td class="org-left">Check if the current bar is odd</td>
<td class="org-left">Boolean</td>
</tr>

<tr>
<td class="org-left">ebar</td>
<td class="org-left">None</td>
<td class="org-left">Check if the current bar is even</td>
<td class="org-left">Boolean</td>
</tr>


<tr>
<td class="org-left">modbar</td>
<td class="org-left">modulo</td>
<td class="org-left">Modulo against current bar number</td>
<td class="org-left">Boolean</td>
</tr>

</tbody>
</table>
    
The `beat` function is a great to start with because it is also very simple. Let's play a clap on the start of the bar:
```python 
Pa * d('(if (beat 0) cp)')
```
    
Let's add another beat to the equation. It will now also play on the following beat of the bar:
       
```python
Pa * d('(if (beat 0 1) cp)')
```
    
You get it. Other functions are working in a similar fashion. These functions are cool but you might have guessed already that you can craft your own functions yourself if you are clever enough :) If you think of some cool functions to add, I'll be more than happy to include them into Sardine :)
