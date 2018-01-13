# 2004-I2C-LCD-and-Encoder-Interface
User interface that allows user to set parameters for a software defined radio using a Beaglebone Black

These scripts use the Adafruit BBIO Encoder interface. Follow the steps to set up the encoder interface correctly [Beaglebone encoder] https://github.com/adafruit/adafruit-beaglebone-io-python/tree/master/Adafruit_BBIO

## Dependencies:
* BBIO 1.0.9 
* python-smbus

## Pins Used:
* LCD Screen
  * P9_19 SCL
  * P9_20 SDA
* Encoder using eQEP2
  * P8_10 for button
  * P8_11 DT
  * P8_12 CLK

## Example:
Open and run ROT_LCD_Snippet in cloud9 or beaglebone black interface
```
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
```

## Callable Function:
Using the name given in the example, other callable functions include:

rotlcd.setParameters(Start Frequency, End Frequency, Sample Rate)

rotlcd.get_Range()
  * Returns the start and end frequency

rotlcd.get_Sample_Rate()
  * Returns sample rate
  
rotlcd.RestartTime(Time)
  * Determines if old time will be used to reset time.
  * Used is making a function run ever segment of time

## To Dos:
* Correct sample rate to change 2^n increments
* Add animation to intro screen
* Implement Internet Options and Other
* Improve Stability and reliability
* Reduce script size if possible
* Add write function to correct range for spectrum
* Improve lcd_api to allow build-in characters for lcd 
