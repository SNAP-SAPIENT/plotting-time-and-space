"""
Error script
Author: Robert Ross

If there is an error that occurs, this script should run and flash all
of the lights on the box to indicate the error
"""

from communication import led
import time

light1 = led.LED(18)
light2 = led.LED(23)
light3 = led.LED(24)
light4 = led.LED(25)
light5 = led.LED(8)
light6 = led.LED(7)
light7 = led.LED(12)
light8 = led.LED(16)
light9 = led.LED(20)
light10 = led.LED(21)

def main():
    while True:
        # Flash leds
        light1.on()
        light2.on()
        light3.on()
        light4.on()
        light5.on()
        light6.on()
        light7.on()
        light8.on()
        light9.on()
        light10.on()

        time.sleep(0.5)

        light1.off()
        light2.off()
        light3.off()
        light4.off()
        light5.off()
        light6.off()
        light7.off()
        light8.off()
        light9.off()
        light10.off()

        time.sleep(0.55)

if __name__ == '__main__':
    main()
