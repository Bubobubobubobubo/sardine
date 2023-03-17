# Update / Uninstall

**Sardine** is distributed as a Python package. As such, installing, updating or deleting
is similar to doing so with a regular Python package.

## Deleting Sardine

- In your terminal, run `pip uninstall sardine`.
- Delete your `sardine` directory if you cloned it using Git.
- You will have to get rid of the configuration files manually.
  - Their path is documented in the [configuration section](../configuration/configuration_tool.md). 

Note that you will still have an installation of **SuperCollider** and **SuperDirt** 
if you followed the full install. Refer to their respective documentation if needed.

## Updating Sardine

I recommend installing **Sardine** using a freshly cloned version using **Git**. This will
allow you to get updates much faster by just running `git pull` from your terminal inside
of the Sardine folder. For the updates to be instantly applied to your version, note that
you need to have installed Sardine using the `--editable` flag. Please refer to the
[installation section](../installation/preliminary_words.md) to learn more about this. If
you followed the tutorial, you must have it installed in editable mode already.

The `--editable` mode means that your *Sardine* installation that *Python* refers to is folder
you just cloned and not a copy of it. Any modification made to it will be immediately mirrored
to the application you have installed.
