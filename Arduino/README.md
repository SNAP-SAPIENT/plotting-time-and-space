#Time & Space Plotter

##Arduino Code
The arduino code consists of the code to control two servo motors and the solenoid. These three things control the drawing mechanism.
The arduino controlls the solenoid directly while it uses the Adafruit motor controller shield v2 to control the motors.
The serial interface is used to send commands to the arduino.

##comms.ino
comms.ino handles the communications over serial. To help with communication, a small easy to use library is used. The library has been modified due to it not being the best of libraries and this is why it is included. There will be effort in the future to use a more robust and standard library

##penlift.ino
penlift.ino handles the penlift controlling.

##exec.ino
exec.ino handles the brunt of the math work. It has the information to move the drawing mechanism in streight lines and to points. The draw arc functions need to be finished in the future

##configuration.ino
configuration.ino handles all of the configuration parameters. If you wish to adjust the starting information, you should adjust it within here

##time_and_space.ino
time_and_space.ino is the main ino file that contains the setup and loop functions. everything is wrapped together here. Some defines are located here as well in order to make them truly global due to how the arduino compiler works

###Notes
The arduino code is not well optiomized. The Sram is getting full and the whole code needs another look over. It is working, but the code might be a cause of the slight drifting issue that exists. Some of the code is not even finished. The task list is below...

- Use EEPROM for configuration information
- Finish the arc functions
- Remove need for accell stepper (remove arching issues for lines)
