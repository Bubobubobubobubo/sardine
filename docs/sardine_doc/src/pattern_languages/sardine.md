# Sardine Pattern Language

The pattern language is everywhere in **Sardine**. Everytime you use any of the senders (`D()`, `N()`, `P()` and their lowercase variants), you are likely to encounter it. **Sardine** automatically turns every argument it receives as a `string` in an expression that is read using the **pattern language**:

```python
D('bd', speed=1, legato=2) # speed and legato are using regular Python types
D('b', speed='1|2', legato='1~4') # speed and legato are now patterns (string)
```

You can't even use a synthesizer or play a note without writing at least one pattern (the initial string). One call to the senders/handlers can result in multiple patterns being interpreted by the **Sardine pattern language** at once.

Think of it as having a second programming language inside your programming language.

Why?

- It saves space, it makes it easier to express complex transformations fast.
- It gives you access to new operators that **Python** doesn't provide.
- It makes writing lists way easier and less verbose.
