# Sleeping and oversleeping


**Sardine** has a few tricks up its sleeves. **Swimming functions** can mimick [Sonic Pi](https://sonic-pi.net/) `sleep()` method because why not! The `sleep()` method from **Python** (and from most programming languages) is very imprecise. It doesn&rsquo;t offer any guarantee on the duration of the sleep. Your program will halt and come back after a certain time, but not always when you need it the most. It won&rsquo;t be really helpful to write precise rhythms like we do in music. **Sonic Pi**, long time ago, acknowledged that issue. They did something about it.

Following its model, **Sardine** is overriding the default `sleep()` method. You can use the new version just like the old one. The interface is very similar. However, it will allow you to write precise rhythms:

```python
@swim
def super_sleeping(p=2, i=0):
    D('bd')
    sleep(1)
    D('cp')
    again(super_sleeping, p=2, i=i+1)
```

Let me explain what I just wrote:

- we are using a regular **swimming function**. The syntax is untouched.
- we use a central `sleep(1)` statement to make a pause in our pattern.
- we do the recursion after a period of `two beats`.

There is something a bit un-intuitive about this. Strictly speaking, **the sleep method is not halting anything, it just shifts the events coming after it to some point in the future**. Read this twice!

It means that you can `sleep()` for some time but the function will not end if the recursion is coming much later. If will just defer the execution of what comes after the sleep and wait until the function is done looping:

```python
clock.tempo = 100
@swim
def super_sleeping(p=2, i=0):
    D('bd')
    sleep(0.25)
    D('{cp sn}')
    D('tabla')
    # ...
    # Nothing happens
    # ...
    again(super_sleeping, p=2, i=i+1)
```

You can also **oversleep** the duration of your function. You defer an event enough so that it occurs after **swimming function** loops:

```python
clock.tempo = 100
@swim
def super_sleeping(p=2, i=0):
    D('cp', speed='[1:5,0.25]', i=i)
    sleep(0.75)
    D('linnhats', speed='[1:5,0.25]', i=i)
    again(super_sleeping, p=0.5, i=i+1)
```

In the example above, the `linnhats` sound is deferred to later, and later means on the **next loop** of our **swimming function**. Rhythms piling up on top of rhythms!

### Patterning sleep()
This example shows how to add patterning to `sleep()`. Musically this can be used to vary the rhythm.  Notice that this requires use of the [Pattern Object](./pattern_object.md). Don't forget to include the iterator (i)!

```python
@swim
def super_sleeping(p=2, i=0):
    D('cp', speed='[1:5,0.25]', i=i)
    sleep( P('.85 1.25!3', i) ) # Pattern Object with iterator
    D('linnhats', speed='[1:5,0.25]', i=i)
    again(super_sleeping, p=0.5, i=i+1)
```
