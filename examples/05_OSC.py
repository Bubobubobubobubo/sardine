from random import randint, random, chance

# Open a new OSC connexion
my_osc = OSC(ip="127.0.0.1",
        port= 23000, name="Bibu",
        ahead_amount=0.25)

# Simple address
O(c, my_osc, 'loulou', value='1 2 3 4').out()

# Composed address (_ equals /)
O(c, my_osc, 'loulou_yves', value='1 2 3 4').out()
