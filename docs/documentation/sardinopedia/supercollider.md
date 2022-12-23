## I - Sardine architecture

### A) General concept

If you have installed **Sardine** alongside **SuperCollider** and **SuperDirt**, you know that **Sardine** can boot its own **SuperDirt** session, etc.. If you haven't been *live coding* for several years, all of this might seem a little bit shady. We assume that things are working properly but we never detail the underlying infrastructure. Let's break it down:

- **Sardine** is doing the patterning and the scheduling. It is your top-level control and playing library.

- **SuperCollider** is the almighty audio engine.

- **SuperDirt** makes it easy to talk with **SuperCollider** in a live-coding context. It was originally designed to work hands-in-hands with [TidalCycles](https://tidalcycles.org) but of course you can hijack it which is what **Sardine** is doing.

**Sardine** is an independant piece of software. By design, it doesn't need **SuperCollider** to work. You can live an happy life by just sending OSC and MIDI using **Sardine** and never bridging with SC. However, if you do so, you will have to manage the connexion, to know how to deal with **SuperCollider**, etc... **Sardine** is not capable of emitting sound, it is more akin to a general sequencing brain that simplifies *input* and *output* communication for you during the improvisation process.

### B) Limitations

**Sardine** is not designed to handle the *digital signal processing* or the reality of scheduling / generating / controlling audio signals. **Python** is not an efficient or particularly optimised language (although things are changing a little bit nowadays..). **Sardine** is already performing a lot of weird tricks to stay afloat in an *almost real-time* context. It is not perfect but hopefully it will evolve and reach perfect stability.

**Sardine** was initially conceived in a music studio on a small laptop surrounded by audio equipment waiting for instructions. The idea was to delegate the audio processing to external hardware / softwares and to fully focus on live control / live sequencing. I would love to keep it that way because there is a lof of exciting solutions to explore for sound / audio design such as [Faust](https://faust.grame.fr/), [SuperCollider](https://supercollider.github.io/), [CSound](https://csound.com/), and [the list goes on and on](https://github.com/ciconia/awesome-music). You can emulate part of the signal logic with patterns but it will never be as good compared to what a **DSP** language can offer.

## II - Talking to SuperDirt / SuperCollider

If you choose to boot **SuperCollider** and **SuperDirt** alongside **Sardine** in your `sardine-config`, everything should fall in place. You have one main **Python** process handling everything for you so you don't have to start things manually. If you don't, you can always start **SuperCollider** yourself and manage two separate applications that will happily collaborate through the network.

### A) Interesting goodies

Let's assume that **SuperDirt** has started, and that you received the message saying that the audio engine is ready. You can now interact with the `SC()` object that represents your SC subprocess. Let's open up a VUMeter of our session:


```python
SC.meter()
```

All good, let's open some other windows as well.

```python
SC.meter()
SC.scope()
SC.freqscope()
```
You can open sound visualisation tools from the active **SuperCollider** session by running any of the commands above. Here is a short explanation of what each function do:

- `SC.meter()`: open a window showing VUMeters for each and every physical sound output.
- `SC.scope()`: open an oscilloscope to visualise every audio bus currently declared.
- `SC.freqscope()`: open a frequency spectrum visualizer of the global audio output.


### B) Sending code to SuperCollider

You can pipe code from your **Sardine** session to **SuperCollider**. Of course, this is not the best interface ever, but it can surely help to run short commands or to open an article from the **SuperCollider** documentation. To see **SuperDirt** documentation, you can type the following:

```python
SC.send('SuperDirt.help')
```

You will have to work without syntax highlighting. Copying and pasting short and useful commands is probably better if you are not an experienced **SuperCollider** user. There are no bindings for the **SuperCollider** server implemented into **Sardine**. Be sure that I am monitoring packages that are proposing solutions for this but I am not ready to write my own bindings for now. There is too much work to handle with **Sardine** itself before thinking about branching out.

If that's your thing, you can integrate small SC snippets in your patterns and sequence them with a decent enough time precision:

```python
# Generating a sinewave oscillating at 200hz.
SC.send('a={SinOsc.ar(200) * 0.1}; b = a.play;')

# Freing the synth
SC.send('b.free')
```