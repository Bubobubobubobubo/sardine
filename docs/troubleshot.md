---
hide:
    - navigation
---

# Troubleshot

This page will guide you along if you need to debug **Sardine**. It can be anything ranging from problems while installing it to problems encountered during performance. If you encounter an issue that is currently not documented here, please forward it by using the issue tracker on GitHub or by directly sending a mail out to me :)

## Broken Sardines

Some bugs and issues are related to **Sardine** itself. I try to document the errors encountered by users as much as I can but I still lack feedback on the installation process for different systems, etc.. You might also have different use cases that I might not have anticipated.

!!! warning "`python3 -m fishery`: no module named ..."
    **[ALL]**: This is likely the sign of an incomplete **Sardine** installation. Please make sure that you have `MSVC` (Windows), `gcc` (Linux) or `clang` (MacOS) installed and that you have also installed `CMake`. The installation failed because some libraries couldn't compile. By failing more or less silently, some other dependencies have not been installed. This is the mythical *broken sardine*.

!!! warning "`python-rtmidi` fails on install"
    **[LINUX/MACOS]**: Installation fails on `python-rtmidi build`. Its probably because you missed libjack development files (`libjack-dev` or `libjack-jack2-dev`). You can install it with `sudo apt-get install libjack-dev` on Debian based systems, with `brew` for MacOS, and with `pacman` for any other Arch-based system.

!!! warning "`jack.h` missing on install"
    **[MACOS]**: Install fails on `python-rtmidi build`. You might have JackOSX installed. Remove it **entirely** from your system and rely on *CoreAudio*. Nothing personal against **Jack**, it just confuses the compilation process of `python-rtmidi`!

!!! warning "uvloop warning or errors"
    **[WINDOWS ONLY]**: `uvloop` does not work on Windows. Fortunately, you can still run **Sardine** but you might have some issues targetting blindly a specific tempo. You will sometimes (?) have to drastically slow down the clock for it to work (~20bpm is a safe value)! This might be linked to a different implementation of `asyncio` on Windows. This issue is currently being investigated and is not fairly common.

## SuperDirt related

!!! warning "I don't hear any sound at all!"
    Check that `--boot_superdirt` is `True` in your `sardine-config`: 
    ```shell
    sardine-config --boot_superdirt True
    ```
    Check that your audio output and microphone are running at the sample rate:

    - 44100 or 48000hz on both sides (audio output / input). 
        
    You can check this using your operating system usual configuration tools. Note that pluging in and out a microphone can change the sampling rate automatically.

!!! warning "I still can't hear anything!"
    Sometimes, when you play around with *booting* and *quiting* Sardine repeatedly, your computer might start to get confused about who is using some of the network connections or not. You now have **zombie connexions** blocking the I/O process from happening (**Sardine** can't match with **SuperCollider**, etc...). This can also happen simply by opening multiple instances of **Sardine**.

    If that is to happen, please make sure to:

    - kill every instance of **Sardine** and **SuperCollider** and the code editors that hosted them.

    - run `Server.killAll` in a brand-new **SuperCollider** window.

    You can now start again.
