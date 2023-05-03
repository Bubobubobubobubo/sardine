# Mini notation

The most basic pattern you can play using Tidal/Vortex is:

```python
d1 * s('bd hh sn hh')
```

This will play a drum pattern using the `d1` Tidal player. `s` is a shortcut notation for the `sound` function. This function allows you to make a pattern of SuperDirt audio samples/synthesizers in a similar fashion to the basic behavior of Sardine. Note the usage of a *string* to define an expression, similar to how SPL or Ziffers are working.

This expression is written using the **Tidal mini-notation**, a powerful language made to describe complex recurring cycles of events. The first step to master it is to learn the mini-notation.

## Mini-notation

The `bd hh sn hh` part is using Tidal mini-notation, a custom patterning DSL (*domain specific language*) similar to other notations available in Sardine. Tidal inspired most of the constructs you will find both in SPL and Ziffers. You will feel familiar with it in no time because of the redundancies.

| Name | Symbol | Example | 
|:-:|:------:|:-------:|
| **Rest** | `~` | `d1 * s("~ hh")` |   
| **Group** | `[ ]`| `d1 * s("[bd sd] hh")` |
| **Group** | `.` | `d1 * s("bd sd . hh hh hh")`|
| **Superpose** | `,` |  `d1 * s("[bd sd, hh hh hh])"` |
| **Multiply** | `*`  | `d1 $ s("bd*2 sd")` |
| **Slow** | `/`  | `d1 * s("bd/2")` |
| **Choice** | &#124;  | d1 * s("[bd &#124; cp &#124; hh]") |
| **Alternation** | `< >`  | `d1 * s("bd <sd hh cp>")` |
| **Replicate** | `!`  | `d1 * s("bd!3 sd")` |
| **Elongate** | `_`  | `d1 * s("bd _ _ ~ sd _")`	 |
| **Elongate** | `@`  | `d1 * s("superpiano@3 superpiano")`	 |
| **Random** | `?`  | `d1 * s("bd? sd")`	 |
| **Select** | `:`  | `d1 * s("bd:3")`	 |
| **Euclid** | `()`  | `d1 * s("bd(3,8)"`	 |
| **Polymetric** | `{}`  | `d1 $ s("{bd bd bd bd, cp cp hh}")`	 |
| **Polymetric subdivision** | `{}%`  | `d1 * s("{bd cp hh}%8")`	 |

Here is a short description of each operation:

| Name | Description |
|:----:|:-----------:|
| **Rest** | Rest / silence: no event |
| **Group** | Grouping multiple values on the same step |
| **Group** | Grouping multiple values on the same step |
| **Superpose** | Superpose multiple values on same step |
| **Multiply** | Multiply the number of values on that step |
| **Slow** | The event will only play every /n cycles |
| **Choice** | Choose between one or many elements |
| **Alternation** | Alternate between each of the values each cycle |
| **Replicate** | Replicate the event (but not on the same step) |
| **Elongate** | Elongate the duration of that event (multiple steps) |
| **Elongate** | Elongate the duration of that event (multiple steps) |
| **Random** | 50/50 chance of returning the value (or rest) |
| **Select** | Pick a sample in the SuperDirt folder (sound library) |
| **Euclid** | Euclidian pattern (e.g. `bd(5,8)`)|
| **Polymetric** | Polymetry using the grouping |
| **Polymetric subdivision** | Variant of the preceding operation |

The mini-notation is only the start of learning Tidal/Vortex. Once you are comfortable using it, you can start to go further by chaining functions together and by diving into *function composition*.
