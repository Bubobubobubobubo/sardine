

c.bpm = 130


hush()

c.bpm = 180
@swim
def hey_pattern(d=0.5, i=0):
    S('arpy', 
            speed='0.5!7,1',
            midinote="C,E,G,A,B,E,G:penta",
            room=4.9, dry=0.2,
            cutoff='(2000,5000,8000,9000)',
            legato=0.9).out(i) 
    again(hey_pattern, d=P('0.25',i), i=i+1)

@swim
def bb(d=0.5, i=0):
    S('bd, hh:4, p, hh:9').out(i)
    S('m:2_4', speed='r/4', cutoff='2_20*100').out(i)
    S('b, u:4, b:8, o:9', 
            legato='1,0.5,0.25',
            speed='0.5,2,4,0.25', 
            trig=euclid(3,8)).out(i)
    S('jvbass,jvbass:4', cutoff='1_10*100', 
            octave='5!2,6').out(i)
    again(bb,d=P('0.5!4,1', i), i=i+1)
