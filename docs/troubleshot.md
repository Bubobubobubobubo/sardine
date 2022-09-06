# Troubleshot

## Sardine related

Some bugs and issues are related to **Sardine** and **Sardine** only. Please provide feedback on the installation process! I try to document it as much as I can but I lack feedback on the installation process on different systems, etc.. You might also have different use cases that I might not have anticipated.

!!! warning "uvloop warning or errors"
    **[WINDOWS ONLY]**: `uvloop` does not work on Windows. Fortunately, you can still run **Sardine** but don't expect the tempo/BPM to be accurate. You will have to drastically slow down the clock for it to work (~20bpm is a safe value)! This might be linked to a different implementation of `asyncio` on Windows.

!!! warning "`python-rtmidi` fails on install"
    **[LINUX/MACOS]**: `poetry install` fails on `python-rtmidi build`. Its probably because the `libjack-dev` lib is missing. You can install it with `sudo apt-get install libjack-dev` on Debian based systems, with `brew` for MacOS, and with `pacman` for any other Arch-based system.


!!! warning "`jack.h` missing on install"
    **[MACOS]**: `poetry install` fails on `python-rtmidi build`. You might have JackOSX installed. Remove it **entirely** from your system and rely on *CoreAudio*. Nothing personal against **Jack**, it just confuses the compilation process of `python-rtmidi`!

!!! warning "Rhythmic hiccups in Ableton Link mode"
    **[ALL]**: The `Ableton Link` protocol integration is not fully done yet! You might experience issues with interrupted loops or various rhythmic hiccups. A fix is on the way!


## SuperDirt related

!!! warning "I don't hear any sound at all!"
    Check that `--boot_superdirt` is `True` in your `sardine-config`: 
    ```shell
    sardine-config --boot_superdirt True
    ```
    Check that your audio output and microphone are running at the sample rate:

    - 44100 or 48000hz on both sides (audio output / input). 
        
    You can check this using your operating system usual configuration tools. Note that pluging in and out a microphone can change the sampling rate automatically.
