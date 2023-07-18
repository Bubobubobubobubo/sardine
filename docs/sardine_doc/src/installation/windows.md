# Windows

Installing Sardine on Windows is more difficult than installing it on Linux/MacOS. Don't blame me, blame Windows for not providing the right tools. Microsoft are doing everything they can to prevent you from having fun. Why aren't you running Excel or Word already?


- **PLEASE READ THE PRE-INSTALLATION PAGE BEFORE GOING FURTHER**.
- Install the [Windows Terminal](https://github.com/microsoft/terminal), the modern terminal for Windows, made by Microsoft.
- Install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) for MIDI connectivity. This will allow you to play with any synthesizer.


### Preparing your environment

The installation of Sardine takes place in several steps and has some prerequisites.
You will have to install all the development environment that will allow you to live code comfortably.
You will of course have to install Python but also make sure you have SuperCollider, the audio engine
used by the application. You will also have to install some tools that will allow you to compile the application.

1) Install the latest [Python](https://www.python.org/) version for your OS (currently 3.11). 
   - **Sardine** will not work with a Python older than 3.10.
   - Be careful with distribution provided Python versions! They might be incomplete!
   - Install [Pyenv](https://github.com/pyenv/pyenv) or use [virtual environments](https://docs.python.org/3/library/venv.html) 
     to keep everything nice and tidy!

2) Install [SuperCollider](https://supercollider.github.io/), the default audio backend used by **Sardine**.
    -   Once this step is over, open **SCIDE** (or click on the **SuperCollider** icon) and type:
    ```Quarks.install("SuperDirt")```
    - Press **Shift + Enter** and wait for the installation to be done! Close **SuperCollider** when done.
    - **Optional:** You can also install [sc3plugins](https://github.com/supercollider/sc3-plugins) to get more audio effects and synthesizers!


## Installing Sardine

We will now proceed to the installation of Sardine. Sardine is a Python library which is composed of two modules: 
- **Sardine Core**: the Python library for live coding. Contains all the goodies.
- **Sardine**: an asynchronous Python interpreter **AND** integrated text editor.


Install the development version (**recommanded**).
```python
git clone https://github.com/Bubobubobubobubo/sardine
cd sardine && python -m pip install --editable .
```

**Note**: the `--editable` flag is optional. You can remove it if you are not planning to modify **Sardine**!

**Note 2:** If you get an error when trying to install `python-rtmidi`, you can try to get it from these sources:
  - `python -m pip install git+https://github.com/SpotlightKid/python-rtmidi.git@eb16ab3268b29b94cd2baa6bfc777f5cf5f908ba#egg=python-rtmidi`
  - `python -m pip install git+https://github.com/SpotlightKid/python-rtmidi.git#eb16ab3268b29b94cd2baa6bfc777f5cf5f908ba`
