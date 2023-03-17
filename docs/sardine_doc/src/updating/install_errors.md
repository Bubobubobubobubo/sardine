# Errors during installation

## Sardine is unable to locate SuperCollider

If Sardine is unable to locate *SuperCollider*, a message will be printed whenever you start `fishery`. Don't worry!
Unfortunately, this error is fairly common on Windows. You should be able to play with Sardine by turning off the
autoboot feature from `sardine-config`:
- run `sardine-config`.
- enter the `SuperCollider` section.
- toggle the first option, untoggle the rest.
- exit the configuration tool, save your changes.

Once done, use the following steps to start Sardine:
- start *SuperCollider*, write `SuperDirt.start` and press Shift+Enter.
- start `fishery` in your terminal.

SuperCollider and Sardine will be able to communicate but you will have to manage the two applications separately!

## ModuleNotFoundError: No module named 'setuptools.command.build'

This error is fairly common if you install Sardine using the default Python installation that comes with your system.
This is likely  the case for Linux and MacOS users. This error happens because these pre-installed versions of Python
do not come with the `setuptools` module. You'll have to install it yourself:
  - install `setuptools` using pip: `python -m pip install setuptools`
  - install [Pyenv](https://github.com/pyenv/pyenv) to get a clean install of Python.
    - Pyenv is the recommended method to use. It makes managing Python versions easier.



