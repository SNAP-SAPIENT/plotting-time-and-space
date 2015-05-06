/**
 * Plotting Time and Space - PENLIFT
 * Author: Robert Ross
 *
 * This file contains a set of functions associated with
 *  a penlift mechanisim if the mechanisim is deemed to exist
 */
#ifdef PENLIFT
// Include the servo class
#include <Servo.h>

// Create the servo to use
Servo penlift;

// Create the setup method
void penlift_setup()
{
  // Attach the servo to the correct pin
  penlift.attach(penliftServoPin);
}

void penlift_up()
{
  // Move to the position and then add a delay for the servo
  //  to move to that position
  penlift.write(penliftUpPosition);
  delay(penliftDelay);
  
  // Send that ready for next command
  Serial.println("READY");
}

void penlift_down()
{
  // Move to the position and then add a delay for the servo
  //  to move to that position
  penlift.write(penliftDownPosition);
  delay(penliftDelay);
  
  // Send that ready for next command
  Serial.println("READY");
}

void penlift_setAngle(int angle)
{
  // Set the angle of the pen to the passed angle and delay
  //  the standard ammount
  penlift.write(angle);
  delay(penliftDelay);
  
  // Send that ready for next command
  Serial.println("READY");
}
#endif
