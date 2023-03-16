# Linux

## Preparing your environment

The first step to install **Sardine** is to prepare your system to make some sounds :)

1) Install the latest [Python](https://www.python.org/) version for your OS (currently l3.11). **Sardine** will not work with a Python older than 3.10. Be careful with distribution provided Python versions, they are not yours! Install [Pyenv](https://github.com/pyenv/pyenv) or use [virtual environments](https://docs.python.org/3/library/venv.html) to keep everything nice and tidy!
2) Install [SuperCollider](https://supercollider.github.io/), the default audio backend used by **Sardine**.
   -   Once this step is over, open **SCIDE** (or click on the **SuperCollider** icon) and type:
    ```Quarks.install("SuperDirt");```

3) Press **Shift + Enter** and wait for the installation to be done! Close **SuperCollider** when done.

4) **Optional:** You can also install [sc3plugins](https://github.com/supercollider/sc3-plugins) to get more audio effects and synthesizers!

## Installing Sardine

To install **Sardine**, you can either:

1) install the development version (recommanded -> **up to date**).
    
        git clone https://github.com/Bubobubobubobubo/sardine
        cd sardine
        python -m pip install --find-links https://thegamecracks.github.io/python-rtmidi-wheels/ --editable .
2) install the [Pypi package](https://pypi.org/project/sardine-system/) (older, lagging behind).
    
        python -m pip install --find-links https://thegamecracks.github.io/python-rtmidi-wheels/ --editable sardine-system
3) **Note:** the `--editable` flag is optional. You can remove it if you are not planning to modify **Sardine**!

These commands will download and install **Sardine** using the recommended method. Once the installation is done, you now have officially installed **Sardine** with all its dependencies. Congratulations! You can now proceed to the configuration section. If you encounter an error, please head to the **Troubleshot** section or ask a question on the **Discord server** or in the **Github Issues**.

## Installing Ziffers

**Sardine** is great but **Ziffers** is great as well. The two together form the perfect duo for making algorithmic music. **Ziffers** is developed by Miika Alonen independently from **Sardine** but we do collaborate to blend our tools together :) Install **Ziffers** now, you won&rsquo;t regret it later!

-   Clone the [ziffers-python](https://github.com/Bubobubobubobubo/ziffers-python) repository.
-   Install it like a regular Python package.

TLDR:

    git clone https://github.com/Bubobubobubobubo/ziffers-python
    cd ziffers-python && python -m pip install --editable .


