# Troubleshot

## Sardine related

### Known bugs and issues

Please provide feedback on the installation process! I try to document it as much as I can but I lack feedback on the installation process on different systems, etc.. You might also have different use cases that I might not have anticipated.

* **[WINDOWS ONLY]**: `uvloop` does not work on Windows. Fortunately, you can still run **Sardine** but don't expect the tempo/BPM to be accurate. You will have to drastically slow down the clock for it to work (~20bpm is a safe value)! This might be linked to a different implementation of `asyncio` on Windows.

* **[LINUX/MACOS]**: `pip3 install` fails on `python-rtmidi build`. Its probably because the `libjack-dev` lib is missing. You can install it with `sudo apt-get install libjack-dev` on Debian based systems, with `brew` for MacOS, and with `pacman` for any other Arch-based system.


## SuperDirt related

* **[ALL]**: I don't hear any sound at all!

    - Check that `--boot` is `True` in your `sardine-config`: `sardine-config --boot True`.
    - Check that your audio output and microphone are running at the sample rate: 44100 or 48000hz. You can check this using your operating system usual configuration tools. Note that pluging in and out a microphone can change the sampling rate automatically.
    - Reboot **Sardine** and run: `S('cp').out()`. You should be hearing a clap.
    - **IF NOT**: boot *SuperDirt* manually and troublecheck using their own documentation.

## Others
