#Time & Space Plotter

##Intro
The "Time and Space Plotter" is a SNAP project focused on alternative machine control, where users are able to control a drawing machine using a combination of sensors.

Using a control panel with a switchboard, the user will be able to change which sensors control which aspects of the drawing.  The control panel will allow the user to plug in different sensor types using banana plugs.  Furthermore each sensor will be connected to a potentiometer, allowing the user to change the affect each sensor has on the final output.

The plotter will be connected to a camera, which will take a picture of a space and create the starting image that will be plotted. Over time the camera will take a series of images and apply a reversal filter, so it can capture the activity that has changed within the frame.  The result is drawing depicting movement through the space over time.

##Sensors
The Sensors used for the project are as follows:

- Microphone
- Humidity
- Lux Sensor
- Temperature Sensor

The sensors will be linked to specific drawing parameters using a series of chords and banana plugs.  This will allow users to experiment by rerouting which sensor is control which drawing parameter.

Each sensor will be connected to a potentiometer that a user can adjust to create additional variations in the drawing.


##Drawing Parameter
The parameters of the drawing which allow for user adjustment are:

- **Drawing Mode** (Fixed)
    - Horizontal - picture starts from left and draws to the right (random).
    - Vertical - picture starts from top and draws to the bottom (sequential).
    - Quilt - Picture fills in through random patchwork (random).
    - Nested - picture draws by alternating vertical and horizontal sections of the drawing starting at the top-left corner (sequential).
- **Line Slope** (Variable)
    - Users are able to adjust the angle of orientation for each line drawn, from an angle of 0 degrees (horizontal line), to an angle of 90 degrees (vertical line).
    - The default value is 45 degrees if nothing is plugged in.
- **Line Spacing** (Range)
    - Users are able to adjust the spacing between lines in Millimeters (mm).  Adjustment range TBD - need min and max.
- **Drawing Speed** (Range)
    - Drawing speed will allow the user to control the execution speed.  
    - This will have an affect in the resolution or quality of the image drawn.
- **Jitter** (Range)
    - The jitter control allows the user to control variation in the line by introducing random pen movement.  Jitter increments are TBD.
- **Contrast Threshold** (Variable)
    - The contrast threshold will allow the user to affect the final image rendered by changing the effect of the contrast filter prior to the image being drawn.
- **Complexity** (Range)
    - Allows the user to adjust the number of component images/panels that will be used to asseble the picture.
    - The minimum value is 1 component, the maximimum is TBD.
    - The complexity adjustment will change the number of pictures the device takes and the number of times data is captured from all sensors.  Each time the camera fires, a data reading will be taken from each sensor as well.

Each Drawing Parameter will have a default value, so that if nothing is plugged in/adjusted there will be a default value for that parameter (as an example: the default value for line direction is horizontal lines).

The sensors all collect data each time the camera is fired and relay this to the plotter.


##Hardware
The hardware will consist of two separate pieces that work together: the **Dashboard**, the **Camera**, and the **Plotter**.

###Dashboard
The Dashboard is the hardware that the user will use to reroute the sensors and affect a change in the final output of the drawing.  The user will do this by changing the connections of each sensor using a switchboard.  The user will have further refinement via a potentiometer to affect the amount of gain that each sensor has.  Users are thus able to drastically change the outcome of the drawing via the dashboard.

####Dashboard Materials
The dashboard will be comprised of the following materials:

- Plexiglass cabinet
- Banana Plugs
- Chord Pulley System
- Rotary Potentiometers
- Arduino + RaspberryPi units
- Sensors (see full list above)
- Connectors (for the dashboard to interface with the plotter)
- Shutter Mechanism (to start the picture)
- Dataport (access arduino)

####Dashboard Controls
The Control mechanism for the plotter are as follows:

- **Start/Reset Button**
    - Starts the process of resetting printhead to the origin and begins a new drawing.
    - Hitting the reset button will not advanced a drawing style until an image has been completed with that drawing style.
    - Once a drawing is complete, if the reset button is hit it will advance to the next drawing style available in the sequence.
- **Banana Connection**
    - Allows the user to connect a sensor to a drawing parameter
- **Adjustment Knob**
    - Allows the user to manually/individually tweak the settings for any drawing parameter.
    - The user is always able to adjust a paremeter down to 0 level.
    - Turned all the way up, the drawing parameter will have 100% effect which could produce an exagerated image.


###Plotter
The Plotter is the device that is being controlled by the Dashboard.  The plotter will contain the necessary motors, gearing system and pen holder to perform the task of drawing the image.  The plotter will be connected to the dashboard via a chord ***with enough length to place it in a separate area from the dashboard (another wall in the same room)***.

####Plotter Materials
The plotter will be compromised of the following materials:

- 2x Motors
- Pen Cradle
- Servo for Pen Cradle
- Pen
- 2x Bead Chain
- Plexiglass Housing
- Suction Cups

###Camera
The camera is connected to the dashboard and will allow the user to position it separately from both the Plotter and the Dashboard.  The Camera will feed the image through the dashboard to be processed by the various sensors, the output will be sent to the plotter to actually draw the image. A mounting mechanism allows the user to reposition the angle of the camera.

####Camera Materials
The Camera will be made from the following materials:

- Camera
- Suction Cups
- Plexiglass Housing
- Mounting Mechanism


##How to Use


##Nice to Have

- **Manual Reset of Canvas Size**
    - The user can reset the top left corner and bottom right corner of canvas before starting drawing procedure.  This allows the machine to draw at varios sizes depending on the medium used and positioning of the device.
- **Motor Distance Sensor**
    - Mount a distance sensor between the two motors to automatically calulate the distance between the two motors and use that to determine/calibrate canvas size.
- **Curves**
    - Need to add curves, currently the sowtware uses aliasing to render curves
- **Invert** (Toggle)
    -The invert control allows the user to switch between using a normal image as the starting point or changing the image to a negative.
- **RFID**
    - Will look into but may be too complex