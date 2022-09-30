@swim 
def test(d=0.5, i=0):
    S('amencutup:r*8').out(i)
    again(test, d=0.5, i=i+1)

hush()
