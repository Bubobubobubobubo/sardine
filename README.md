<h2 align="center"><b>Sardine</b>: ✨ Live Coding Library for Python ✨</h2>
<p align="center"><i>Python's missing algorave module. Simple/hackable live coding tool for modern Python (< 3.10)</i></p>

<p align="center">
  <img src=https://img.shields.io/discord/1029399269574193203 />
  <img src=https://img.shields.io/github/license/Bubobubobubobubo/sardine />
  <img src=https://img.shields.io/github/stars/Bubobubobubobubo/sardine />
</p>

<p align="center">
  <a href="https://discord.gg/aPgV7mSFZh">Discord</a> |
  <a href="https://sardine.raphaelforment.fr/">Website</a> |
  <a href="https://sardine.raphaelforment.fr/sardinopedia">Examples</a> |
  <a href="https://sardine.raphaelforment.fr/installation">Installation</a> |
  <a href="https://raphaelforment.fr/">Author</a>  |
  <a href="https://toplap.org/">About Live Coding</a>
  <br><br>
  <p align='center'>
    <a href="https://github.com/bubobubobubobubo/sardine/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=bubobubobubobubo/sardine" />
    </a>
  </p>
</p>

-----------

Sardine is a hacker-friendly Python library tailored for musical improvisation, algorithmic composition and much more. **Sardine** is transforming your typical **Python** interpreter into a music instrument that allows you to write melodic and rhythmic patterns of any kind and to map them to any electronic instrument: **MIDI**, **OSC** and/or **SuperCollider**. Using **Sardine**, you can:
- **improvise music freely on stage / in the studio / for your own enjoyment.**
    * **Sardine** can talk to any MIDI/OSC device and to the **SuperCollider** audio engine.
    * Bindings for **SuperDirt**, a well-known synthesis engine used by live coders around the world.
- **build complex and rich audio/visual installations using **MIDI** and **OSC** *I/O*.**
    * Attach **callbacks** to any OSC event, turn **Sardine** into a complex reactive toolbox.
    * Watch values as they change and propagate them to your musical patterns or code.
- **synchronise with other computers / other musical instruments**
    * **MIDI Clock** In and Out.
    * **Link Protocol** support.
- **make Python code time-aware**
    * Using temporal recursion, you can make any Python code time and tempo aware.
    * Launch any sync or async function precisely in time, with results falling back on time.
    * Hack your own **Senders** or **Receivers** to turn **Sardine** to your liking!

Broadly speaking, **Sardine** can be said to have three main features: 

* A **Clock** system capable of syncing itself to other computers instruments. This clock is organizing your **Python** code so that it can be time / tempo aware. Using temporal recursion, **Sardine** is pretty good at describing looping processes, musical patterns, etc... 
* A **Pattern language** that lives inside **Sardine**, designed to make musical sequences/patterns easier and fun to write. This is a language focused on generative/algorithmic music making, capable of matching your typical sequencer.
* **Senders** dispatching your patterns to variouts **outputs** (**MIDI**, **OSC**, **SuperCollider**). The list is centered around what I am using but adding a **Sender** is fairly easy to do. There is a plan to support more (**DMX**, other audio engines, etc..). 

## Contributions

There is no version number yet. We are still exploring what **Sardine** is and what it could be and you might see some things changing pretty quickly as a result. The first version, `0.0.1` is planned for release later this year. **Sardine** is looking for contributors! Anybody is welcome to contribute with code/documentation/thoughts, etc... You can contact the **Sardine** community directly on **Discord** or **PM** me if you have specific questions.

### Documenting Sardine

**Sardine** is a **Python** library that you learn to use as a musical instrument. For this reason, documentation is of paramount importance so that others can learn your cool tricks too :). The documentation resides in the `docs/` folder. It is a bunch of loosely organised Markdown files. You can contribute by editing these files and adding the missing bit of information you would like to see being updated or added.

The code source lives in the `cli/`, `fishery/` and `sardine/` folders. Most functions are already documented but the architecture of **Sardine** needs some time to get used to. You can contact me directly if you would like to learn more about it. There are no contributions rules for the moment, and I will explore each and every request that you would like to propose!

