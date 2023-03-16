# OSC

**Sardine** is capable of receiving and sending custom **OSC** messages.
Obviously, this should be configured manually on your side. I am only
providing the basic tools do to so without encountering any hurdle!
Configuring **OSC** is prone to errors and has always been a very painful
activity that computer musicians like to do for some reason.

### Sending OSC

```python
output_one = OSCHandler(
    ip="127.0.0.1", port=12345,
    name="A first test connexion",
    ahead_amount=0.0, loop=osc_loop, # The default OSC loop, don't ask why!
)
bowl.add_handler(output_one)

# Look who's here, the send functions as usual
one = output_one.send
two = output_two.send
```

You can now use the methods one and two as OSC senders just like `D()` or `N()`.

```python
@swim
def one_two_test(p=0.5, i=0):
    """This is a dummy swimming function sending OSC."""
    one('random/address', value='1 2 3')
    again(one_two_test, p=0.5, i=i+1)
```

If you'd like, you can also make a `Player` out of it by using the 
following technique:

```python
def osc_player(*args, **kwargs):
    """Partial function to add a new OSC player :)"""
    return play(
        output_one,
        output_one.send,
        *args, **kwargs
    )
Pa >> osc_player('random/address', value='1 2 3')
```

You are now able to send **OSC** messages just like if they were patterns.
It means that you can use the **Sardine** pattern syntax to compose complex
algorithmic sequences of OSC messages. Note that you can also pattern the
address, making it a super fun/powerful way to explore your **OSC** bindings.

### Receiving OSC

You can receive and track incoming **OSC** values coming from your controllers or devices. In fact, you can even attach callbacks to incoming **OSC** messages and turn **Sardine** into a soundbox so let&rsquo;s do it!

```python
# Making a new OSC-In Handler
listener = OSCInHandler(
    ip="127.0.0.1",
    port=44444,
    name="Listener",
    loop=osc_loop
)

# Adding the listener to the bowl
bowl.add_handler(listener)

def funny_sound():
    D('bip', shape=0.9, room=0.9)

listener.attach('/bip/', funny_sound)
```

That's everything you need! In the above example, we are declaring a new
`OSCInHandler` object that maps to a given **port** on the given **IP** 
address (with `127.0.0.1` being `localhost`). All we have to do next is
to map a function to every message being received at that address and poof.
We now have a working soundbox. Let&rsquo;s break this down and take a look
at all the features you can do when receiving OSC.

There are three methods you can call on your `OSCInHandler` object:
- `.attach(address: str, function: Callable, watch: bool)` : attach a callback to a given address. It must be a function. Additionally, you can set watch to `True` (`False` by default) to also run the `.watch` method automatically afterhands.
- `.watch(address: str)` : give an address. The object will track the last received value on that address. If nothing has been received yet, it will return `None` instead of crashing \o/.
- `.get(address)` : retrieve the last received value to that address. You must have used `.watch()` before to register this address to be watched. Otherwise, you will get nothing.



