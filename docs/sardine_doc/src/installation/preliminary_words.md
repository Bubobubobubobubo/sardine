# Preliminary words

Sardine will allow you to fly. Before flying, please make sure that you have wings. Otherwise, you are just building a rocket and you will crash into a wall. Read this page carefully, prepare your computer for installation. In particular we will make sure that:
1) You know how Python is installed.
2) You downloaded all the required software.
3) You understand what Sardine is.

## 1) The proper way to install Python

![xkcd](https://imgs.xkcd.com/comics/python_environment.png)

**It is extremely important to know how your current version of Python is installed.**
- You can have multiple versions of **Python** running on the same system.
- **Always** prefer a version of Python that you installed yourself. 
- **Be careful** with aliases. On Windows, people often have **python** and **py** living side by side.
- **They are not the same installation of Python**.

You will now install [Pyenv](https://github.com/pyenv/pyenv), the only Python version manager that you can trust. For Windows, please install [Pyenv for Windows](https://github.com/pyenv-win/pyenv-win). The installation process is well explained by the Pyenv team. Once it is done, please run the following commands:
- `pyenv install python3.11`: install Python 3.11 with all its bells and whistles.
- `pyenv global python3.11`: make this version the base install on your system.

Now, **kill your command line** and restart a fresh terminal. The output of `python --version` should look like you have installed a Python 3.11 version:

```bash
❯ python --version
Python 3.11.3
```


## 2) Other versions of Sardine

- As funny as it may sound, I am not the owner of the `sardine` package on Pypi. **Sardine** is named `sardine-system`. Some people sometimes end up installing a totally unrelated tool!
- `sardine-system` is very outdated. Please install from source.

## 3) The modular architecture of Sardine

- Sardine is a **very** flexible software. It can be hard to install for that reason.
- You probably don't need everything but you need to understand the architecture:
  - **Sardine web** is an optional text editor for **Sardine** written in TypeScript.
  - **Sardine** is an asynchronous Python interpreter firing up the **Sardine** library.
  - **Sardine Core** is the Python library that is responsible for all that livecoding.
    - it defines a temporal engine allowing you to live code in Python.
    - it communicates through the OSC protocol or through MIDI ports.
    - it allows you to create musical code using powerful patterning engines.
