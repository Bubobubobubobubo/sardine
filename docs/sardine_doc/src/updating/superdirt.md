## No sound, what should I do?

Sometimes, **SuperDirt** will refuse to boot. You won&rsquo;t hear anything and **Sardine** will appear to be working perfectly. There are some steps I recommend to follow while trying to debug that issue:

-   Check if **SuperDirt** is configured to boot in your **sardine config**
-   Check that your audio output and microphones are running at the audio sample rate (*44100* or *48000hz*) on both sides (audio output / input). You can check this using your operating system usual configuration tools. Note that pluging in and out a microphone can change the sampling rate automatically. This is annoying, but so is life!

## I still can't hear anything!

-   Sometimes, when you play around with booting and quiting **Sardine** repeatedly, your computer might start to get confused about who is using some of the network connections or not. You now have **zombie connexions** blocking the I/O process from running normally. This can also happen simply by opening multiple instances of **Sardine** on the same computer!
    -   kill every instance of **Sardine** and **SuperCollider** and the code editors that hosted them.
    -   run `Server.killAll` in a brand-new **SuperCollider** window.

This should solve the issue. If not, it might be something more serious and is less likely to be an error arising from **Sardine** itself. As crazy as it might sound, I'm not responsible of all the computer errors :)

-   Use **sardine config** and tell it not to boot **SuperCollider** automatically by itself.
-   Open **SuperCollider** and **Sardine** side by side. From there:
    -   type `SuperDirt.start` in your **SuperCollider** window and press **Shift + Enter** to manually start **SuperDirt**.
    -   boot **Sardine** as usual, and try to play some sounds using it.

If you are stil unable to play sound then you have a broken install. Join us on the **Discord** server to get some help fixing the issue.
