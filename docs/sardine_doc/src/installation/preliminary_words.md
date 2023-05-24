# Preliminary words

## About your Python version

- Being aware of your installed **Python** versions is of tremendous importance! 
  - You can have multiple versions of **Python** running on the same system.
  - **Always** prefer a version of Python that you installed yourself (*e.g.* [Pyenv](https://github.com/pyenv/pyenv)).
  - **Be careful** with aliases. On Windows, people often have **python** and **py** living side by side. **They are not the same installation of Python**.

## Find the right command

- Find the command that will summon your **Python 3.10** or **Python 3.11** installation 
  (can be `python`, `python3`, `python3.10`, `python3.11` or `py` depending on the system you are currently using). 
  Now, stick to it! You don't want to scatter files everywhere on your computer or to do a multi-version install.
- Don't let any error happen un-noticed! If you see an error, then there must be an error! Consider it seriously! Most people assume that seing errors is normal as long as nothing crashes. It may not be that bad but a missing package means a broken **Sardine**!
- As funny as it may sound, I am not the owner of the `sardine` package on Pypi. **Sardine** is named `sardine-system`. Some people sometimes end up installing a totally unrelated tool!

## A Modular Architecture

- Sardine is a **very** flexible software. It can be hard to install for that reason.
- It is designed to mold around your system, not to be all bells and whistles.
- You probably don't need everything but you need to understand the architecture:
  - **Sardine web** is an optional text editor for **Sardine** crafted by us!
  - **Sardine** is an asynchronous Python interpreter firing up the **Sardine** library.
  - **Sardine Core** is the library for live coding in Python itself.
    - it opens / close and manage MIDI ports.
    - it communicates over the network through the OSC protocol.
    - it create musical code using a powerful patterning engine.

## About the different Sardine versions

- **Sardine** is experimental software. Always install from GitHub if possible!
- The **Pipy** version is always lagging behind. We update it at every major version.
