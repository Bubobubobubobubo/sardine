## The importance of patterning 

By nature, *swimming functions* are repetitive. Almost everything you play with is falling into a time loop. Strict repetition can be come pretty boring after a while, and you need to find a way to define events that will gradually change in time, whether it is because they are sequence of events, random events, mutating events, etc... Sequencing and patterning is the big deal for *live-coders*. That's how they think about composition / improvisation, that's how they write interesting music by patterning synthesizers, audio samples, custom events and much more. If you go down the rabbit hole, you can also pattern your patterns. You can also pattern the functions altering your patterns. There is no limit to it, only what you are trying to define and play with.

Thinking about music being composed with patterns, recursion and time loops is a deparature from the timeline / score model we are used to when thinking about music being written on scores or being recorded on tape. By patterning and thinking about loops, we enter into a different relationship with sound materials and the management of musical information. 

It would have been weird to design **Sardine** without taking into account the fact that **patterning** is as much needed as control over the temporal execution of code. **Sardine** is taking some inspiration from [ORCA](https://github.com/hundredrabbits/Orca) (Devine Lu Linvega), [FoxDot](https://github.com/Qirky/FoxDot) (Ryan Kirkbride) and [TidalCycles](https://tidalcycles.org) (Alex McLean and colaborators). These systems, among others, have been designed just like **Sardine** around the idea of patterning values in musical time. They all choose a different route to do so, and come up in exchange with interesting concepts about what an event or even what time is in a musical improvisation system. **Sardine** is proposing its own flavor of patterning that you will soon discover :)

## I - What are patterns?

**Sardine** was designed with its own internal pattern language. This pattern language is not **Python** but a very specialised subset of it written from scratch. It basically came into existence because of my frustration with the inability to define custom operators and to really override the behavior of primitive data types. This language is interpreted on-the-fly when you play music with **Sardine**. Some objects such as **senders** are really good at interpreting patterns naturally. Some can be forced to take patterns as arguments. You don't really have to care about it and the syntax is so close to **Python** that it never feels like speaking multiple languages.

**Patterns are lists**. Everything you write in a pattern form will eventually output a list. Just like lists, you can **extract values by using an iterator**. With **Sardine**, patterns are usually written as strings (`"1,2,3,4"`, `"$.p%20+10"`, `"C@min7^1"`, etc...). Remember these few facts, all the rest is just the consequence of other mechanisms built around this behavior. There are multiple ways to extract values from a list:

- in order, by reading every element of the list one after the other.

- in reverse order, the same thing the other way around.

- randomly, by taking arbitrary values out of the list.

- sometimes in one direction, sometimes randomly, sometimes in reverse order?

There are other things to take into consideration when time enters the game. How often should we extract values? Should we skip some elements if a time condition is met? What if the index is manipulated? What if you pattern all of this? As you can see, there is no end to this game and patterns can be sometimes boring, sometimes wonderful, sometimes totally chaotic to the point where it would be better not to have one, etc... It is a never-ending game of exploring them and finding the best techniques to create interesting variations.

## II - Observing patterns

You can use the `Pat()` object to get a *generic interface* to **Sardine** patterns. This object can be used just anywhere you would like to see a pattern. It means that you can contaminate your Python functions or anything in your text buffer with them and see what comes out of it. As you will soon learn, the inverse is true. **Python** data can enter in the pattern realm as well.

```python3
@swim
def free(p=0.5, i=0):
    print(Pat('1,2,3,4', i))
    again(free, p=0.5, i=i+1)
```

In the example above, we are just using a *swimming function* to print the result of a pattern. It just goes through each element in sequence. That is because we are feeding an **iterator** to the `Pat(pattern, iterator)` function. Try to change that **iterator**. It'll already produce a variation on the pattern without even touching the pattern itself:

```python3
@swim
def free(p=0.5, i=0):
    print(Pat('1,2,3,4', i if random() > 0.5 else i+2))
    again(free, p=0.5, i=i+1)
```

The good thing with writing your own language is that you can write it to make some things more easy to accomplish. Why counting to 4 by writing down each number? We already have something to do it for us:

```python3
@swim
def free(p=0.5, i=0):
    print(Pat('[1:4]', i if random() > 0.5 else i+2))
    again(free, p=0.5, i=i+1)
```

Ok but now what if we would like to combine this pattern with the same one in the opposite direction? We can use functions from the `FuncLibrary` to do so:

```python3
@swim
def free(p=0.5, i=0):
    print(Pat('pal([1:4])', i if random() > 0.5 else i+2))
    again(free, p=0.5, i=i+1)
```

You might sometimes feel a bit lost when writing complex patterns. As you'll soon discover, there are many features to the language. Always remember that you can print out patterns! You can observe them without making sound and you can even use them to do other tasks if you prefer. **Sardine** is cool for music playing but you can do much more with it. 

## III - Patterns and senders

**It now all falls into place!** We saw *swimming functions*, *senders*, and now *patterns*. These three features form the core of **Sardine** and you are now ready to understand all of it. String keyword arguments feeded to senders are patterns! These strings will be interpreted and replaced by lists internally to form the final message. Ok, but where is the **iterator**? You can see it in the tail of your sender, the `i` letter in the example below.

```python3
@swim
def boom(p=0.5, i=0):
    D('bd', 
        cutoff='r*2000',
        speed='1,2,3,4', i=i)
    again(boom, p=0.5, i=i+1)
```

Conceptually, *senders* are pattern sandwiches. It is a collection of lists sharing a common **iterator**. They all form a common event by merging together in a final message. The easiest way to deal with this is to have one and only one iterator but of course, if you don't like it that way, you can have multiple **iterators** in a single *sender*.

```python3
@swim
def boom(p=0.5, i=0):
    D('bd', 
        cutoff=P('2000!4, 4000!2, 8000!3, 200~5000', i+2),
        speed='1,2,3,4', i=i)
    again(boom, p=0.5, i=i+1)
```

It can even be more extreme than this but it all depends on what you are trying to achieve! You already saw that the tail method of your *sender* also have additional parameters that you can use to further refine the message composition.

## IV - Iterators are cool 

```python3
@swim
def boom(p=0.5, i=0):
    D('bd', 
        cutoff=P('r*2000, 500, 1000', i%2),
        speed='1, 2, 3, 4', i=randint(1,4))
    again(boom, p=0.5, i=i+1)
```

You can be creative with **iterators** and easily generate semi-random sequences, drunk walks, reversed sequences, etc... Be sure to always have a few different iterators close by to morph your sequences really fast. I know that writing complex patterns is nice but they are nothing without good iterators.