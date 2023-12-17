from machine import Pin,SPI,PWM
import time
import gc

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9
    
    
#=============== MAIN ============

if __name__ == '__main__':
        # Setup the LCD display
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(65535)#max 65535

        gc.collect()

        import test_lib
        while True:
                test_lib.frame1()
                time.sleep(0.03)
                gc.collect()
                test_lib.frame2()
                time.sleep(0.03)
                gc.collect()
                test_lib.frame3()
                time.sleep(0.03)
                gc.collect()
                test_lib.frame4()
                time.sleep(0.03)
                gc.collect()
                test_lib.frame5()
                time.sleep(0.03)
                gc.collect()
                test_lib.frame6()
                time.sleep(0.03)
                gc.collect()
                test_lib.frame7()
                time.sleep(0.03)
                gc.collect()
                test_lib.frame8()
                time.sleep(0.03)
                gc.collect()
