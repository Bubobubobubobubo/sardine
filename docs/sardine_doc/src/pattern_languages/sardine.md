# Sardine Pattern Language

The pattern language is everywhere in **Sardine**. Everytime you use any of the senders (`D()`, `N()`, `P()` and their lowercase variants), you are likely to encounter it. **Sardine** automatically turns every argument it receives as a `string` in an expression that is read using the **pattern language**:

```python
D('bd', speed=1, legato=2) # speed and legato are using regular Python types
D('b', speed='1|2', legato='1~4') # speed and legato are now patterns (string)
```
**Pattern Object**
Sardine also has a pattern object. This is useful and required when patterning outside of Senders. Examples would be to pattern the period value in the `again()` statement, or patterning the `clock.tempo` value. 

See [Diving Deeper > Pattern Object](../diving_deeper/pattern_object.md).

### Patterning - a programming language within
You can't even use a synthesizer or play a note without writing at least one pattern (the initial string). One call to the senders/handlers can result in multiple patterns being interpreted by the **Sardine pattern language** at once.

Think of it as having a second programming language inside your main programming language.

So, why use the Sardine pattern language?

- It is an efficient way to create change and variety in musical output. 
- It saves space, it makes it easier to express complex transformations fast.
- It gives you access to new operators that **Python** doesn't provide.
- It makes writing lists way easier and less verbose.
- It is the key that unlocks Sardine's expressive potential. 
- Patterning is a basic tool available in most livecoding environments. 


