# MacOS

The installation of **Sardine** on MacOS is pretty straightforward. You shouldn't encounter any particular
issue to make it work properly. I am developing **Sardine** on MacOS Ventura 13.0.1.

- **[PLEASE READ THE PRE-INSTALLATION PAGE BEFORE GOING FURTHER]**

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
    - You might have to add `sclang` to your path. To do so, copy `alias sclang="/Applications/SuperCollider.app/Contents/MacOS/sclang"`
      into your `.bashrc` or `.zshrc` in the `$HOME` directory.

## Installing Sardine

We will now proceed to the installation of Sardine.
Sardine is a Python library which is composed of two modules:
- **Sardine Core**: the Python library for live coding. Contains all the goodies.
- **Sardine**: an asynchronous Python interpreter **AND** integrated text editor.

```bash
python -m pip install sardine-system
```

If you want to install the development version, which may have more features
than the package on PyPI:

```bash
python -m pip install git+https://github.com/Bubobubobubobubo/sardine
```

**Note:**
  If you get an error when trying to install `python-rtmidi`,
  you can install the package manually using one of the following commands:
  - ```bash
    python -m pip install git+https://github.com/SpotlightKid/python-rtmidi.git@eb16ab3268b29b94cd2baa6bfc777f5cf5f908ba#egg=python-rtmidi
    ```
  - ```bash
    python -m pip install git+https://github.com/SpotlightKid/python-rtmidi.git#eb16ab3268b29b94cd2baa6bfc777f5cf5f908ba
    ```

## Installing Sardine Web

After Sardine is installed, you may choose to install the `sardine web` editor
with the following command:

```bash
python -m pip install sardine-web
```

More details are provided in the [Sardine Web](../editors/fishery.md) section.
