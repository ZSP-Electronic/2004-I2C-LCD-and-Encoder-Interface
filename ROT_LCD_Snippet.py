from LCD_RotaryR2 import ROT_LCD
import time


Sf = 420e6
Ff = 512e6
samprate = 2.048e6
rotlcd = ROT_LCD()
rotlcd.setParameters(Sf,Ff,samprate)

old_time = time.time()

while True:
    rotlcd.void_main(True)
    old_time = rotlcd.RestartTime(old_time)
    
    if time.time() - old_time > 20:
        print('Recording')
        time.sleep(7)
        old_time = time.time()
