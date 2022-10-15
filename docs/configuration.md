---
hide:
    - navigation
---

# Configuration

This page will help you to learn how to configure **Sardine** to your desire. You will soon learn that **Sardine** is really modular in nature. You can toggle on and off certain features, you can pre-configure many things and fine-tune to be up and ready for your next sessions, etc...

## Code Editors for fishing

You can use `Sardine` directly from the Python interpreter. There is nothing wrong about it, but you will be pretty limited in what you can do. It is sometimes enough to run quick sound/MIDI tests. After a while, you will figure out that working this way is fairly cumbersome and you will likely be searching for a better text editor. **Sardine** code can become quite verbose when dealing with complex *swimming* functions. As you might have guessed already, there is no `Sardine` plugin for **VSCode**, **Atom** or any popular code editor **yet**. However, **Sardine** is just Python and there are great plugins to deal with interactive Python code. Here are a few things you can try.

### Vim / Neovim

[Neovim](https://github.com/neovim/neovim) (and by extension [Vim](https://github.com/vim/vim)) is the editor I currently use on stage but the target audience for this software is mostly developers, old Unix gurus and command-line users. **Vim** is a modal text editor with multiple modes for editing, jumping around and composing text. It can be extended using plugins and can be augmented and tweaked to your liking. Quite powerful, but quite hard and required some learning to be proficient. The process for working with **Sardine** from **Neovim** is pretty straightforward:

- 1) install the [slime](https://github.com/jpalardy/vim-slime) plugin.
- 2) split your workspace in two vertical (`:vs`) or horizontal (`:sp`) panes.
- 3) open up a `:terminal` in one of them and run `python3 -m fishery`.
- 4) work in the other one and use `C-cC-c` to send code from one side to the other.

### VSCode

[VSCode](https://code.visualstudio.com/) is a powerful and all-devouring code editor developed by Microsoft. It is the most widely spread code editor out there, with millions of users. **VSCode** is more than capable of handling **Sardine** sessions and there are multiple ways to configure everything for **Sardine**.

#### Native Python terminal (recommended)

- 1) install the `Python` support for VSCode (usually proposed whenever you open a Python file).
- 2) open the configuration menu and search for `Python launch args`. Click on `Modify in settings.json`
- 3) write the following:
```json
    "python.terminal.launchArgs": [
        "-m",
        "asyncio"
    ],
```
- 4) You are done!

To start a new **Sardine** session, open any `.py` file and type:
```python3
from sardine import *
```

Press `Shift+Enter` and wait for the new Python terminal to show up. You can now start typing **Sardine** code, you are good to go! 

#### Jupyter Notebook

