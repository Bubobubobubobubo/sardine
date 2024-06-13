<h2 align="center">
  <b>Sardine</b>: ✨ Live Coding Library for Python ✨
</h2>
<p align="center"><i>
  Python's missing Algorave module. Hackable live coding tool for modern Python (3.10+)
</i></p>

<p align="center">
  <img src=https://img.shields.io/discord/1029399269574193203 />
  <img src=https://img.shields.io/github/license/Bubobubobubobubo/sardine />
  <img src=https://img.shields.io/github/stars/Bubobubobubobubo/sardine />
  <img src=https://img.shields.io/pypi/wheel/sardine-system>
  <img src=https://img.shields.io/pypi/v/sardine-system>
  <img src=https://img.shields.io/pypi/status/sardine-system>
</p>


<p align="center">
  <a href="https://discord.gg/aPgV7mSFZh">Discord</a> |
  <a href="https://sardine.raphaelforment.fr/">Website</a> |
  <a href="https://sardine.raphaelforment.fr/showcase">Examples</a> |
  <a href="https://sardine.raphaelforment.fr/installation/">Installation</a> |
  <a href="https://raphaelforment.fr/">Author</a>  |
  <a href="https://toplap.org/">About Live Coding</a> |
  <a href="https://livecoding.fr/">Live Coding France</a>
  <br><br>
  <p align='center'>
    <a href="https://github.com/bubobubobubobubo/sardine/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=bubobubobubobubo/sardine" />
    </a>
  </p>
</p>

<p align="center">
  <a href='https://ko-fi.com/I2I2RSBHF' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi3.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
</p>

-----------

![Sardine algorave picture](pictures/sardine_intro_picture_repo.png)

**Sardine** is a versatile and user-friendly Python library designed for musical improvisation, algorithmic composition, and more. It turns your standard Python interpreter into a powerful musical instrument, allowing you to create and map melodic and rhythmic patterns to any electronic instrument (**MIDI**, **OSC**, and **SuperCollider**). With **Sardine**, you can:

- **Unleash your musical creativity on stage or in the studio**
  - Seamlessly communicate with any MIDI/OSC device and the **SuperCollider** audio engine using **Sardine**.
  - Utilize bindings for **SuperDirt**, a widely recognized audio engine embraced by live coders globally.

- **Python code but with time/tempo-awareness**
  - Employ temporal recursion to make any Python code time and tempo aware.
  - Accurately launch synchronous or asynchronous functions with time-specific results.
  - Customize your own **Senders** or **Receivers** to pattern any kind of data!

- **Develop intricate audiovisual performances with MIDI and OSC *I/O***
  - Assign **callbacks** to any OSC event, transforming **Sardine** into a sophisticated reactive toolbox.
  - Monitor changing values and incorporate them into your musical patterns or code.

- **Synchronize with other computers and musical instruments**
  - Synchronise your hardware with **MIDI Clocks**.
  - Synchronize effortlessly with other tools or players using the **Link Protocol**.

## Installation

Refer to the [installation section](https://sardine.raphaelforment.fr/installation.html).

## Contributions

Sardine is in its early stages of development, and we're actively seeking contributors to help the project. If you're passionate about music and technology, we welcome your expertise, whether it's code, documentation, or ideas. We are looking for contributors! 

To collaborate with the Sardine community, connect with us on **Discord**, **Github** or send a private message if you have specific inquiries.

### Generating documentation

**Sardine** documentation is using [mdbook](https://rust-lang.github.io/mdBook/guide/creating.html). You first need to have [Rust](https://www.rust-lang.org/tools/install) properly installed.

```
cargo install mdbook
mdbook serve --open
```

You should have the documentation automatically opened in your browser at <http://localhost:3000/>.
