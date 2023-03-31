# Repeat

    
- The `!` operator inspired by ****TidalCycles**** is used to denote the repetition of a value.
  - You need to add a number or a list to its right side.

```python
@swim
def repeat_stuff(p=0.5, i=0):
    D('pluck|jvbass', speed='1:2', n='C4!4 E4!3 E5 G4!4', i=i)
    again(repeat_stuff, p=0.5, i=i+1)
```
