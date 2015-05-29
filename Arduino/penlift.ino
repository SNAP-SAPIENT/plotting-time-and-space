/**
 * Plotting Time and Space - PENLIFT
 * Author: Robert Ross
 *
 * This file contains a set of functions associated with
 *  a penlift mechanisim if the mechanisim is deemed to exist
 */
#ifdef PENLIFT

// Create the penlift pin
int penPin = 8;

// Create the setup method
void penlift_setup()
{
  // Attach the lift to the correct pin
  pinMode(penPin, OUTPUT);
}

void penlift_up()
{
  // Move to the position
  digitalWrite(penPin, HIGH);  
  delay(penliftDelay);
  
  // Send that ready for next command
  comms_ready();
}

void penlift_down()
{
  // Move to the position 
  digitalWrite(penPin, LOW);
  delay(penliftDelay);
  
  // Send that ready for next command
  comms_ready();
}

//void penlift_setAngle(int angle)
//{
//  // Set the angle of the pen to the passed angle and delay
//  //  the standard ammount
//  penlift.write(angle);
//  delay(penliftDelay);
//  
//  // Send that ready for next command
//  comms_ready();
//}
#endif
