# Slicing

The **Sardine** pattern notation is built around the idea of having
multiple ways to deal with linear lists and collections. The basic
arithmetic syntax and most operators work on single tokens **but will
also work on lists**. It means that you can write expressions such 
as :
    
```python
[0 1 2 3]%8
[0 2 4 5]*[4 5]
[1:8 0.1]&[2 9]
[0 2 4 5 9 10 12 14]!2
[0 2 4 5 9 10 12 14]!!4
```
    
There are a few special operators that are only available when you deal with lists. This is something you will get familiar with by trying. You will see that most things work while some will not yield the result you expect.

## Slicing and indexing

```python
@swim
def test_slicing(p=0.5, i=0):
    pattern = P('[1 2 3]&[1]') # change me
    print(pattern)
    again(test_slicing, p=0.125, i=i+1)
```
    
- You can get a slice or just one value from a list by using the special `&` operator.
- It will work with any list on the right side of the operator but it will 
  only take the first and second value of it no matter what to compose a slice.
- The index value can be infinite because the index is looping on the list. You can feed
  a random number generator and get something out.
    
On the down side, slicing can become quite complex to write, so be careful with it:
    
```python
@swim
def test_slice(p=0.5, i=0):
    D('pluck:19', legato=0.2,
      n='[60 62 63 67 69 71]^(1~5)&[1~4]', i=i)
    again(test_slice, p=0.125, i=i+1)
```


