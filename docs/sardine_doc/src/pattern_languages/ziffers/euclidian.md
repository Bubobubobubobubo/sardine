# Euclidian



Euclidean rhythms can be used to create rhythms or complex rhythmic variation to melodies.

Euclidean syntax is `(onbeat)<2,4>(offbeat)` where (offbeat) is optional and defaults to `r`.

```python
Pa * zd("superpiano","(0)<3,5>") # 0 r 0 0 r
Pa * zd("superpiano","(0 1 2)<3,5>") # 1 r 2 3 r
Pa * zd("superpiano","(0 1 2)<3,5>(6 5)") # 0 6 1 2 5
Pa * zd("superpiano","((q <0 3> e 2) (q 5 e 2))<3,5>") # Cycling groups 
Pa * zd("superpiano","((q <-3 3> s 8 2) (q 5 e 2))<5,8>(e 8 (s 9 6))") # Cycling onset and offset groups
```

# Euclidean patterns with samples

TBD!
