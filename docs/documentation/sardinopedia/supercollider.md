## SuperCollider interface

### The SC Object
Note: the SC object is only available when you boot SuperCollider / SuperDirt from Sardine. (See the Install page for details.)

```python
SC.meter()
```
If `boot=True` in your `sardine-config`, **SuperCollider** and **SuperDirt** are booted as a subprocess when **Sardine** is initialized. The `SC` object acts as an interface if you ever need to talk directly with **SuperCollider**.

### VUmeter, Scope, FreqScope

```python
SC.meter()
SC.scope()
SC.freqscope()
```
You can open sound visualisation tools from the active **SuperCollider** session by running any of the commands above. Here is a short explanation of what each function do:

- `SC.meter()`: open a window showing VUMeters for each and every physical sound output.
- `SC.scope()`: open an oscilloscope to visualise every audio bus currently declared.
- `SC.freqscope()`: open a frequency spectrum visualizer of the global audio output.

### Sending code to SuperCollider

```python
# Generating a sinewave oscillating at 200hz.
SC.send('a={SinOsc.ar(200) * 0.1}; b = a.play;')

# Freing the synth
SC.send('b.free')
```
You can pipe code from your **Sardine** session to **SuperCollider**. Of course, this is not the best interface ever, but it can surely help to run short commands or to open an article from the **SuperCollider** documentation. To see **SuperDirt** documentation, you can type the following:

```python
SC.send('SuperDirt.help')
```

You will have to work without syntax highlighting. Copying and pasting short and useful commands is probably better if you are not an experienced **SuperCollider** user.
