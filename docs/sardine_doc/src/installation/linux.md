# Linux

**Sardine** feels right at home on Linux. Its modular architecture is like a fish in water on a Unix system.
Sardine makes extensive use of the terminal, another of the strengths of Unix systems.

- **[PLEASE READ THE PRE-INSTALLATION PAGE BEFORE GOING FURTHER]**

### Preparing your environment

The installation of Sardine takes place in several steps and has some prerequisites.
You will have to install all the development environment that will allow you to live code comfortably.
You will of course have to install Python but also make sure you have SuperCollider, the audio engine
used by the application. If you want to use Fishery Web, our integrated text editor, you will also have
to install some tools that will allow you to compile the application.

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

3) Install [NodeJS](https://nodejs.org/en) and [Yarn](https://yarnpkg.com/) to be able to build the website.
    - NodeJS is a package manager for JavaScript. Yarn is also... a package manager for JavaScript.
    - If you are installing the package from GitHub, the build process for the text editor will start automatically.

## Installing Sardine

We will now proceed to the installation of Sardine. Sardine is a Python library which is composed of two modules: 
- **Sardine**: the Python library for live coding. Contains all the goodies.
- **Fishery**: an asynchronous Python interpreter **AND** integrated text editor.


Install the development version (**recommanded**).
```python
git clone https://github.com/Bubobubobubobubo/sardine
cd sardine && python -m pip install --find-links https://thegamecracks.github.io/python-rtmidi-wheels/ --editable .
```
- **Optional**: You can install the outdated [Pypi package](https://pypi.org/project/sardine-system/) but it is older and lagging behind:
  ```python
  python -m pip install --find-links https://thegamecracks.github.io/python-rtmidi-wheels/ --editable sardine-system
  ```

**Note**: the `--editable` flag is optional. You can remove it if you are not planning to modify **Sardine**!

## Installing Ziffers

**Sardine** is great but **Ziffers** is great as well. The two together form the perfect live coding duo. 
**Ziffers** is developed by Miika Alonen independently from **Sardine** but are colaborating to make our
tools compatible together :) Install **Ziffers** now, you won't regret it later!

1) Clone the [ziffers-python](https://github.com/Bubobubobubobubo/ziffers-python) repository.
2) Install it like a regular Python package.

```python
git clone https://github.com/Bubobubobubobubo/ziffers-python
cd ziffers-python && python -m pip install --editable .
```
