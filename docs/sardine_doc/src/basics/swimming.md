# Swimming functions

**Sardine** very existence is tied to the notion of **swimming functions**. 
A**swimming function** is a specific type of function that can easily be modified and updated **on the fly**,
whenever you want. Strictly speaking, a **swimming function** is a **temporally recursive function**, 
a construct used by many programming languages in the realm of music and digital art.
This way of writing functions is extremely interesting. People have been playing with the concept for more
than 30 years now. If you dig deep enough, you will find that the concept of **temporal recursive functions**
is at the very base of computer music systems such as **SuperCollider**.

Here is a basic Python function that you might already be familiar with:

```python
def hello_world():
    print('Hello, World!')
```
You can call this function like so:

```python
hello_world()
```

However, this will only be executed once. It is not very interesting for live coding or playing on stage. A few remarks:

- it would be much better if the function could be called again, indefinitely, in rhythm.
- it would be nice if we could reevaluate that function to change its behavior, whenever you want.

A **swimming function** is doing precisely doing that! It comes at a cost, a slightly different syntax. Evalute this:

```python
@swim
def hello_world():
    print('Hello, World!')
    again(hello_world)
```

Your interpreter window will now be polluted by the message `Hello, World!` printing on repeat. This is a good sign! The function will now be repeated indefinitely, until you change something. Let&rsquo;s change something then:

```python
@swim
def hello_world():
    print('Goodbye, World!')
    again(hello_world)
```

Now it prints `Goodbye, World!`. You can alter a swimming function whenever you want. Whenever you add `@swim` and `again()`, you make the function recursive. It is calling itself again and again.

You can stop a **swimming function** by changing the decorator (the `@` that *decorates* our function):

- `@swim`: the function will loop.
- `@die`: the function stops looping.

Let's stop our first **swimming function** then:

```python
@die
def hello_world():
    print('Goodbye, World!')
    again(hello_world)
```


Even though the function is fully written, it will not play anymore. Try to rewrite `@swim` again to make it start anew. You can also try to remove some parts of the function (the call to `again()`) to see what happens. Try to familiarise yourself with **swimming functions** because they are exciting!

If you don't like that syntax, you can also just call the `.stop()` method on any **swimming function** to make it stop:

```python
hello_world.stop()
```

You might be wondering what happens if a function is invalid. Under pressure, on stage, you can easily write a function that just doesn&rsquo;t make sense. Here is a fictional one written by an animal suddenly falling on the keyboard:

```python
@swim
def hello_world():
    qsjdfmlsqfdkjlm
    print('Goodbye, World!')
    again(hello_world)
```


You can try to evaluate this function. If you do so, the following will happen:

- If the function was previously running: **Sardine** will continue with the previous one that worked!
- If the function is brand new: **Sardine** will refuse to play and will warn you.

This means that you are immune to crash! You can experiment freely. The next step for you is now to try to make the system crash even by respecting these rules. It can happen, you have to be creative!


