# Rhythm Functions

This set of functions is all about generating and manipulating rhythms. There are different ways to generate rhythms using Sardine. The system is quite permissive and will allow you to do a lot of things either by manipulating the `period` argument, by filtering some of your events, by adding silences, etc... This variety of approaches is also reflected in rhythm functions.

## euclid (eu)
## neuclid (neu)
## mask 
## numclid (e)
## binary rhythm

## Euclidian

Functions that apply a boolean mask on a pattern. This mask will either leave the pattern as is or replace some values by silences. The euclidian rhythm generator lives in this category. I know that you were looking for it :)
    
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
 <td class="org-left">[pattern], pulses, steps, rotation</td>
 <td class="org-left">Euclidian rhythm</td>
 <td class="org-left">[pattern]</td>
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
 <td class="org-left">[pattern], [mask]</td>
 <td class="org-left">Boolean mask applied on a list</td>
 <td class="org-left">[pattern]</td>
 </tr>
 
 
 <tr>
 <td class="org-left">vanish</td>
 <td class="org-left">percentage, [pattern]</td>
 <td class="org-left">Remove x% of elements from pattern</td>
 <td class="org-left">[pattern]</td>
 </tr>
 </tbody>
 </table>
    
**Example of application:**
    
```python
@swim
def demo(p=1/8, i=0):
    D('(eu drum 5 8)', i=i)
    D('(eu [cp linnhats] 3 8)', i=i)
    D('(neu voodoo:rand*5  5 16)', i=i, r=0.5)
    again(demo, p=1/4, i=i+1)
```   

You will notice that you can now generate some interesting rhythm by combining
the euclidian rhythms with `rate` and `div`. The quirks of the **Sardine**
pattern system will also generate very surprising rhythms, especially when 
playing with lists of audio samples.
    

