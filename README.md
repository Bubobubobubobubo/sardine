<h2 align="center">
  <b>Sardine</b>: ✨ Live Coding Library for Python ✨
</h2>
<p align="center"><i>
  Python's missing algorave module.
  Simple/hackable live coding tool for modern Python (3.10+)
</i></p>

<p align="center">
  <img src=https://img.shields.io/discord/1029399269574193203 />
  <img src=https://img.shields.io/github/license/Bubobubobubobubo/sardine />
  <img src=https://img.shields.io/github/stars/Bubobubobubobubo/sardine />
  <img src=https://img.shields.io/pypi/wheel/sardine-system>
  <img src=https://img.shields.io/pypi/v/sardine-system>
  <img src=https://img.shields.io/pypi/status/sardine-system>
</p>

<p align="center">
  <a href="https://discord.gg/aPgV7mSFZh">Discord</a> |
  <a href="https://sardine.raphaelforment.fr/">Website</a> |
  <a href="https://sardine.raphaelforment.fr/documentation/sardinopedia/introduction/">Examples</a> |
  <a href="https://sardine.raphaelforment.fr/technical/installation/">Installation</a> |
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

![Sardine algorave picture](pictures/sardine_intro_picture_repo.png)

Sardine is a hacker-friendly Python library tailored for musical improvisation,
algorithmic composition and much more. **Sardine** is transforming your typical
**Python** interpreter into a music instrument that allows you to write melodic
and rhythmic patterns of any kind and to map them to any electronic instrument:
**MIDI**, **OSC** and/or **SuperCollider**. Using **Sardine**, you can:

- **Improvise music freely on stage / in the studio / for your own enjoyment.**
  - **Sardine** can talk to any MIDI/OSC device and to the **SuperCollider**
    audio engine.
  - Bindings for **SuperDirt**, a well-known synthesis engine used by
    live coders around the world.
- **Build complex and rich audio/visual installations using MIDI and OSC *I/O*.**
  - Attach **callbacks** to any OSC event, turn **Sardine** into a complex
    reactive toolbox.
  - Watch values as they change and propagate them to your musical patterns or code.
- **Synchronise with other computers / other musical instruments**
  - **MIDI Clock** Out.
  - **Link Protocol** synchronization.
- **Make Python code time-aware**
  - Using temporal recursion, you can make any Python code time and tempo aware.
  - Launch any sync or async function precisely in time,
    with results falling back on time.
  - Hack your own **Senders** or **Receivers** to pattern whatever you see fit!

## Installation

In order to install Sardine, your system will require a recent version of Python (3.10+). We now support 3.11 versions as well. A more detailed installation guide can be found on [Sardine's website](https://sardine.raphaelforment.fr/technical/installation/).

1) Run: `python -m pip install --find-links https://thegamecracks.github.io/python-rtmidi-wheels/ sardine-system`.
    - the `--find-links` option is used as a temporary fix to the unavailability of some dependencies in the Pypi repositories for Python 3.10/3.11.
2) Install [SuperCollider](https://supercollider.github.io/) and [SuperDirt](https://github.com/musikinformatik/SuperDirt) for an additional supported audio backend.
3) Run `sardine-config` and configure Sardine to your liking following [this guide](https://sardine.raphaelforment.fr/configuration.html)
4) Install the text editor of your choice: VSCode, Neovim, Vim, Emacs, Jupyter Notebook, etc... There are many options you can pick from. They have all been tested with Sardine.

## Contributions

Sardine is currently in the early development phase. We are looking for contributors! Anybody is welcome to contribute with code / documentation / thoughts, etc... You can contact the **Sardine** community directly on **Discord** or **PM** me if you have specific questions.

### Documenting Sardine

**Sardine** is a **Python** library that you learn to use as a musical instrument. For this reason, documentation is of paramount importance so that others can learn your cool tricks too :). The documentation resides in the `docs/` folder. It is a bunch of loosely organised Markdown files. You can contribute by editing these files and adding the missing bit of information you would like to see being updated or added.

Source code is contained to the `sardine/` and `fishery/` folder. Most functions are already documented but the architecture of **Sardine** needs some time to get used to. You can contact me directly if you would like to learn more about it. There are no contributions rules for the moment, and I will explore each and every request that you would like to propose!
