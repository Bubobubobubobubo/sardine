---
hide:
    - navigation
---


# Installation

**Sardine** is still experimental software and it has not yet been fully packaged. You can be up and running in minutes if everything is going fine but depending on your proficiency level with programming tools, you might have to spend some extra time configuring everything up for the first time. Most of the setup process is straightforward, only some extra details need to be taken care of in some cases that will be detailed along the way.

For those unfamiliar with *live-coding* tools, the installation is usually a two-step process:

- **[MANDATORY]** install/configuration of the library + text editor.

- **[RECOMMENDED]** install/configuration of the backend, the audio synthesis engine.

!!! warning "Installing from Pypi or from a package manager"
    Installation of **Sardine**  using Pypi is not yet available. Of course, **Sardine** will be added when it will be ready for everyone to use! The first planned milestone is the **0.1** version that should be released later this year (2022). Until then, you should install it manually! The first released version will greatly simplify the installation process.

## Library

!!! warning "For Windows Users only"
    **Sardine** is particularly tricky to install for users running Windows. This is due to the fact that **Sardine** depends on `rtmidi` (no wheels for Python 3.10) and `link` (relies on `pybind11`). These packages are bindings for existing C++ code used extensively for important chunks of the application. Without the proper development related tools, you might not be able to install **Sardine**. Please make sure that you install the following before proceeding with the installation:

    - [MSVC Build Tools](https://visualstudio.microsoft.com/fr/downloads/?q=build+tools) (*Microsoft Visual Studio Code Build Tools*).

    - [CMake](https://cmake.org/): a tool used to build, test and configure softwares.

**Sardine** can be installed like any other **Python** package using `pip`, the official package manager.


!!! note "Installing and updating a snake"
    1) Install [Python](https://www.python.org/) for your operating system (>=3.10). **Update if needed**!

    2) Open a terminal and type `python` or `python3` for extra safety. A prompt will open telling you what version you currently default to. Please make sure that you are running at least Python 3.10.

Being aware of your installed **Python** versions is of tremendous importance. You can have multiple versions of Python running on your system, some being required by your operating system, some being installed by other applications. They sometimes end up piling up. Find the command that will summon your **Python 3.10** installation (can be `python`, `python3`, `python3.10` depending on the system you are currently using)..

You can now safely proceed to download and install **Sardine**:

!!! note "Fishing a Sardine"

    1) Install [Git](https://git-scm.com/) or [download the project](https://github.com/Bubobubobubobubo/sardine#:~:text=with%20GitHub%20Desktop-,Download%20ZIP,-Latest%20commit) from GitHub and place it wherever you like!

    - If you take the *Git* route, clone Sardine ('`git clone https://github.com/Bubobubobubobubo/Sardine`'). 
    
    2) Using a `shell` or `cmd` (in admin-mode), run `python3 -m pip install -e` in the `sardine` folder.

    - If you are using Linux or MacOS, use `sudo` to install with the highest priviledges. This is usually not recommended but it can help with the installation of other **Sardine** components.

This command can take quite some time depending on your internet connexion, your computer specifications, etc... It will install **Sardine** as well as all the packages and libraries needed to get it running. This is likely the step where you will start noticing crashes, errors and sometimes some truly cryptic messages. Please watch carefully, and do not let an error pass without notice. This might result in a broken / uncomplete installation of **Sardine**.

Wait until the end of the process. To test if **Sardine** is installed properly, execute the following commands in your terminal:
```python3
python3 -m asyncio
from sardine import *
```

You should now see a big bright `SARDINE` written on your screen. Congratulations! This is the indication that **Sardine** was able to start!

## Audio engine

### Installation

