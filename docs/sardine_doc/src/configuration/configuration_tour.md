# Configuration tour

Let's break down what the options in the configuration tool are.
To start the configuration tool, please type `sardine-config` in your terminal.
A splashscreen will appear and some options will pop up as well!

### Show Config
- Print the configuration file.
### Reset
- Reset the configuration file.
  - other files such as the SuperDirt configuration are unnafected.
  - this won't delete your Python buffers or SuperCollider files.
### MIDI
The **MIDI** menu will allow you to select the default **MIDI** port used by **Sardine**. This port will be used to automatically create some targets for you to play with when first starting a session. More ports can be configured manually later on.
- **Automatic**: **Sardine** will try to create the... **Sardine** virtual port.
  - Only works for **MacOS** and **Linux**.
- **Manual**: Select a **MIDI** port from the list. 
  - The list is made out of all the MIDI hardware or software ports currently available on your system.
- **Custom (advanced)**: write the name of your **MIDI** port directly. Do not use this except for very good reasons!

### Clock
This menu will allow you to configure the default clock used by **Sardine** at the start of a session. You can always switch clock later (even when playing!) but you will usually stick to one clock only for the duration of a session.
- **No (internal clock)**: use the system clock. 
  - unsuitable for synchronisation with other users.
- **Yes (external clock)**: use the external Ableton Link clock. 
  - Automatic synchronisation with other players on the local network.
- You will also be prompted to enter a new default tempo and a default number of beats per measure.

### SuperCollider
- **Add SuperDirt Handler**: do you want to interact with **SuperDirt** at all?!
  - This is different from booting **SuperCollider**. **SuperDirt** is a more specialised engine for audio sampling and managing synthesizers. For newcomers, yes, you want to play with **SuperDirt**!
- **Boot a SuperCollider instance**: should **Sardine** try to manage **SuperCollider** by itself?
  - This is a safe option to use for people using **MacOS** or **Linux** but can result in problems later on for those using **Windows**. You will have to boot **SuperCollider** and **SuperDirt** manually if you untoggle this option!
- **Use Sardine boot file**: should we load our default boot file?
- **Turn on verbose output**: Debug printing.
  - Can prove very useful for **MacOS** and **Linux** users playing with their configuration.
  - Please turn it off for playing! Printing is expensive in Python!
- **Enter your SuperDirt booth path**: leave blank if you don&rsquo;t know what you are doing.
### Editor
- This menu will allow you to toggle the **web editor** by default or not. See the section concerning text editors to know if this is an option you want to consider. Note that this option is untoggled by default.
### More
- **Don't touch it**: it's for devs only :)



