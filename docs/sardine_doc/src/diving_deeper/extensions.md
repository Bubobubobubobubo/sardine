# Extensions

Sardine also has an extension/plugin system that lets you write custom *handlers* and take advantage of the time scheduling engine for your own purposes.

The steps for making a Sardine extension are:
- create a Python package containing your custom handlers
- create a configuration file for your extension
- reference this configuration file in Sardine's user configuration file.

The next paragraphs describe in more details how to do this with a simple example: the **Doug** extension.

### Doug structure

The project structure for a Sardine extension is quite standard: all you need is a root folder containing your Python package, and inside that package the modules containing the handlers (of course the package's content is not restricted to Sardine handlers, it is a regular Python package).

You can also place your extension's configuration file in your project for convenience, but note that this is not mandatory as you can place it anywhere that is accessible on your file system.

```
Doug
|__ doug
|   |__ __init__.py
|   |__ DougHandler.py
|__ doug-config.json
```

### Doug Handler

Here is an example of a Sardine extension handler:

```python
from sardine_core.handlers.sender import Number, NumericElement, ParsableElement, Sender, StringElement
from sardine_core.utils import alias_param

from typing import Optional, List


class DougHandler(Sender):

    def __init__(self, params: dict):
        super().__init__()

        self._intro = params['intro']

    def _doug_print(self, message):
        word = message["words"]
        if word is not None:
            print(f'{self._intro}:: {word}')

    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send(
        self,
        words: Optional[StringElement | List[StringElement]],
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **pattern: ParsableElement,
    ):
        if words is None:
            return

        if self.apply_conditional_mask_to_bars(pattern):
            return

        pattern["words"] = words
        deadline = self.env.clock.shifted_time
        for message in self.pattern_reduce(pattern, iterator, divisor, rate):
            self.call_timed(deadline, self._doug_print, message)
```

Let's decompose this and understand what Doug does.

The `DougHandler` class inherits from Sardine's `Sender` class: this allows us to use Sardine's native pattern parsing and time scheduling tools.

In the constructor method, we initialize our handler and provide it with a custom parameter called `intro::`. The value of such initialization parameters are specified in the extension's configuration file.

In the `_doug_print` method comes the core of what Doug does: it simply prints what it receives, starting all its lines with a little `intro`.

The `send` method is a simplified version the `send` method of Sardine's native sender (`MidiHandler`, `SuperDirtHandler`, etc.): it allows us to use Doug in *swim* functions and to use *patterns*.

### Doug configuration

The extension's configuration file is a JSON file that describes the project structure:

```json
{
  "root": "/path/to/Doug",
  "package": "doug",
  "handlers": [
    {
      "module": "DougHandler",
      "class": "DougHandler",
      "send_alias": "Doug",
      "params": {
        "intro": "sample"
      }
    }
  ]
}
```

The `params` field corresponds to the handler's constructor parameters.

The `send_alias` field corresponds to the alias that will be given to your handler's `send` method in Sardine's session (like the `D` for SuperDirt or `N` for Midi Notes): this alias will become a global variable so you have to make sure it doesn't conflict with anything else.

### Using Doug in Sardine

Using extensions is achieved by referencing the extension configuration files in Sardine's user configuration file:

```json
{
  "config": {
    ...
  },
  "extensions": [
    "/path/to/extension-config.json"
  ]
}
```

For now you have to edit the file manually by adding the path to the configuration files in the `extensions` list.

Resetting the user configuration file will clear all references to any extension you may have.

### Doug in practice

Now that we are able to use Doug in a Sardine session, let's see an example of what we can do with it:

```python
@swim
def hello_doug(p=1, i=0):
    pat = 'alphabet:[0:26]'
    D(pat, i=i)
    Doug(pat, i=i)
    again(hello_doug, p=1, i=i+1)
```

Calling `Doug` will actually call the `DougHandler.send` method (as it is the alias for it), which will parse the given pattern: hence in this example Doug will print the name of the sample SuperCollider is playing.

The visual output should look like:

```
sample:: alphabet:0
sample:: alphabet:1
sample:: alphabet:2
...
```

and the audio output should sound like: "A", "B", "C", ...