!!! note "Installing SuperCollider and SuperDirt"
    - Refer to the [SuperDirt](https://github.com/musikinformatik/SuperDirt) installation guide for your platform. It will guide you through the installation of [SuperCollider](https://supercollider.github.io/) and **SuperDirt**. It is usually a three step process:
        * install [SuperCollider](https://supercollider.github.io/).
        * run `Quarks.install("SuperDirt")` in the SCIDE window.
        * run `SuperDirt.start` to start the engine.


**SuperDirt** is the *optional* but very much recommended synthesis engine for **Sardine**. As a matter of fact, **Sardine** was initially built as an alternative client for **SuperDirt**. It is a well-known freen and open source piece of software used by live coders. **SuperDirt** is mostly developed by Julian Rohrhuber, and intended to be used initially for [TidalCycles](https://tidalcycles.org/), a truly great live coding library. It is meant to be used via a simple message-based syntax converted into SuperDirt instructions that can trigger samples, synthesizers and do many other things, taking care of the finicky details. Note that it also means that your **Sardine** configuration will be valid and portable to **TidalCycles** alternatively.

### Configuration

**Sardine** is perfectly capable of booting both **SuperCollider** and **SuperDirt** by itself. However, this mechanism is disabled by default because I can't assume that you will have it installed and configured properly! You can turn on the *SuperDirt autoboot* feature by tweaking the configuration:

```shell
sardine-config --boot_superdirt True
```

For a first ride, please also turn on the `verbose` option that will help you monitor the output of **SuperCollider** directly from the same console:

```shell
sardine-config --verbose_superdirt True
```

It will help you to track if any mistake arise from the **SuperCollider** side (usually an audio mismatch between your input audio sampling frequency and your output audio sampling frequency). **Do remember to shut off this option later on!** It can be pretty invasive in your workspace. 

### Word of Caution

!!! warning "About the autoboot feature"
    **Sardine** will assume that `SuperCollider` (and more specifically `sclang`) is accessible on your `$PATH`. Everything should run just fine if you install it in the default folder for your platform. On some specific systems, you might need to locate the `sclang` executable and to add it to `$PATH`.

The autoboot feature can cause trouble among newcomers and unexperienced live-coders. There is a bazillion ways **SuperCollider** and **SuperDirt** can refuse to boot, crash or cease to function all of the sudden. Consult the troubleshot page for more information about frequent issues. I recommend to boot **SuperCollider** and **Sardine** separately for new users so that they can keep an eye on both sides. To do so, turn off the autoboot feature and start **Sardine** and **SuperCollider** separately, each in their own window. Type `SuperDirt.start` to start the latter manually from the SuperCollider side. To start anew if any error arise, type `Server.killAll` to restart **SuperCollider** to a blank slate.
 

## Code Editor

Pick the editor you prefer from the following list. All of them have been tested with Sardine! It's only a matter of preference.

!!! note "List of Sardine compatible text editors"
    - [VSCode](https://code.visualstudio.com/): great for everyone, from newcomers to exprienced users.
    - [Vim](https://www.vim.org/): fast, powerful, ubiquitous. Modal editor that requires some learning.
    - [Neovim](https://neovim.io/): the modernized version of Vim, configurable using Lua.
    - [Emacs](https://www.gnu.org/software/emacs/): Emacs is everything and can do anything.
    - [Jupyter Notebook](https://jupyter.org/): A data-science oriented tool that can support **Sardine**.


Working and making music with **Sardine** is usually done following the same method for all editors:

- 1) Opening a new blank `.py` file (no need to save).

- 2) Launching a terminal in the same coding environment

- 3) Sending lines of code from the code buffer to the terminal buffer.

If you already know how to do that for you, great! If you don't, please head to the configuration section where additional help concerning your editor of choice will be written.

## First swim

You should now have **Sardine** (and possibly **SuperDirt**) installed. You can fine-tune your **Sardine** installation by running the configuration client:

```
sardine-config
```

This is the main configuration tool for **Sardine**. We will come back to it later. If the command is not found or if nothing happens, **Sardine** might not be installed correctly. Please, worry and review the preceding steps! You might get a message saying that you have no configuration file. Take for a guarantee that **Sardine** is installed! This is perfectly normal. By default, there is no configuration file until it is created the first time you start **Sardine**.

Open a new interactive Sardine session by running `python3 -m fishery`. If everything is alright, some popup messages will be printed and you will be left on a prompt (`>>> `) waiting for your input:

```shell


░██████╗░█████╗░██████╗░██████╗░██╗███╗░░██╗███████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝
╚█████╗░███████║██████╔╝██║░░██║██║██╔██╗██║█████╗░░
░╚═══██╗██╔══██║██╔══██╗██║░░██║██║██║╚████║██╔══╝░░
██████╔╝██║░░██║██║░░██║██████╔╝██║██║░╚███║███████╗
╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝

Sardine is a MIDI/OSC sequencer made for live-coding
Play music, read the docs, contribute, and have fun!

BPM: 125, BEATS: 4 SC: [X], DEFERRED: [X] MIDI: MIDI Bus 1
Sardine is booting SCLang && SuperDirt...

...
...
...

>>> 
```

If you have opted to use the **SuperDirt** audio backend, you can start checking if everything is fine by playing a *clap* or a *kickdrum*: 

```python
S('cp').out()
```

If you want to play a note on your MIDI Synth, use this command instead:

```python
M().out()
```

If you hear the clap or the note you were expecting, you are good to go! Have fun!


## Trivia

### Alternative boot methods

So far, we've used the fast boot method for **Sardine**:

```python
python3 -m fishery
```

Note that you can boot **Sardine** manually in a two-step process:

1) `python3 -m asyncio`: start the asyncio REPL

2) `from sardine import **`: import **Sardine** library

