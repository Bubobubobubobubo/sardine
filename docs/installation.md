# Installation

Installing **Sardine** is a multi step process but shouldn't really take that long. The problem with Sardine -- as is with live-coding tools in general -- is that they depend on many inputs and outputs and on additional interlinked softwares for functioning properly. **Sardine** itself is really easy to install but you will need some additional tools to get the most out of it: 
- *SuperCollider* and/or *SuperDirt* for direct sound output
- *MIDI related packages* and *MIDI capable softwares* (very OS specific)

Installation of **Sardine**  using Pypi is not yet available. Of course, **Sardine** will be added when it will be ready for general public usage ! The first planned milestone is the **0.1** version, that should be released later this year. Until then, you should install it manually!

This page will help you to install Sardine and to configure it to your liking! You can skip some sections if you don't need a specific functionality! You can always come back later and install the missing bits.

## Python Package

**Sardine** can be installed using [Poetry](https://python-poetry.org/), a new Python packaging tool that helps fetching the dependencies in the right order and that packages everything automatically in a virtual environment. That way, your basic Python system stays clean, Sardine staying confined where it should be, in a can!

1) Install [Python](https://www.python.org/) for your operating system (>=3.9).
    - If you already have Python, update it! You might have an outdated version of Python. Sardine uses many features recently introduced to Python (asyncio REPL, typing, etc...).
2) Install [Poetry](https://python-poetry.org/docs/) for your operating system.

You will now have to download and install **Sardine** itself:

1) Install [Git](https://git-scm.com/) or [download the project](https://github.com/Bubobubobubobubo/sardine#:~:text=with%20GitHub%20Desktop-,Download%20ZIP,-Latest%20commit) from GitHub and place it wherever you like!
    - Alternatively, clone Sardine with Git('`git clone https://github.com/Bubobubobubobubo/Sardine`').
2) Using a `shell` or `cmd` (in admin-mode), run `poetry install` in the `sardine` folder.

This command will take quite some time. `Poetry` will install all the needed parts and package them properly. Wait until the end of the process. To test if **Sardine** is installed correctly, execute the following commands:

```python
poetry shell
python3 -m fishery
```

You should now see a big bright `SARDINE` written in red on your screen. Congratulations! 

