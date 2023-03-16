# SuperCollider interaction

If you are using **SuperDirt**, you are also somehow using **SuperCollider**. Most of the time, you can&rsquo;t really know about this because the process handling **SuperCollider** is invisible. Everytime you start **Sardine**, you also incidentally start **SuperCollider** and **SuperDirt** with only one command. **SuperCollider** is a very exciting programming language and audio server. Since its first publication in 1996, this software has been adopted by many musicians worldwide because of its robustness and performance. Some people are **live coding** directly in **SuperCollider** because they can handle its verbosity and complexity. Most of the time, people are developing high-level layers to communicate more easily with **SuperCollider** just like we do.

To get a better understanding of the **Sardine** environment, think about it this way:

-   **Sardine** is an independant layer on top of everything. It can do **MIDI** and **OSC** alone.
-   **SuperDirt** is a specialised audio engine designed to make **live coding** on **SuperCollider** simpler.
-   **SuperCollider** is the fundamental audio server that receives all the information and processes audio.

We can't do the audio synthesis or the scheduling directly in **Python**. The language is not fast enough to handle most of it and we must rely on external software to make things work smoothly. However, we can collaborate with it very easily.

It means that **Sardine** has a few commands that will help you get the most out of **SuperCollider**:

-   `SC.scope()` will open an *oscilloscope* pop-up window to visualise all your audio channels.
-   `SC.freqscope()` will open a frequency analyzer pop-up window to visualise your audio output.
-   `SC.info()` will open a general pop-up window that can help you with a few things:
    -   monitoring your CPU usage.
    -   monitoring the audio volume.
    -   recording sound on the server.

It does not end here. You can also execute arbitrary code written in **SCLang**, **SuperCollider&rsquo;s** programming language. To do so, simply pass a string to the `SC()` object:

    # Play a sinewave at 200hz
    SC("a = play({SinOsc.ar(200) * 0.25});")
    
    # Stop that sinewave
    SC("s.freeAll;")

In the future, it is very likely that **Sardine** interaction with **SuperCollider** will be further refined. For the moment, it is only used as lightweight high-level layer on top of **SuperCollider** :)


