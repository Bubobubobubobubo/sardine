# Addresses

- Addresses are names containing one or multiple  `/` separators just like any OSC address.
- If using the `send_raw` function in conjunction with OSC, the syntax differs:
  - prepend your address with an additional `/`.

```python
O("an/address another/address", value=1, other_value=2)
```



