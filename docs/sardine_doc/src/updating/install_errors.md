# Errors during installation

## Sardine is unable to locate SuperCollider

If Sardine is unable to locate *SuperCollider*, a message will be printed whenever you start `fishery`. Don't worry!
Unfortunately, this error is fairly common on Windows. You should be able to play with Sardine by turning off the
autoboot feature from `sardine-config`:
- run `sardine-config`.
- enter the `SuperCollider` section.
- toggle the first option, untoggle the rest.
- exit the configuration tool, save your changes.

Once done, use the following steps to start Sardine:
- start *SuperCollider*, write `SuperDirt.start` and press Shift+Enter.
- start `fishery` in your terminal.

SuperCollider and Sardine will be able to communicate but you will have to manage the two applications separately!