and there might be more than one way to do it. I will present you one way of doing it, using the [Jupyter](https://jupyter.org) extension.

- install **VSCode** and the **Jupyter Notebook** plugin. To do so, open the Extensions pane on the left (it looks like crates) and search for the extension name. Click install and wait a moment.
- Create a new `.ipynb` notebook either by yourself or by using the plugin-backed command.
- Make sure that you are using **the right Python version** as your kernel (3.10).
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
From now on, **Sardine** is installed in the notebook you just created. You can write cells containing your **Sardine** code, which makes it easy to work with. Some plugins allow you to write and manage cells directly using source code, using symbols akin to comment strings. More on this later!

### Emacs

The venerable [Emacs](https://www.gnu.org/software/emacs/) is of course able to do what the other ones are doing and it is particularly well suited for the task of running interpreted code. Please use the [python.el](https://github.com/emacs-mirror/emacs/blob/master/lisp/progmodes/python.el) plugin. This mode will allow you to pipe easily your code from a text buffer to a running interpeter. The plugin is adding quality-of-life features for working with **Python** in general but also makes working with a **REPL** much easier and much more convenient. If you are new to the vast world of Emacs, it is probably worthwhile to take a look at [Doom Emacs](https://github.com/doomemacs/doomemacs) or [Spacemacs](https://www.spacemacs.org/), both being really great distributions of plugins. I will not dive into more details, as Emacs users are generally able to figure out their prefered way of working by themselves :)

## Configuration

**Sardine** is relying on a configuration folder that will be silently created the first time you open it. The path leading to the configuration folder can be printed out by typing `print_config()`. This command will also print out the content of your main configuration file. How practical! 

There are three files you can tweak to configure **Sardine**:

- `config.json`: main **Sardine** configuration file.
- `default_superdirt.scd`: **SuperDirt** configuration file.
- `user_configuration.py`: Python code runned everytime you boot **Sardine** (facultative).

There is also a `synths` folder made to store synthesis definitions (synthesizers, effects). This system is currently broken but be aware of its existence.

- `synths` folder: store new synthesizers written with **SuperCollider**.

### Sardine

The `config.json` file will allow you to finetune **Sardine** by choosing a default MIDI port, a default PPQN (*pulses per quarter note*, used for the MIDI Clock), and BPM (*beats per minute*), etc... You can edit it manually but you don't have too. There is a tool made for that, installed by default on your `$PATH`. Access it by typing `sardine-config`.

![Configuration tool](images/config_tool.png)

You can use it as a regular command-line tool, by following instructions and feeding the right arguments. For instance, if you would like to change your default BPM to 140, write the following:

```bash
sardine-config --bpm 140
```

To select a default MIDI port without having to choose everytime you boot Sardine, enter something similar, matching the MIDI Port name with a port available on your computer:

```bash
sardine-config --midi "MIDI Bus 1"
```

### SuperDirt

The `default_superdirt.scd` is... your default `SuperDirt` configuration. You must edit it manually if you are willing to load more audio samples, change your audio outputs or add anything that you need on the **SuperCollider** side. The `synths` folder is a repository for your `SynthDefs` file. Each synthesizer should be saved in its own file and will be loaded automatically at boot time. 

!!! important "How to tweak the SuperDirt file"
	The [SuperDirt](https://github.com/musikinformatik/SuperDirt) repository is a good place to start, especially the `hacks/` folder that will teach you how to edit and configure *SuperDirt* to your liking. **SuperDirt** was initially conceived for TidalCycles, and there is more documentation about Tidal and its usage than documentation about anything **Sardine**.

!!! note "Editing the SuperDirt file directly from the terminal"
	If you know how to work with text files from the terminal using `vim` or `nano`, there is a command available to open the default *SuperDirt* configuration file: `sardine-config-superdirt`. It will open up the file using `$EDITOR`. Be sure to configure it beforehand!

Here is an example showing of how to load more audio samples to play with:

```supercollider
(
s.reboot {
	s.options.numBuffers = 1024 * 256;
	s.options.memSize = 8192 * 32;
	s.options.numWireBufs = 128;
	s.options.maxNodes = 1024 * 32;
	s.options.numOutputBusChannels = 2;
	s.options.numInputBusChannels = 2;
	s.waitForBoot {
		~dirt = SuperDirt(2, s);
		~dirt.loadSoundFiles;
		~dirt.loadSoundFiles("/Users/bubo/Dropbox/MUSIQUE/LIVE_SMC/DRUMS/*");
		s.sync;
		~dirt.start(57120, 0 ! 12);
		(
			~d1 = ~dirt.orbits[0]; ~d2 = ~dirt.orbits[1]; ~d3 = ~dirt.orbits[2];
			~d4 = ~dirt.orbits[3]; ~d5 = ~dirt.orbits[4]; ~d6 = ~dirt.orbits[5];
			~d7 = ~dirt.orbits[6]; ~d8 = ~dirt.orbits[7]; ~d9 = ~dirt.orbits[8];
			~d10 = ~dirt.orbits[9]; ~d11 = ~dirt.orbits[10]; ~d12 = ~dirt.orbits[11];
		);
	};
	s.latency = 0.3;
};
)
```

Many people already use the **SuperDirt** audio backend for live-coding, more specifically people working with [TidalCycles](https://tidalcycles.org). You will find a lot of configuration tips, tools and extensions by searching in the TOPLAP / Tidal communities forums and chats.

### Python

The last configuration file is named `user_configuration.py`. It is not created by default. It must be added manually if you wish to use this feature. All the code placed in this file will be imported by default everytime you boot **Sardine**. It is an incredibely useful feature to automate some things:

* functions, aliases, classes, **OSC** and **MIDI** connexions.
* Starting some musical code, aka 'art installation' mode for museums, openings, etc... You will be able to manually take over after init if you ever wished to change parameters.

!!! warning "Do not break Sardine"
	Make sure not to override any of the defaults. This file will run **after** init, and can override basic Sardine functionalities if you are not careful enough.

