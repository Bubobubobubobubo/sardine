# SuperCollider / SuperDirt

The `default_superdirt.scd` is your default **SuperDirt** configuration. **SuperDirt** is the nickname of a very powerful audio engine used by some live coding libraries like **Sardine**. By default, this file will specify **where to look for audio samples** or **how many inputs and outputs** your system must use.

You must edit it manually if you are willing to change anything to it. This is outside of the reach of **Sardine** and it is preferable to let the user decide for the most suitable configuration. The [SuperDirt](https://github.com/musikinformatik/SuperDirt) repository is a good place to start, especially the `hacks/` folder. It will teach you how to edit and configure **SuperDirt** to your liking. **SuperDirt** was initially conceived for [TidalCycles](https://tidalcycles.org/). You will find a great amount of customization options on their website too!

Here is an example showing of how to load more audio samples to play with:

```python
(
s.reboot {
    s.options.numBuffers = 1024 * 256;
    s.options.memSize = 8192 * 32;
    s.options.numWireBufs = 128;
    s.options.maxNodes = 1024 * 32;
    s.options.numOutputBusChannels = 2;
    s.options.numInputBusChannels = 2;
    s.waitForBoot {
        ~dirt = SuperDirt(2, s);
        ~dirt.loadSoundFiles;
        ~dirt.loadSoundFiles("/Users/bubo/Dropbox/MUSIQUE/LIVE_SMC/DRUMS/*");
        s.sync;
        ~dirt.start(57120, 0 ! 12);
        (
            ~d1 = ~dirt.orbits[0]; ~d2 = ~dirt.orbits[1]; ~d3 = ~dirt.orbits[2];
            ~d4 = ~dirt.orbits[3]; ~d5 = ~dirt.orbits[4]; ~d6 = ~dirt.orbits[5];
            ~d7 = ~dirt.orbits[6]; ~d8 = ~dirt.orbits[7]; ~d9 = ~dirt.orbits[8];
            ~d10 = ~dirt.orbits[9]; ~d11 = ~dirt.orbits[10]; ~d12 = ~dirt.orbits[11];
        );
    };
    s.latency = 0.3;
};
)
```

SuperDirt treats a wildcard (`*`) at the end of the path to mean that there are named subdirectories. If you want to load just one sample directory, omit the wildcard.

