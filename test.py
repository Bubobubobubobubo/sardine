Pat("sometimes(C, F, A)", 0)

Pat("sometimes()", 0)

# Syntax tests


@swim
def baba(p=0.5, i=0):
    D("jvbass", midinote="rare() @ bass(C4|C5,D|F+12,Eb)", i=i)
    again(baba, p=0.25, i=i + 1)
