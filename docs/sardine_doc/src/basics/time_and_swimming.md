# Time and swimming

**Swimming functions** are interesting but they always repeat at the same rate. What if we want to repeat the function, but in rhythm?

The answer, once again, is the `p` (`period`) argument. This argument will allow you to precise the time of your **temporal recursion**. You can repeat the function every beat, every two beats, twice in a beat, etc&#x2026;

This function will clap twice per beat. Try to change the value in the last call to `again()`:


```python
@swim
def yes(p=0.5):
    D('cp')
    again(yes, p=0.5)
```


You now control the rate of repetition, which is the very basic of playing in rhythm. Obviously, we can be more clever than that. Hold on for a moment :)

What you are doing here, basically speaking, is passing a new `period` to your future function. You call that function **again** with a new period. The first value you give to `p` if your function signature has no importance because time is not flowing yet. After the first iteration, you basically **recall** your function with a new value of `p`, and again, and again, and again.. It loops! With loops, we can describe a lot of different things!

But.. wait. If we can pass a new value to the same function in the future, it means that we can also pass it some information! Let&rsquo;s try this:

This function will start to count, because the value of `i` will be incremented every time we loop around:

```python
@swim
def counter(p=0.5, i=0):
    print(f"Counter: {i}")
    again(counter, p=0.5, i=i+1)
```

This is **the stereotypical swimming function** and **you need to learn it by heart**. You can even start training writing it as fast as you can. You will type it a lot because this is an extremely convenient way to think about time both as a *cycle* (it loops) and as a continuity (we can count how many times it loops). Many many things in **Sardine** are based on this concept. Pretty much all of it!


