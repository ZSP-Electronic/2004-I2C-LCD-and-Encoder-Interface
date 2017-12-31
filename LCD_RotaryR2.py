from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP2
import Adafruit_BBIO.GPIO as GPIO
from i2c_lcd import I2cLcd
import customChar
import time

LCD_I2C_ADDR = 0x27
ROT_SW = 'P8_10'
        
myEncoder = RotaryEncoder(eQEP2)
myEncoder.setAbsolute()
GPIO.setup(ROT_SW,GPIO.IN)
        
lcd = I2cLcd(2, LCD_I2C_ADDR, 4, 20)

menuItem1 = '>Screen Info       '
menuItem2 = ' Freq. Settings    '
menuItem3 = ' Internet Options  '
menuItem4 = ' Other             '
menuItem5 = ' Wave Tech         '
            
setItem1 = '>Freq. Settings    '
setItem2 = ' Start Frequency   '
setItem3 = ' Finish Frequency  '
setItem4 = ' Sample Rate       '
        
GPIO.add_event_detect(ROT_SW, GPIO.FALLING,bouncetime = 300)

class ROT_LCD():
    
    '''TO DOs
    
    1) Correct sample rate to change 2^n increments
    
    3) Add animation to intro screen
    
    4) Implement Internet Options and Other
    
    5) Improve Stability and reliability
    
    6) Reduce script size if possible
    
    7) Add write function to correct range for spectrum
    
    8) Improve lcd_api to allow build-in characters for lcd  -->X
    
    '''
    
    def __init__(self):
        self.cur_position = 0
        self.last_pos = 0
        self.data = 0
        self.last_data = 0
        self.page = 0
        self.lastTime = 0
        self.Old_time = 0
        self.prime = False
        self.void_prime = False
        self.intro_lcd()
        time.sleep(3)
        lcd.clear()
        
    def en_init(self,startnum = 0):
        self.cur_position = 0
        self.last_pos = 0
        self.data = startnum
        self.last_data = 0
        self.lastTime = 0
        
    def intro_lcd(self):
        lcd.clear()
        lcd.move_to(4,1)
        lcd.putstr('This is Intro Screen')
        lcd.move_to(6,2)
        lcd.putstr('Stuff Here')
        
    def main(self,prime):
        self.prime = prime
        lcd.clear()
        while True:
            if self.page == 0:
                self.DrawScreen('Main Screen')
            if GPIO.event_detected(ROT_SW):
                self.page = 1
                #time.sleep(0.2)
                self.DrawScreen('Settings')
                self.loop()
                
    def void_main(self,prime):
        self.void_prime = prime
        if self.page == 0:
            self.DrawScreen('Main Screen')
        if GPIO.event_detected(ROT_SW):
            self.page = 1
            #time.sleep(0.2)
            self.DrawScreen('Settings')
            self.loop()

    def DrawScreen(self, screen, fFunction = 0):
        if screen == 'Main Screen':
            lcd.custom_char(0,customChar.numBLK('TLoff'))
            lcd.custom_char(1,customChar.numBLK('TRoff'))
            lcd.custom_char(2,customChar.numBLK('BLoff'))
            lcd.custom_char(3,customChar.numBLK('BRoff'))
            topos = 9
            #lcd.clear()
            lcd.move_to(0,0)
            lcd.putchar(chr(0))
            lcd.putchar(chr(1))
            lcd.move_to(0,1)
            lcd.putchar(chr(2))
            lcd.putchar(chr(3))
            
            lcd.move_to(9, 0)
            lcd.putstr(time.strftime('%m/%d %H:%M', time.localtime()))
            lcd.move_to(0,0)
            
            Snumlen = len(self.startstr)
            lcd.move_to(topos,3)
            lcd.putstr('to ')
            
            Snum = (topos - 1) - Snumlen
            lcd.move_to(Snum,3)
            lcd.putstr(self.startstr)
            lcd.move_to(12,3)
            lcd.putstr(self.finishstr)
            
        if screen == 'Settings':
            lcd.custom_char(0,customChar.uparrow())
            lcd.custom_char(1,customChar.rightarrow())
            lcd.clear()
            lcd.putstr(menuItem1)
            lcd.putchar(chr(0))
            lcd.move_to(0,1)
            lcd.putstr(menuItem2)
            lcd.putchar(chr(1))
            lcd.move_to(0,2)
            lcd.putstr(menuItem3)
            lcd.putchar(chr(1))
            lcd.move_to(0,3)
            lcd.putstr(menuItem4)
            lcd.putchar(chr(1))
            
        if screen == 'Frequency Settings':
            lcd.clear()
            lcd.putstr(setItem1)
            lcd.putchar(chr(0))
            lcd.move_to(0,1)
            lcd.putstr(setItem2)
            lcd.putchar(chr(1))
            lcd.move_to(0,2)
            lcd.putstr(setItem3)
            lcd.putchar(chr(1))
            lcd.putstr(setItem4)
            lcd.putchar(chr(1))
            
        if screen == 'Set Frequency':
            lcd.clear()
            lcd.move_to(0,0)
            if fFunction == 0:
                lcd.putstr('Start Freq:')
                lcd.move_to(8,1)
                lcd.putstr('>')
                lcd.putstr(self.startf)
            if fFunction == 1:
                lcd.putstr('Finish Freq:')
                lcd.move_to(8,1)
                lcd.putstr('>')
                lcd.putstr(self.finishf)
            if fFunction == 2:
                lcd.putstr('Sample Rate:')
                lcd.move_to(8,1)
                lcd.putstr('>')
                lcd.putstr(str(self.sample_rate))
            lcd.move_to(9,3)
            lcd.putstr('End')
        if screen == 'Internet':
            pass
        if screen == 'Other':
            pass
                
    def loop(self):
        myEncoder.zero()
        self.en_init()
        self.lastTime = time.time()
        while self.page == 1:
            self.ReadEncoder(0)
            if GPIO.event_detected(ROT_SW):
                if self.data == 0:
                    self.page = 0
                    print('Page 0')
                if self.data == 1:
                    self.page = 2
                    print('Page 2')
                if self.data == 2:
                    print('Page 3')
                if self.data == 3:
                    print('Page 4')
            time.sleep(.1)
        if self.page == 0:
            lcd.clear()
            if self.prime == True:
                print('Main')
                self.main(True)
            if self.void_prime == True:
                print('Void Main')
                self.Old_time = time.time()
                self.void_main(True)
        if self.page == 2:
            self.FreqSettings()
        
    def FreqSettings(self):
        myEncoder.zero()
        self.en_init()
        fFunc = 0
        self.DrawScreen('Frequency Settings')
        Page = 1
        self.lastTime = time.time()
        while Page == 1:
            self.ReadEncoder(0)
            time.sleep(.2)
            if GPIO.event_detected(ROT_SW):
                if self.data == 0:
                    Page = 0
                    print('F! 0')
                if self.data == 1:
                    print('F! 2')
                    Page = 2
                if self.data == 2:
                    print('F! 3')
                    Page = 3
                if self.data == 3:
                    print('F! 4')
                    Page = 4
        if Page == 0:
            self.page = 1
            self.DrawScreen('Settings')
            self.loop()
        if Page == 2:
            fFunc = 0
            self.FFreq(fFunc)
            self.DrawScreen('Frequency Settings')
            Page = 1
        if Page == 3:
            fFunc = 1
            self.FFreq(fFunc)
            self.DrawScreen('Frequency Settings')
            Page = 1
        if Page == 4:
            fFunc = 2
            self.FFreq(fFunc)
            self.DrawScreen('Frequency Settings')
            Page = 1
    
    def FFreq(self, fFunction):
        myEncoder.zero()
        self.en_init(1)
        self.DrawScreen('Set Frequency',fFunction)
        fEnd = 1
        self.lastTime = time.time()
        while fEnd == 1:
            self.ReadEncoder(8,1,4,Fsetter = True)
            time.sleep(.2)
            if GPIO.event_detected(ROT_SW):
                if self.data == 1:
                    fEnd = 2
                    print('SF! 0')
                if self.data == 3:
                    print('SF! 2')
                    fEnd = 0
        if fEnd == 0:
            self.FreqSettings()
        if fEnd == 2:
            self.SetFreq(fFunction)
        
    def SetFreq(self, fFunction, init = 0):
        myEncoder.zero()
        self.en_init(int(init))
        self.DrawScreen('Set Frequency', fFunction)
        numpos = 10
        num = 0
        Com = 1
        lcd.blink_cursor_on()
        while Com == 1:
            self.ReadEncoder(8, horizontal = True)
            time.sleep(.2)
            if GPIO.event_detected(ROT_SW):
                if self.data == 0:
                    print('End SF')
                    Com = 0
                if self.data >= 1:
                    numpos = self.data - 1
                    print('Change number ', numpos)
                    if fFunction == 0:
                        num = self.startf[numpos]
                    if fFunction == 1:
                        num = self.finishf[numpos]
                    if fFunction == 2:
                        num = self.sample_rate[numpos]
                    self.selectNum(numpos, num, fFunction)
        if Com == 0:
            lcd.blink_cursor_off()
            lcd.hide_cursor()
            self.FFreq(fFunction)
                    
    def selectNum(self, NumberPos, number, fFnct):
        myEncoder.zero()
        self.en_init(int(number))
        enpos = 0
        last_enpos = int(number)
        start = 1
        lcd.blink_cursor_off()
        lcd.hide_cursor()
        print('Select Number')
        lcd.clearRow(3,9,12)
        while start == 1:
            self.ReadEncoder(NumberPos,Fsetter = True, horizontal = True)
            enpos = self.data
            time.sleep(.2)
            if GPIO.event_detected(ROT_SW):
                start = 0
        if start == 0:
            '''Add addition to frequency by turning number into int then add 
            (self.data * 10**(9-NumberPos)) then back into a str to display'''
            if fFnct == 0:
                if enpos > last_enpos:
                    tmpfrq = int(self.startf)
                    tmpfrq = tmpfrq - (int(number) * 10**(8-NumberPos))
                    tmpfrq = tmpfrq + (self.data * 10**(8-NumberPos))
                    self.startf = str(tmpfrq)
                    self.startstr = str(round((tmpfrq/1000000.0),4))
                if enpos < last_enpos:
                    tmpfrq = int(self.startf)
                    tmpfrq = tmpfrq - (int(number) * 10**(8-NumberPos))
                    tmpfrq = tmpfrq + (self.data * 10**(8-NumberPos))
                    self.startf = str(tmpfrq)
                    self.startstr = str(round((tmpfrq/1000000.0),4))
            if fFnct == 1:
                if enpos > last_enpos:
                    tmpfrq = int(self.finishf)
                    tmpfrq = tmpfrq - (int(number) * 10**(8-NumberPos))
                    tmpfrq = tmpfrq + (self.data * 10**(8-NumberPos))
                    self.finishf = str(tmpfrq)
                    self.finishstr = str(round((tmpfrq/1000000.0),4))
                if enpos < last_enpos:
                    tmpfrq = int(self.finishf)
                    tmpfrq = tmpfrq - (int(number) * 10**(8-NumberPos))
                    tmpfrq = tmpfrq + (self.data * 10**(8-NumberPos))
                    self.finishf = str(tmpfrq)
                    self.finishstr = str(round((tmpfrq/1000000.0),4))
            if fFnct == 2:
                if enpos > last_enpos:
                    tmpfrq = int(self.sample_rate)
                    tmpfrq = tmpfrq - (int(number) * 10**(6-NumberPos))
                    tmpfrq = tmpfrq + (self.data * 10**(6-NumberPos))
                    self.sample_rate = str(tmpfrq)
                if enpos < last_enpos:
                    tmpfrq = int(self.sample_rate)
                    tmpfrq = tmpfrq - (int(number) * 10**(6-NumberPos))
                    tmpfrq = tmpfrq + (self.data * 10**(6-NumberPos))
                    self.sample_rate = str(tmpfrq)
            self.SetFreq(fFnct,NumberPos + 1)
                    
            
    '''Read Encoder to get the position stored in self.data'''    
    def ReadEncoder(self, lcd_Col, start = 0, finish = 0, Fsetter = False, horizontal = False):
        if (Fsetter == False) & (horizontal == False):
            self.cur_position = myEncoder.position
            if (self.cur_position - 3) >= self.last_pos:
                self.data += 1
                if self.data > 3:
                    self.data = 3
                if self.data != self.last_data:
                    lcd.clearCol(lcd_Col)
                    self.lastTime = time.time()
                lcd.move_to(lcd_Col,self.data)
                lcd.putstr('>')
                self.last_data = self.data
                #time.sleep(0.1)
            if (self.cur_position + 3) <= self.last_pos:
                self.data -= 1
                if self.data < 0:
                    self.data = 1
                if self.data != self.last_data:
                    lcd.clearCol(lcd_Col)
                    self.lastTime = time.time()
                lcd.move_to(lcd_Col,self.data)
                lcd.putstr('>')
                self.last_data = self.data
                #time.sleep(0.1)
            self.last_pos = self.cur_position
            if self.data == self.last_data:
                if (time.time() - self.lastTime) >= 10:
                    self.lastTime = time.time()
                    print('Reset')
                    self.Old_time = time.time()
                    lcd.clear()
                    self.page = 0
                    if self.prime == True:
                        print('Main')
                        self.main(True)
                    else:
                        print('Void Main')
                        self.void_main(True)
                        
        if (Fsetter == True) & (horizontal == False):
            self.cur_position = myEncoder.position
            if (self.cur_position - 3) >= self.last_pos:
                self.data += 3
                if self.data > 2:
                    self.data = 3
                if self.data != self.last_data:
                    lcd.clearCol(lcd_Col,start,finish)
                    self.lastTime = time.time()
                lcd.move_to(lcd_Col,self.data)
                lcd.putstr('>')
                self.last_data = self.data
                #time.sleep(0.1)
            if (self.cur_position + 3) <= self.last_pos:
                self.data -= 3
                if self.data < 1:
                    self.data = 1
                if self.data != self.last_data:
                    lcd.clearCol(lcd_Col,start,finish)
                    self.lastTime = time.time()
                lcd.move_to(lcd_Col,self.data)
                lcd.putstr('>')
                self.last_data = self.data
                #time.sleep(0.1)
            self.last_pos = self.cur_position
            if self.data == self.last_data:
                if (time.time() - self.lastTime) >= 10:
                    self.lastTime = time.time()
                    print('Reset')
                    self.Old_time = time.time()
                    lcd.clear()
                    self.page = 0
                    if self.prime == True:
                        print('Main')
                        self.main(True)
                    else:
                        print('Void Main')
                        self.void_main(True)
                        
        if (Fsetter == False) & (horizontal == True):
            self.cur_position = myEncoder.position
            if (self.cur_position - 3) >= self.last_pos:
                self.data += 1
                if self.data > 9:
                    self.data = 9
                lcd.move_to(lcd_Col + self.data,1)
                self.last_data = self.data
                #time.sleep(0.1)
            if (self.cur_position + 3) <= self.last_pos:
                self.data -= 1
                if self.data < 0:
                    self.data = 0
                lcd.move_to(lcd_Col + self.data,1)
                self.last_data = self.data
                #time.sleep(0.1)
            self.last_pos = self.cur_position
            if self.data == 0:
                lcd.move_to(lcd_Col,1)
                
        if (Fsetter == True) & (horizontal == True):
            self.cur_position = myEncoder.position
            if (self.cur_position - 3) >= self.last_pos:
                self.data += 1
                if self.data > 9:
                    self.data = 9
                if self.data != self.last_data:
                    lcd.clearCol(9 + lcd_Col)
                lcd.move_to(9+lcd_Col, 1)
                lcd.putstr(str(self.data))
                self.last_data = self.data
                #time.sleep(0.1)
            if (self.cur_position + 3) <= self.last_pos:
                self.data -= 1
                if self.data < 0:
                    self.data = 0
                if self.data != self.last_data:
                    lcd.clearCol(9 + lcd_Col)
                lcd.move_to(9+lcd_Col, 1)
                lcd.putstr(str(self.data))
                self.last_data = self.data
                #time.sleep(0.1)
            self.last_pos = self.cur_position
            
    def setParameters(self, Start_Frequency = 0, End_Frequency = 0, sample_rate = 0):
        self.startf = str(int(Start_Frequency))
        self.finishf = str(int(End_Frequency))
        self.startstr = str(Start_Frequency/1000000)
        self.finishstr = str(End_Frequency/1000000)
        self.sample_rate = str(int(sample_rate))
        
    def get_Range(self):
        return int(self.startf), int(self.finishf)
        
    def get_Sample_Rate(self):
        return int(self.sample_rate)
        
    def correctRange(self):
        pass
    
    def HackRF_recordOn(self):
        lcd.custom_char(0,customChar.numBLK('TLon'))
        lcd.custom_char(1,customChar.numBLK('Tron'))
        lcd.custom_char(2,customChar.numBLK('BLon'))
        lcd.custom_char(3,customChar.numBLK('BRon'))
        
        if self.page == 0:
            lcd.move_to(0,0)
            lcd.putchar(chr(0))
            lcd.putchar(chr(1))
            lcd.move_to(0,1)
            lcd.putchar(chr(2))
            lcd.putchar(chr(3))
            
    def HackRF_recordOff(self):
        lcd.custom_char(0,customChar.numBLK('TLoff'))
        lcd.custom_char(1,customChar.numBLK('TRoff'))
        lcd.custom_char(2,customChar.numBLK('BLoff'))
        lcd.custom_char(3,customChar.numBLK('BRoff'))
        
        if self.page == 0:
            lcd.move_to(0,0)
            lcd.putchar(chr(0))
            lcd.putchar(chr(1))
            lcd.move_to(0,1)
            lcd.putchar(chr(2))
            lcd.putchar(chr(3))
            
    def RestartTime(self,oldTime):
        if oldTime > self.Old_time:
            return oldTime
        else: 
            return self.Old_time
        
if __name__ == "__main__":
    Sf = 420e6
    Ff = 512e6
    samprate = 2.048e6
    rotlcd = ROT_LCD()
    rotlcd.setParameters(Sf,Ff,samprate)
    rotlcd.main(True)
