""" This is a test script to see if all the sensors give data and are wired
correctly
"""

# Import the proper classes
from sensors.light import LightSensor
from sensors.potentiometer import PotentiometerSensor
from sensors.switch import SwitchSensor
from sensors.microphone import MicrophoneSensor
from sensors.humidity_and_temperature import HumidityAndTemperatureSensor

# Create the objects
slop = PotentiometerSensor(addr=0x48, ch=2, gain=4096, sps=250)
spac = PotentiometerSensor(addr=0x4A, ch=2, gain=4096, sps=250)
sped = PotentiometerSensor(addr=0x4A, ch=0, gain=4096, sps=250)
jttr = PotentiometerSensor(addr=0x4A, ch=1, gain=4096, sps=250)
trhd = PotentiometerSensor(addr=0x48, ch=1, gain=4096, sps=250)
cplx = PotentiometerSensor(addr=0x48, ch=3, gain=4096, sps=250)

lux = LightSensor(addr=0x39, gain=0)
hum_and_tmp = HumidityAndTemperatureSensor(dataPin=4)
snd = MicrophoneSensor(addr=0x48, ch=0, gain=4096, sps=250)

reset = SwitchSensor(dataPin=5)

def main():
    while True:
        # Go through and check every sensor
        print "Lux=", lux.getValue()
        humidity, temperature = hum_and_tmp.getValues()
        print "Tmp=", temperature
        print "Hum=", humidity
        print "Snd=", snd.getValue()

        print "Slop=", slop.getValue()
        print "Spac=", spac.getValue()
        print "Sped=", sped.getValue()
        print "Jttr=", jttr.getValue()
        print "Trhd=", trhd.getValue()
        print "Cplx=", cplx.getValue()

        if reset.on:
            print "Reset is being pressed"
        else:
            print "Reset is not being pressed"

if __name__ == '__main__':
    main()
