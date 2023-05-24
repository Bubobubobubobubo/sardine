# Post installation

You just installed **Sardine**. Congratulations. Now let's check if everything is alright.
Read and answer each and every of these questions. You will get familiar with the system
doing so!

## Do you see an error involving Alsa and MIDI?

Two months ago, an error started to appear for Linux users: `rtmidi._rtmidi.SystemError: MidiInAlsa::initialize: error creating ALSA sequencer client object.`.
To fix this error, you will have to manually copy some files to a different location:
- copy the `/usr/lib/alsa-lib/` into `usr/lib/x86_64-linux-gnu/alsa-lib` and/or `usr/lib64/alsa-lib`.
- if this path does not exist, try searching into `usr/lib/x86` or similar.

The source of this error is currently unknown and is not Sardine related. Hopefully, it will resolve automatically with future updates of the packages Sardine uses.

## Are you running Windows?

- **Windows users:** check if SuperCollider is properly detected.
  - if not, boot **SuperCollider** and **Sardine** side by side. Check the 
    [configuration section](../configuration/configuration_tool.md) and the
    troubleshot section to learn more about this process.

- **Windows users:** do you want to play virtual MIDI instruments (VSTs, etc)?
  - install a tool to create [virtual midi ports](https://www.tobias-erichsen.de/software/virtualmidi.html). Create at least one virtual port.
  - configure Sardine to use it in the `MIDI` section of `sardine config`.
  - Linux and MacOS users don't need to do this. The `Sardine` port is automatically created.

## Can you run sardine and sardine web?

- in your terminal, run `sardine` first! If you see a splashscreen, everything is fine! :)
- in your terminal, run `sardine web`! Does your web browser magically open? You are good to go.
  - Windows users: you will sometimes have to run this twice. Run the app. Quit it and launch again.

## Can you run sardine config? 

- in your terminal, run `sardine config`? If you see the configuration tool appearing, perfect!
- take some time to familiarise yourself with all the available options! The configuration step 
  is important.

## Do you want to turn on SuperCollider?

- If you want to play audio directly with **Sardine**, check out the 
  [configuration](../configuration/configuration_tool.md) section. Head to the `SuperCollider`
  section and turn everything on!

