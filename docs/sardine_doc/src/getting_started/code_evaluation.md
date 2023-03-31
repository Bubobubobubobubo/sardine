# Code evaluation

## Evaluating code

To live code, you always need to have two things :

- a document where you write your code.
- a running interpreter that will receive code.

One pattern is the base of everything, **sending new code for evaluation** :

- Your main document is your playing interface. Write / edit / change code.
- Send new code whenever you are ready by pressing a key.

On the included web text editor, press **Shift + Enter** or **Ctrl+E** to send code for evaluation. 
You need to select the code you want to send! If an error occurs, the application will not stop but will 
report the error and continue running using an older version of the code. The interpreter will warn you
if something goes wrong!

## Evaluating code

Write the following line and evaluate it:
```python
Pa >> d('bd cp')
```
At the beginning of the next bar, a musical pattern will start to play. This pattern will be composed of a kickdrum and a clapping sound in quick succession. We just evaluated our first **pattern**. This pattern will repeat indefinitely until you stop it.

To stop a pattern, use one of the following functions:
```python
silence() #  gentle shutdown
panic() #  hard stop (will be detailed later)
```
You can also be more precise about your intentions by giving the name of the pattern you want to stop:
```python
silence(Pa)
```
We will now repeat the kickdrum two times. Change the code and press **Shift+Enter** again:

```python
Pa >> d('bd!2 cp')
silence(Pa)
```

You can **live code** anything. The system will jump to the new version of your code
as soon as you submit it. This is how you **live code**. From now on, we will only 
get more specific and precise in the code we submit.

Evaluating code takes some practice. There are some pitfalls to avoid:
- you sometimes need to evaluate things in a specific order.
- you need to make sure that ALL your needed code is evaluated.
- sending code can fail for cryptic reasons (invisible characters), etc.
**Summary:**

- **Shift + Enter**: submitting new code.
- `silence()` or `panic()`: stop the execution of code.
