# Starting Sardine

Before starting **Sardine**, you need understand what **Sardine** is and where it 
sits on your system:

- **Fishery** is the **Sardine** interpreter. To play with **Sardine**, you need to start `fishery`.
- **Sardine** is the main **Python** library that you will be interacting with.
- Behind the scene, everything will be translated to **SuperCollider**, **MIDI** or **OSC** messages
  - `text editor -> fishery -> sardine -> SuperCollider/MIDI/OSC`)

Do not try to import `sardine` in a regular **Python** interpreter! It won&rsquo;t work, you will be disappointed. Whenever you start `fishery` in your terminal, the following splashscreen will appear:

```python
╭──────────────────────────────────────────────────────╮
│                                                      │
│ ░██████╗░█████╗░██████╗░██████╗░██╗███╗░░██╗███████╗ │
│ ██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝ │
│ ╚█████╗░███████║██████╔╝██║░░██║██║██╔██╗██║█████╗░░ │
│ ░╚═══██╗██╔══██║██╔══██╗██║░░██║██║██║╚████║██╔══╝░░ │
│ ██████╔╝██║░░██║██║░░██║██████╔╝██║██║░╚███║███████╗ │
│ ╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝ │
│                                                      │
│ Sardine is a MIDI/OSC sequencer made for live-coding │
│ Play music, read the docs, contribute, and have fun! │
│ WEBSITE: https://sardine.raphaelforment.fr           │
│ GITHUB: https://github.com/Bubobubobubobubo/sardine  │
│                                                      │
╰──────────────────────────────────────────────────────╯
BPM: 120.0,BEATS: 4 SC: [X], DEFER: [X] MIDI: Sardine
>>>
```

Only then will you know that **Sardine** has started and that everything is working! Some additional messages are likely to appear shortly after, warning you that the audio engine was hooked correctly or that an error has happened somewhere.

-   You can write code directly in the interpreter. However, this is not a recommended practice!
    -   You will soon begin to see that the system will print some useful information, preventing you from writing easily in the interpreter window. You should jump to your text editor!
-   For the duration of this tutorial, I will make the assumption that you are using `fishery web`, our internal text editor and environment!
