from LCD_RotaryR2 import ROT_LCD
import time


Sf = 420.0125e6
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
        stfreq,ffreq,samplerate = rotlcd.get_Parameters()
        print(stfreq,ffreq,samplerate)
        rotlcd.recordOn()
        time.sleep(7)
        print('Stop Recording')
        rotlcd.recordOff()
        old_time = time.time()