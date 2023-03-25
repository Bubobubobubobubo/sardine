# Code evaluation

## Evaluating code

To live code, you need two things :

- a document where you write your code.
- a running interpreter that will receive code.

One action is the base of everything, **sending new code for evaluation** :

- Your main document is your playing interface. Write / edit / change code.
- Send code for evaluation by pressing a key or keystroke combination. 
- This combination of text / code editor with a code enterpreter is called REPL (read-eval-print-loop). 

On the included web text editor, select the code you want to execute and press **Shift + Enter** or **Ctrl+E**. This will cause the code to evaluated. If an error occurs, the code execution will not stop but will report the error and continue running using the existing code. The interpreter will warn you if something goes wrong! Every text / code editor that functions as REPL will have its own keystroke combination for code evaluation. 

## Evaluating code

Write the following line and evaluate it:
```python
Pa >> d('bd cp')
```
At the beginning of the next bar, a musical sequence will start to play with a kickdrum and a clapping sound in quick succession. This is a **pattern**. This pattern will repeat indefinitely until you stop it.

To stop a pattern, use one of the following functions:
```python
silence() #  gentle shutdown
panic() #  hard stop (will be detailed later)
```
You can also be more precise about your intentions by giving the name of the pattern you want to stop:
```python
silence(Pa)
Pa.stop()
```
The code below repeats the kickdrum two times. Change the code and press **Shift+Enter** again:

```python
Pa >> d('bd!2 cp')
silence(Pa)
```

You can **live code** anything. The system will jump to the new version of your code
as soon as you submit it. This is how you **live code**. 

Coding like this takes practice. There are some pitfalls to avoid:
- keep your code statements simple at first.
- sometimes code lines must be evaluated in a specific order.
- make sure that ALL your needed code is evaluated.
- sending code can fail for cryptic reasons (invisible characters or missing characters).
- pay attention to error messages, but sometimes they won't be helpful! 
   - when your code fails - study it closely for syntax, and try simpler statements

