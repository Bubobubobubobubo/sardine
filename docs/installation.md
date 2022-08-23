# Installation

Installing **Sardine** is a multi step process but shouldn't really take that long. The problem with Sardine and all programs in that same category is that they depend a lot on input/output for functioning properly. **Sardine** itself is really easy to install but you will need some additional tools to get the most out of it: *SuperCollider*, *SuperDirt*, *MIDI related packages*, etc...

**/!\\ There is no way to install Sardine from Pypi for now /!\\. It will be possible to do so once the project will reach its first milestone, the 0.1**.

## Python Package

### Installation

The installation process is fairly simple if you wish to install Sardine system-wide. You will need, that goes without saying, the most recent version of Python you can install on your OS. Some knowledge of the usage of a command prompt/shell is required but only for the installation / configuration process.

- install **Python** (3.9/3.10) and a suitable code editor ([VSCode](https://code.visualstudio.com/), [Vim](https://www.vim.org/)/[Neovim](https://neovim.io/), [Emacs](https://www.gnu.org/software/emacs/), etc..)
- run `git clone https://github.com/Bubobubobubobubo/Sardine` to download Sardine or fork it directly from Github before cloning.
- run `cd sardine && pip3 install -e .` (can also be `python` on some systems).
    * **You need to have `python` and `pip` already installed on your computer**.
- optionally (but recommended), run `pip3 install uvloop` (MacOS/Linux only). Install also everything related to `rtmidi` and `python-rtmidi`.

### First swim

You should now have Sardine installed and ready. Try to start the configuration tools: `sardine-config`, `sardine-config-superdirt`, `sardine-config-python`. If something is happening, it means that Sardine is installed. Now to test if **Sardine** is running properly!

- open a new interactive session using `python3 -m asyncio`
    * **/!\\ Make sure that you are running the asyncio REPL! /!\\**
    * **/!\\ The `IPython` REPL will not work. It is handling `asyncio` code differently. /!\\**

- import the library with `from sardine import *`

- Follow the prompt to connect to a MIDI Output. You will be able to configure the default MIDI interface later.

- Configure Sardine to your liking with `sardine-config`, `sardine-config-superdirt` and `sardine-config-python`.

- Read and try the examples provided in the `examples/` folder to learn more.

If you are hearing sound, everything is good and you can now have fun with **Sardine**! Let me know how the installation process went. Feel free to open an issue on GitHub or to send me a message directly if you encounter any problem.

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
    - run `%pip install -e "path/to/sardine"`, restart the kernel when `pip` is done installing.!
    - run `from sardine import *` and have fun!
* Emacs with the [python.el](https://github.com/emacs-mirror/emacs/blob/master/lisp/progmodes/python.el) plugin.

Any program or editor allowing you to run Python code dynamically can/should work as long as it is modern enough to support the `asyncio` REPL. I don't really want to develop my own code editor because the more mainstream ones offer so many features that it's hard to compete!

## Known bugs and issues

Please provide feedback on the installation process! I try to document it as much as I can but I lack feedback on the installation process on different systems, etc.. You might also have different use cases that I might not have anticipated.

* **[WINDOWS ONLY]**: `uvloop` does not work on Windows. Fortunately, you can still run **Sardine** but don't expect the tempo/BPM to be accurate. You will have to drastically slow down the clock for it to work (~20bpm is a safe value)! This might be linked to a different implementation of `asyncio` on Windows.

* **[LINUX/MACOS]**: `pip3 install` fails on `python-rtmidi build`. Its probably because the `libjack-dev` lib is missing. You can install it with `sudo apt-get install libjack-dev` on Debian based systems, with `brew` for MacOS, and with `pacman` for any other Arch-based system.