You should now think about installing a code editor for your future Sardine sessions:
- [VSCode](https://code.visualstudio.com/)
- [Vim](https://www.vim.org/)
- [Neovim](https://neovim.io/)
- [Emacs](https://www.gnu.org/software/emacs/)
- [Jupyter Notebook](https://jupyter.org/)

**NOTE** : *All these editors have been tested with Sardine!*

If you just want to test **Sardine** without installing a code editor, you can always use the *inline editor* shipped with **Sardine** but note that rhythms might not always be exactly right on time!

### First swim

You should now have Sardine installed and ready. If you are still in your `poetry shell`, try the following command: `sardine-config`. This is the main configuration tool for **Sardine**. We will come back to it later. If the command is not found or if nothing happens, **Sardine** might not be installed correctly. Feel free to email me directly or to open an issue on GitHub documenting your problem.

Open a new interactive Sardine session by running `python3 -m fishery`. You will not be allowed to played immediately. **Sardine** is built around the usage of a MIDI

open a new interactive session using `python3 -m asyncio`
    * **/!\\ Make sure that you are running the asyncio REPL! /!\\**
    * **/!\\ The `IPython` REPL will not work. It is handling `asyncio` code differently. /!\\**

- import the library with `from sardine import *`

- Follow the prompt to connect to a MIDI Output. You will be able to configure the default MIDI interface later.

- Configure Sardine to your liking with `sardine-config`, `sardine-config-superdirt` and `sardine-config-python`.

- Read and try the examples provided in the `examples/` folder to learn more.

If you are hearing sound, everything is good and you can now have fun with **Sardine**! Let me know how the installation process went. Feel free to open an issue on GitHub or to send me a message directly if you encounter any problem.

### Faster method

There is now an even faster method to run **Sardine** using only one command:

```python
python3 -m fishery
```

If you would like to edit **Sardine** code directly from the command prompt, be sure to try out the *unstable* inline editor ([ptpython](https://github.com/prompt-toolkit/ptpython)). I have noticed some timing issues while using it but it is still a fun way to run some examples and to learn **Sardine**. In order to activate it, run the following command from the command line:

```bash
sardine-config --inline_editor True
```

## SuperDirt

SuperDirt is a nice to have but **optional** output for Sardine. It is a well-known audio engine used by live coders, originally developed by Julian Rohrhuber for [TidalCycles](https://tidalcycles.org/). It provides a simple message-based syntax to speak with SuperCollider, to trigger samples, synthesizers and many other things.

- Refer to the [SuperDirt](https://github.com/musikinformatik/SuperDirt) installation guide for your platform. It will guide you through the installation of [SuperCollider](https://supercollider.github.io/) and **SuperDirt** for your favorite OS. It is usually a three step process:
    * install [SuperCollider](https://supercollider.github.io/).
    * run `Quarks.install("SuperDirt")` in the SCIDE window.
    * run `SuperDirt.start` to start the engine.

We will assume that you already have some experience dealing with SuperDirt in order to focus more on explaining how **Sardine** works. **Sardine** will assume that `SuperCollider` (and more specifically `sclang`) is accessible on your `$PATH`. Everything should run just fine if you install it in the default folder for your platform. **Sardine** will automatically try to boot a **SuperCollider** server and the `SuperDirt` audio engine as soon as you import the library.

This might cause some trouble to newcomers and unexperienced live coders because there are a bazillion ways **SuperCollider** and **SuperDirt** can refuse to boot all of the sudden. See the troubleshot page to fix any issue you might encounter if you don't hear any sound.

## Code-editing with Sardine

You can use `Sardine` directly from the Python interpreter. There is nothing wrong about it, but you will be pretty limited in what you can do. It is sometimes enough to run quick tests. After a while, you will figure out that working this way is fairly cumbersome and you will likely be searching for a better text editor. **Sardine** code can become quite verbose when dealing with complex *swimming* functions.

As you might have guessed already, there is no `Sardine` plugin for VSCode, Atom or any popular code editor. However, **Sardine** is Python and there are great plugins to deal with interactive code. Here are a few things you can try:

- [Vim](https://github.com/vim/vim) or [Neovim](https://github.com/neovim/neovim) [slime](https://github.com/jpalardy/vim-slime) plugin. This plugin gives you the ability to `pipe` strings from a text buffer to another (from your code to another buffer containing the python interpreter).
* VSCode with the [Jupyter Notebook](https://jupyter.org/) extension
    - install VSCode and the Jupyter Notebook plugin. Create a new `.ipynb` notebook.
    - make sure that you are using the right Python version as your kernel (3.9 / 3.10).
    - run:
    ```python
      import sys;
      !{sys.executable} -m pip install "/path/to/sardine"
    ```
    - restart the kernel and run:
    ```python
    import sys
    sys.path.insert(0, '/path/to/sardine')
    from sardine import *
    ```
* Emacs with the [python.el](https://github.com/emacs-mirror/emacs/blob/master/lisp/progmodes/python.el) plugin.

Any program or editor allowing you to run Python code dynamically can/should work as long as it is modern enough to support the `asyncio` REPL. I don't really want to develop my own code editor because the more mainstream ones offer so many features that it's hard to compete!

## Known bugs and issues

Please provide feedback on the installation process! I try to document it as much as I can but I lack feedback on the installation process on different systems, etc.. You might also have different use cases that I might not have anticipated.

* **[WINDOWS ONLY]**: `uvloop` does not work on Windows. Fortunately, you can still run **Sardine** but don't expect the tempo/BPM to be accurate. You will have to drastically slow down the clock for it to work (~20bpm is a safe value)! This might be linked to a different implementation of `asyncio` on Windows.

* **[LINUX/MACOS]**: `pip3 install` fails on `python-rtmidi build`. Its probably because the `libjack-dev` lib is missing. You can install it with `sudo apt-get install libjack-dev` on Debian based systems, with `brew` for MacOS, and with `pacman` for any other Arch-based system.

