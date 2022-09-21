# Installation

Installing **Sardine** is a multi step but straightforward process.

**Sardine** being a live-coding library, most of the install will be spent gathering coding-related tools. If you wish to play sound directly from **Sardine**, aim for a *full installation*. If you wish to use OSC/MIDI most of your time, skip the SuperCollider and SuperDirt section. Sardine is already quite capable by itself without needing **SuperCollider** but it's always better to have both!

!!! warning "Installing from Pypi or from a package manager"
    Installation of **Sardine**  using Pypi is not yet available. Of course, **Sardine** will be added when it will be ready for everyone to use! The first planned milestone is the **0.1** version that should be released later this year (2022). Until then, you should install it manually!

This page will help you to install Sardine and to configure it to your liking! You can skip some sections if you want to opt out of a specific feature! You can always come back later and install the missing bits.

## Install
### Python Package

!!! warning "For Windows Users only"
    **Sardine** is particularly tricky to install for users running Windows. This is due to the fact that **Sardine** depends on `rtmidi` (no wheels for Python 3.10) and `link` (relies on `pybind11`). These packages are bindings for existing C++ code used extensively for important chunks of the application. Without the proper development related tools, you might not be able to install **Sardine**. Please make sure that you install the following before proceeding with the installation:

    - [MSVC Build Tools](https://visualstudio.microsoft.com/fr/downloads/?q=build+tools) (*Microsoft Visual Studio Code Build Tools*)

    - [CMake](https://cmake.org/): a tool used to build, test and configure softwares.

    Adding to this, make sure that **you add Poetry to your PATH**. Follow [this official guide](https://docs.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)) teaching you how to do so. Here are some other tips I gathered while helping people install **Sardine**:

    - For the entirety of the installation process, please make sure that you run your command prompt **as an administrator**.

    - `python` might be named `py` on your system. Replace `python` by `py` in the submentioned commands.


**Sardine** is packaged using [Poetry](https://python-poetry.org/), a new Python packaging tool that helps fetching the dependencies in the right order and that bundles everything nicely in a virtual environment. That way, your basic Python system stays clean, Sardine staying confined where it should be, in a can!

!!! note "First steps"
    1) Install [Python](https://www.python.org/) for your operating system (>=3.9).

    1b) Update Python if needed! **Sardine** requires a very recent Python version.

    2) Install [Poetry](https://python-poetry.org/docs/) for your operating system.

You will now have to download and install **Sardine** itself:

!!! note "Fishing a Sardine"

    1) Install [Git](https://git-scm.com/) or [download the project](https://github.com/Bubobubobubobubo/sardine#:~:text=with%20GitHub%20Desktop-,Download%20ZIP,-Latest%20commit) from GitHub and place it wherever you like!

    - If you take the *Git* route, clone Sardine ('`git clone https://github.com/Bubobubobubobubo/Sardine`'). 
    
    2) Using a `shell` or `cmd` (in admin-mode), run `poetry install` in the `sardine` folder.

This last command will take quite some time. `Poetry` will install all the needed parts and package them properly. Wait until the end of the process. To test if **Sardine** is installed correctly, execute the following commands:

```python
poetry shell
python -m fishery # python3 on some Linux/MacOS Python distributions
```

You should now see a big bright `SARDINE` written in red on your screen. Congratulations! This is the indication that **Sardine** was able to boot correctly!

You should now think about installing a code editor for your future Sardine sessions. Pick the one you prefer from the following lists:

!!! note "List of Sardine compatible text editors"
    - [VSCode](https://code.visualstudio.com/): great for everyone, from newcomers to exprienced users.
    - [Vim](https://www.vim.org/): fast, powerful, ubiquitous. Modal editor that requires some learning.
    - [Neovim](https://neovim.io/): the modernized version of Vim, configurable using Lua.
    - [Emacs](https://www.gnu.org/software/emacs/): Emacs is everything and can do anything.
    - [Jupyter Notebook](https://jupyter.org/): A data-science oriented tool that can support **Sardine**.


!!! important
    **NOTE** : *All these editors have been tested!*

Check out the configuration page to learn more about configuring a specific editor for **Sardine**. 

### SuperCollider and SuperDirt

**SuperDirt** is the *optional* sound engine recommended for **Sardine**. As a matter of fact, **Sardine** was initially built as an alternative client for **SuperDirt**. It is a well-known audio engine used by live coders, developed by Julian Rohrhuber for [TidalCycles](https://tidalcycles.org/). It is meant to be used via a simple message-based syntax converted into SuperDirt instructions that can trigger samples, synthesizers and do many other things, taking care of the finicky details. I'm not the author of **SuperDirt**, I will let the authors themselves speak for their tool:

!!! note "Installing SuperCollider and SuperDirt"
    - Refer to the [SuperDirt](https://github.com/musikinformatik/SuperDirt) installation guide for your platform. It will guide you through the installation of [SuperCollider](https://supercollider.github.io/) and **SuperDirt**. It is usually a three step process:
        * install [SuperCollider](https://supercollider.github.io/).
        * run `Quarks.install("SuperDirt")` in the SCIDE window.
        * run `SuperDirt.start` to start the engine.

**Sardine** is perfectly capable of booting SuperCollider and SuperDirt by itself. However, this mechanism is disabled by default because I can't assume that you will have it installed and configured properly! You can turn on the *SuperDirt autoboot* feature by tweaking the configuration:

```shell
sardine-config --boot_superdirt True
```

If you want SuperDirt to be particularly verbose (useful for debugging), turn on the `stdout` optional output:

```shell
sardine-config --verbose_superdirt True
```

!!! warning "About the autoboot feature"
    **Sardine** will assume that `SuperCollider` (and more specifically `sclang`) is accessible on your `$PATH`. Everything should run just fine if you install it in the default folder for your platform. On some specific systems, you might need to locate the `sclang` executable and to add it to `$PATH`.

The autoboot feature can cause trouble among newcomers and unexperienced live-coders. There is a bazillion ways **SuperCollider** and **SuperDirt** can refuse to boot, crash or cease to function all of the sudden. Consult the troubleshot page for more information about frequent issues. I recommend to boot SuperCollider and Sardine separately for new users so that they can keep an eye on both sides.

### First swim

You should now have Sardine (and possibly **SuperDirt**) installed. If you are still in your `poetry shell`, try the following command:

```
sardine-config
```

This is the main configuration tool for **Sardine**. We will come back to it later. If the command is not found or if nothing happens, **Sardine** might not be installed correctly. You might get a message saying that you have no configuration file. Take for a guarantee that **Sardine** is installed! This is perfectly normal. Feel free to email me directly or to open an issue on GitHub documenting your problem.

Open a new interactive Sardine session by running `python3 -m fishery`. If everything is alright, some popup messages will be printed and you will be left on a prompt (`>>> `) waiting for your input:

```shell
░██████╗░█████╗░██████╗░██████╗░██╗███╗░░██╗███████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝
╚█████╗░███████║██████╔╝██║░░██║██║██╔██╗██║█████╗░░
░╚═══██╗██╔══██║██╔══██╗██║░░██║██║██║╚████║██╔══╝░░
██████╔╝██║░░██║██║░░██║██████╔╝██║██║░╚███║███████╗
╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝

Sardine is a MIDI/OSC sequencer made for live-coding.
Play music, read the docs, contribute, and have fun!

[1/3] Configuration folder
      - /Users/bubo/Library/Application Support/Sardine
[2/3] Reading configuration file
      - /Users/bubo/Library/Application Support/Sardine/config.json
[3/3] Sardine is swimming!

Preemptive: Killing all SC instances...
There was no SC process to kill...

Starting SCLang && SuperDirt
No user provided configuration file found...
>>> 
```

!!! note "First sound with Sardine"
    If **SuperDirt** is on, run the following command:

    ```python
    S('cp').out()
    ```

    You should hear a clap. You are done!

!!! note "First MIDI note with Sardine"
    If **Sardine** is running without any sound engine, run the following command:
    ```python
    M().out()
    ```

    This should send a middle C MIDI note (C5) to the newly created `Sardine` MIDI port.


## Things to know

### Boot methods

So far, we've used the fast boot method for **Sardine**:

```python
python3 -m fishery
```

Note that you can boot **Sardine** manually in a two-step process:

1) `python3 -m asyncio`: start the asyncio REPL

2) `from sardine import **`: import **Sardine** library


### Code-editing

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

### Known bugs and issues

Please provide feedback on the installation process! I try to document it as much as I can but I lack feedback on the installation process on different systems, etc.. You might also have different use cases that I might not have anticipated.

* **[WINDOWS ONLY]**: `uvloop` does not work on Windows. Fortunately, you can still run **Sardine** but don't expect the tempo/BPM to be accurate. You will have to drastically slow down the clock for it to work (~20bpm is a safe value)! This might be linked to a different implementation of `asyncio` on Windows.

* **[LINUX/MACOS]**: `poetry install` fails on `python-rtmidi build`. Its probably because the `libjack-dev` lib is missing. You can install it with `sudo apt-get install libjack-dev` on Debian based systems, with `brew` for MacOS, and with `pacman` for any other Arch-based system.
