# Acousmatic Tekno

<iframe width="700" height="500" src="https://www.youtube.com/embed/GvXRxAYYeTw" title="Acousmatic Tekno Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

```python
 ▄▄▄▄     ▄▄▄▄    ▄▄▄   ▄▄▄ ▄▄▄   ▄▄▄▄  ▄▄ ▄▄ ▄▄    ▄▄▄▄   ▄██▄  ▄▄▄    ▄▄▄▄     
▀▀ ▄██  ▄█   ▀▀ ▄█  ▀█▄  ██  ██  ██▄ ▀   ██ ██ ██  ▀▀ ▄██   ██    ██  ▄█   ▀▀    
▄█▀ ██  ██      ██   ██  ██  ██  ▄ ▀█▄▄  ██ ██ ██  ▄█▀ ██   ██    ██  ██         
▀█▄▄▀█▀  ▀█▄▄▄▀  ▀█▄▄█▀  ▀█▄▄▀█▄ █▀▄▄█▀ ▄██ ██ ██▄ ▀█▄▄▀█▀  ▀█▄▀ ▄██▄  ▀█▄▄▄▀    
                                                                                 
                                                                                 
█▀▀██▀▀█ ▀██▀▀▀▀█  ▀██▀  █▀  ▀█▄   ▀█▀  ▄▄█▀▀██      
   ██     ██  ▄     ██ ▄▀     █▀█   █  ▄█▀    ██     
   ██     ██▀▀█     ██▀█▄     █ ▀█▄ █  ██      ██    
   ██     ██        ██  ██    █   ███  ▀█▄     ██    
  ▄██▄   ▄██▄▄▄▄▄█ ▄██▄  ██▄ ▄█▄   ▀█   ▀▀█▄▄▄█▀     
                                                     
                                                     
clock.tempo=187

silence()

Pi * d("teratoma:[1~150]", leg=0.25, p=0.5, begin="rand")

Pi * d("spore:[1~150]", leg=0.25, p=0.5, begin="rand")

Pd * d('teratoma:[0:150]', amp=0.4, p=.5, leg=.05, pan='rand', speed='(if (beat 0 2) 1 0.5)')
Pe * d('.!8 spore:[0:50]', p=.25, leg=.1, pan='rand', on=2, speed=2)

PD * d('crunchorganic:[0:150]', amp=0.4, p=.5, leg=.05, pan='rand', speed='(if (beat 0 2) 1 0.5)')

PE * d('.!8 proximity:[0:50]', p=.25, leg=.1, pan='rand', on=2, speed=2)

Pk * d("kick:1 . laSNARE:[1~18] .", p=0.5, shape=0.45, room=0.15)

ph * d("leHIHAT:[8]", leg=0.25, p=0.25, orbit=2, shape=0.2)

PP * d("[proximity:[0:50] spore:[0:150]]", p=0.125, speed="(lsin 2)", 
        lpf="150*(lsaw 4)", leg=0.2, res=0.2)

Pk * d("kick:1 kick:[0~8] laSNARE:[1~18] .", p=0.5, shape=0.45,room=0.26)

ph * d("leHIHAT:[9:12]", leg=0.15, p=0.25, orbit=2, shape=0.2)

#double loud kicks c64 vibe

Pk * d("{kick:1 sid:2} {kick:[0~8] sid:2} laSNARE:[1~18] sid:2", p=0.5, room=0.26,shape=0.65)

#acousmatic break ?

silence()
Pk * d("{kick:1 sid:2} {kick:[0~8] sid:2} laSNARE:[1~18] sid:2", room=0.6,p="(rand)*0.5", shape=0.45,lpf=1000)
Pd * d('teratoma:[0:150]', amp=0.4, p=.5/4, leg=.1, pan='rand', speed='(if (beat 0 2) 1 0.5)')
Pe * d('.!8 spore:[0:50]', p=.25/4, leg=.3, pan='rand', on=2, speed="(lsaw 8)")
PD * d('crunchorganic:[0:150]', amp=0.4, p=.5/4, leg=.1, pan='rand', speed='(if (beat 1 3) 1 0.5)')
PE * d('.!8 proximity:[0:50]', p=.25/4, leg=.3, pan='rand', on=1, 
        speed="(lsaw 8)",lpf="2502*(lsin 8)")

silence(Pk,Pd,Pe,PD)
Pk * d("protokick", lpf="250*(lsaw 4)",res="(lsin 1)*0.5",p=0.25)

Pk * d("(eu protokick 3 5)", shape=0.9,lpf="250*(lsaw 4)",res="(lsin 1)*0.5",p=0.5)

Pd * d('teratoma:[0:150]', amp=0.4, p=.5, leg=.05, pan='rand', speed='(if (beat 0 2) 1 0.5)')
Pe * d('.!8 spore:[0:50]', p=.25, leg=.1, pan='rand', on=2, speed=2)
PD * d('crunchorganic:[0:150]', amp=0.4, p=.5, leg=.05, pan='rand', speed='(if (beat 0 2) 1 0.5)')
PE * d('.!8 proximity:[0:50]', p=.25, leg=.1, pan='rand', on=2, speed=2)
ph * d("leHIHAT:[9:12]", leg=0.25, p=0.25, orbit=2)
Pk * d("(eu protokick 3 5)", gain=0.93,shape=0.9,lpf="2500*(lsaw 4)",res="(lsin 1)*0.5",p=0.5)

#boom boom [o] [o]

solo(Pk)

Pk * d("(eu protokick [2~5] [6~9])", gain=0.93,shape=0.9,lpf="2500*(lsaw 4)",res="(lsin 1)*0.5",p=0.5)

silence()
```

