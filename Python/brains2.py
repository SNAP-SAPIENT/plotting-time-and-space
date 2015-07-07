"""
Plotting Time and Space - Brains
Author: Robert Ross

The brains of the system. Takes in all attributes and combines them
using the config file to do initialization and contains utility functions
that help run everything.
"""

# Import all of the classes we need
import time

# Import each item seperatly
import config

# Comms
from communication import led
from communication import plug
from communication import communication

# Helper Classes
import draw as dr
import img as im

class Brains:
    """
    TODO
    """
    modes = [None]  # An array of the different mode objects

    #################################################################
    # Declerations
    #################################################################
    # Inputs
    cam = camera.Camera()
    humidAndTemp = humidity_and_temperature.HumidityAndTemperatureSensor()
    mic = microphone.MicrophoneSensor(addr=0x4A, ch=3)
    lux = light.LightSensor(addr=0x39, gain=0)  # Autogain mode
    reset = switch.SwitchSensor(dataPin=26)

    ###############################################################
    # Helper Functions
    ###############################################################
    def preformReset():
        """
        Does a soft reset of the system, bringing all variables to their
        origional state and allows the drawing machine to be recalibrated
        """
        # The first thing to do in reset is wait for the person to let go of
        # the reset button
        while True:
            if reset.off():
                break

        # Now that the reset button is pressed, let us disable the motors
        comms.disable()

        # Teleport where we think the motors are
        comms.teleport(config.startingX, config.startingY)

        # Wait about 10 seconds so the user can react
        time.sleep(10)

        # Now wait until the reset button is pressed again
        while True:
            if reset.on():
                break

        # Turn off all of the led's
        ledSped.off()
        ledJttr.off()
        ledSlop.off()
        ledThrd.off()
        ledSpac.off()
        ledCplx.off()
        ledModeHorizontal.off()
        ledModeVertical.off()
        ledModeGrid.off()
        ledModeWeave.off()

        # Now re-enable the motors
        comms.enable()

        # Now select the new mode
        img.changeToNextMode()
        setModeLight()

    def setModeLight():
        """Cycle through the modes and set the correct mode light on"""
        # Now select the new mode
        if img.mode == 0:
            ledModeHorizontal.on()
        elif img.mode == 1:
            ledModeVertical.on()
        elif img.mode == 2:
            ledModeGrid.on()
        elif img.mode == 3:
            ledModeWeave.on()

    def detectPlugsAndSensors():
        """
        Send signals through each of the plugs to detect where it might
        be plugged in
        After it finds if something is plugged in, it finds the sensor value
        and uses that
        """
        # First turn off all of the plugs and led's
        plugLux.off()
        plugTmp.off()
        plugHum.off()
        plugSnd.off()
        ledSlop.off()
        ledSpac.off()
        ledSped.off()
        ledJttr.off()
        ledThrd.off()
        ledCplx.off()

        values = {
                'slop': slop.getValue(), 'spac': spac.getValue(),
                'sped': sped.getValue(), 'jttr': jttr.getValue(),
                'thrd': thrd.getValue(), 'cplx': cplx.getValue()
                }

        # Get the sensor readings
        h, t = humidAndTemp.getValues()
        l = lux.getValue()
        s = mic.getDistPeakValue()

        # Now check for the lux
        plugLux.on()
        if jackSlop.on():
            ledSlop.on()
            values['slop'] *= l
        elif jackSpac.on():
            ledSpac.on()
            values['spac'] *= l
        elif jackSped.on():
            ledSped.on()
            values['sped'] *= l
        elif jackJttr.on():
            ledJttr.on()
            values['jttr'] *= l
        elif jackThrd.on():
            ledThrd.on()
            values['thrd'] *= l
        elif jackCplx.on():
            ledCplx.on()
            values['cplx'] *= l
        plugLux.off()

        # Now check for the tmp
        plugTmp.on()
        if jackSlop.on():
            ledSlop.on()
            values['slop'] *= t
        elif jackSpac.on():
            ledSpac.on()
            values['spac'] *= t
        elif jackSped.on():
            ledSped.on()
            values['sped'] *= t
        elif jackJttr.on():
            ledJttr.on()
            values['jttr'] *= t
        elif jackThrd.on():
            ledThrd.on()
            values['thrd'] *= t
        elif jackCplx.on():
            ledCplx.on()
            values['cplx'] *= t
        plugTmp.off()

        # Now check for the hum
        plugHum.on()
        if jackSlop.on():
            ledSlop.on()
            values['slop'] *= h
        elif jackSpac.on():
            ledSpac.on()
            values['spac'] *= h
        elif jackSped.on():
            ledSped.on()
            values['sped'] *= h
        elif jackJttr.on():
            ledJttr.on()
            values['jttr'] *= h
        elif jackThrd.on():
            ledThrd.on()
            values['thrd'] *= h
        elif jackCplx.on():
            ledCplx.on()
            values['cplx'] *= h
        plugHum.off()

        # Now check for the snd
        plugSnd.on()
        if jackSlop.on():
            ledSlop.on()
            values['slop'] *= s
        elif jackSpac.on():
            ledSpac.on()
            values['spac'] *= s
        elif jackSped.on():
            ledSped.on()
            values['sped'] *= s
        elif jackJttr.on():
            ledJttr.on()
            values['jttr'] *= s
        elif jackThrd.on():
            ledThrd.on()
            values['thrd'] *= s
        elif jackCplx.on():
            ledCplx.on()
            values['cplx'] *= s
        plugSnd.off()

        # Limit the values to max
        for key, value in values.iteritems():
            if value > config.MAX:
                value = config.MAX

        return values


    def error():
        """
        Flashes all of the led's to indicate that there has been an error
        and does not stop until the system is turned off or the reset button
        is used
        """
        while True:
            # Flash leds
            ledSped.on()
            ledJttr.on()
            ledSlop.on()
            ledThrd.on()
            ledSpac.on()
            ledCplx.on()
            ledModeHorizontal.off()
            ledModeVertical.off()
            ledModeGrid.off()
            ledModeWeave.off()

            time.sleep(0.5)

            ledSped.off()
            ledJttr.off()
            ledSlop.off()
            ledThrd.off()
            ledSpac.off()
            ledCplx.off()
            ledModeHorizontal.on()
            ledModeVertical.on()
            ledModeGrid.on()
            ledModeWeave.on()

            # Check for reset
            if reset.on():
                # Break from the loop and the perform the reset function
                break

            time.sleep(0.5)

        preformReset()

    ###############################################################
    # Main Program Function
    ###############################################################
    def main():
        """
        This function contains the main loop that is run to controll the
        plotting time and space drawing machine and console.

        The loop will go through and handle each input and output
        """
        # First wait for the reset button to be pressed to indicate that everything
        # is ready
        while True:
            if reset.on():
                break

        # Now set up some things
        currentChunk = None
        chunk = None
        lastPixelInChunk = None

        # Set the initial mode light
        setModeLight()

        # Now we can start drawing in an infinate loop
        try:
            while True:
                #######################################################
                # Plugs and sensors
                #######################################################
                # Detect the plugs that are plugged in
                plugs = detectPlugsAndSensors()

                # Set the values based on the sensors
                img.setComplexity = plugs['cplx']
                img.setSpacing = plugs['spac']
                img.setThreshold = plugs['thrd']
                img.setSpeed = plugs['sped']
                draw.setJitter = plugs['jttr']
                draw.setSlope = plugs['slop']

                #######################################################
                # Check or change mode
                #######################################################
                for col in img.img:
                    for cell in col:
                        if not cell.drawn:
                            break
                    else:
                        continue
                    break
                else:
                    # All chunks are drawn. Let us now change the mode
                    img.changeToNextMode()
                    currentChunk = None
                    chunk = None
                    lastPixelInChunk = None
                    setModeLight()

                #######################################################
                # Take Picture
                #######################################################
                # Now check if a new picture needs to be taken
                if img.timeForNextImage():
                    added = img.addNextImage()

                #######################################################
                # Draw Pixel
                #######################################################
                # Now find the next pixel to draw
                # First start at the chunk level
                if currentChunk is None:
                    # Assign the first chunk
                    if img.chunksAddedOrder is None:
                        # Wait for an image to be added
                        continue
                    else:
                        currentChunk = img.chunksAddedOrder[0]
                        chunk = img.img[currentChunk[0]][currentChunk[1]]
                elif lastPixelInChunk is not None:
                    if chunk.pixels.shape == lastPixelInChunk:
                        # We finished this chunk
                        chunk.drawChunk()
                        # Grab the next chunk if there is one
                        pos = img.chunksAddedOrder.index(currentChunk)
                        if pos+1 == len(img.chunksAddedOrder):
                            # Wait for a new picture to be taken
                            continue
                        currentChunk = img.chunksAddedOrder[pos+1]
                        chunk = img.img[currentChunk[0]][currentChunk[1]]
                        # Reset the pixel position
                        lastPixelInChunk = None

                # Set the pixel dimensions based on the chunk
                draw.setPixelDimensions(chunk.pixels.shape[1]*img.chunksWide,
                        chunk.pixels.shape[0]*img.chunksHigh)

                # Adjust the slope if we are drawing down
                if img.mode == img.MODE_VERTICAL:
                    draw.setSlope(draw.slope + ((config.MAX-config.MIN)*0.25))
                elif img.mode == img.MODE_WEAVE:
                    if currentChunk[0] >= currentChunk[1]:
                        draw.setSlope(draw.slope + ((config.MAX-config.MIN)*0.25))

                # Finally find the pixel to draw
                if lastPixelInChunk is None:
                    lastPixelInChunk = (0,0)
                else:
                    # Determine if we are drawing down or not
                    if img.mode == img.MODE_VERTICAL:
                        # Drawing down
                        lastPixelInChunk[1] += 1
                        if lastPixelInChunk[1] > chunk.pixels.shape[1]:
                            lastPixelInChunk[1] = 0
                            lastPixelInChunk[0] += 1
                    elif (img.mode == img.MODE_WEAVE and currentChunk[0] >=
                            currentChunk[1]):
                        # Also drawing down
                        lastPixelInChunk[1] += 1
                        if lastPixelInChunk[1] > chunk.pixels.shape[1]:
                            lastPixelInChunk[1] = 0
                            lastPixelInChunk[0] += 1
                    else:
                        # Drawing horizontal
                        lastPixelInChunk[0] += 1
                        if lastPixelInChunk[0] > chunk.pixels.shape[0]:
                            lastPixelInChunk[0] = 0
                            lastPixelInChunk[1] += 1

                # Now that the pixel is selected, let us draw it
                pixVal = chunk.pixels[lastPixelInChunk[0]][lastPixelInChunk[1]]
                xVal = ((chunk.pixels.shape[1] * currentChunk[1]) +
                    lastPixelInChunk[1])
                yVal = ((chunk.pixels.shape[0] * currentChunk[0]) +
                    lastPixelInChunk[0])

                # The big call
                draw.pixel(pixVal, xVal, yVal)

        except:
            # TODO

if __name__ == '__main__':
    main()
