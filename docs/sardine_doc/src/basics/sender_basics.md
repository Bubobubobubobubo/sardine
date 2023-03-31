# Basic of Senders


Previously, you might have noticed that we used `d()` without talking about its true nature!

`d()` is what we call a **Sender**. It is a special function that takes care of sending messages to your musical applications or audio tools. It also provides an interface to any pattern language that you&rsquo;d like to use. Basically, **senders are a gate to the outside world**.

**Senders** are numerous, and more can be created depending on your needs. By default, there are a couple of pre-declared ones that you will be using **all the time**:

-   `D()` and `d()`: **SuperDirt** sender.
-   `N()` and `n()`: **MIDI** notes.
-   `CC()` and `cc()`: **MIDI** control messages.
-   `PC()` and `pc()`: **MIDI** program changes.

These **senders** both exist in uppercase and lowercase. Why is that?

-   **UPPERCASE** players are the basic **senders**.
-   **lowercase** players are to be used with the shorthand notation: `Pa >> d('bd')`.

There are some additional **senders** that you can use to play with the **Ziffers** patterning language:

-   `ZD()` or `zd()`: the **Ziffers SuperDirt** senders.
-   `ZN()` or `zn()`: the **Ziffers MIDI** note senders.

The following example is highlighting the very basic usage of these **senders**:

```python
Pa >> n('C5 E5 G5', p=0.25) # playing a chord, one note every 1/4 of a beat.
Pb >> cc(ctrl=20, chan=0, value='rand*127') # sending a random MIDI control on ctrl 20, channel 0
Pc >> d('tabla tabla:2') # Playing audio samples of an indian tabla
```

