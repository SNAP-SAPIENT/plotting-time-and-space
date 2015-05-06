/**
 * Plotting Time and Space - EXEC
 * Author: Robert Ross
 *
 * This file handles all of the commands that are passed
 *  from the comms
 */

/*
 * Adjust where they system thinks the motors currently are
 */
void exec_teleport(int x, int y)
{
  float leftPos = sqrt(sq(pageTopPaddingMM + y) + sq(pageLeftPaddingMM + x)) / lengthPerStepMM;
  float rightPos = sqrt(sq(pageTopPaddingMM + y) + sq(motorWidthMM - pageLeftPaddingMM - x)) / lengthPerStepMM;
  leftMotor.setCurrentPosition(leftPos);
  rightMotor.setCurrentPosition(rightPos);
  
  // Set the new x and y
  currentX = x;
  currentY = y;
  
#ifdef DEBUG
  Serial.println((String)"TELEPORT: left motor = " + leftMotor.currentPosition() + " right motor = " + rightMotor.currentPosition());
#endif
}

/*
 * Move the drawing tool to the xy position given in a line
 */
void exec_moveline(float x, float y)
{  
  // Calculate the new positions
  float newLeftPos = sqrt(sq(pageTopPaddingMM + y) + sq(pageLeftPaddingMM + x)) / lengthPerStepMM;
  float newRightPos = sqrt(sq(pageTopPaddingMM + y) + sq(motorWidthMM - pageLeftPaddingMM - x)) / lengthPerStepMM;
  
  // Set the new positions
  leftMotor.moveTo(newLeftPos);
  rightMotor.moveTo(newRightPos);
  
  // Now calcuate the ratio between the motor distance to move
  float moveRatio = (newLeftPos - leftMotor.currentPosition()) / (newRightPos - rightMotor.currentPosition());
  // Fix the failure of the abs function
  if(moveRatio < 0.0) 
  {
    moveRatio = (float)0.0 - (float)moveRatio;
  }
  
  // Set the speeds and ratios accordingly
  if(moveRatio < 1.0)
  {
    leftMotor.setMaxSpeed(motorMaxStepsPerSec * moveRatio);
    rightMotor.setMaxSpeed(motorMaxStepsPerSec);
    leftMotor.setAcceleration(motorMaxAcceleration * moveRatio);
    rightMotor.setAcceleration(motorMaxAcceleration);
  }
  else
  {
    leftMotor.setMaxSpeed(motorMaxStepsPerSec);
    rightMotor.setMaxSpeed(motorMaxStepsPerSec / moveRatio);
    leftMotor.setAcceleration(motorMaxAcceleration);
    rightMotor.setAcceleration(motorMaxAcceleration / moveRatio);
  }
  
  // Run the motors
  while(leftMotor.distanceToGo() != 0 || rightMotor.distanceToGo() != 0)
  {
    rightMotor.run();
    leftMotor.run();
  }
  
  // Set the new x and y
  currentX = x;
  currentY = y;
  
#ifdef DEBUG
  Serial.println((String)"MOVE_LINE: left motor = " + leftMotor.currentPosition() + " right motor = " + rightMotor.currentPosition());
#endif
}

/*
 * Move the drawing tool to the xy position given as quickly
 * as possible
 */
void exec_moverapid(float x, float y)
{
  // Calculate the new positions
  float newLeftPos = sqrt(sq(pageTopPaddingMM + y) + sq(pageLeftPaddingMM + x)) / lengthPerStepMM;
  float newRightPos = sqrt(sq(pageTopPaddingMM + y) + sq(motorWidthMM - pageLeftPaddingMM - x)) / lengthPerStepMM;
  
  // Set the new positions
  leftMotor.moveTo(newLeftPos);
  rightMotor.moveTo(newRightPos);
  
  // Move as fast as possible
  leftMotor.setMaxSpeed(motorMaxStepsPerSec);
  rightMotor.setMaxSpeed(motorMaxStepsPerSec);
  leftMotor.setAcceleration(motorMaxAcceleration);
  rightMotor.setAcceleration(motorMaxAcceleration);

  // Move the motors to the new positions
  while(leftMotor.distanceToGo() != 0 || rightMotor.distanceToGo() != 0)
  {
    leftMotor.run();
    rightMotor.run();
  }
  
  // Set the new x and y
  currentX = x;
  currentY = y;
  
#ifdef DEBUG
  Serial.println((String)"MOVE_RAPID: left motor = " + leftMotor.currentPosition() + " right motor = " + rightMotor.currentPosition());
#endif
}

/*
 * Move the drawing tool in a clockwise arc to the xy 
 * location given in an arc around the circle given with 
 * a center at point ij and a radius of the distance 
 * between ij and the current position
 */
void exec_movearc_clockwise(float x, float y, float i, float j)
{
  // TODO move in an arch clockwise away from the circle given
  
  // Set the new x and y
  currentX = x;
  currentY = y;
  
#ifdef DEBUG
  Serial.println((String)"MOVE_ARC_CLOCK: left motor = " + leftMotor.currentPosition() + " right motor = " + rightMotor.currentPosition());
#endif
}

/*
 * Move the drawing tool in a counterclockwise arc to the xy 
 * location given in an arc around the circle given with 
 * a center at point ij and a radius of the distance 
 * between ij and the current position
 */
void exec_movearc_counterclockwise(float x, float y, float i, float j)
{
  // TODO you know
  
  // Set the new x and y
  currentX = x;
  currentY = y;
  
#ifdef DEBUG
  Serial.println((String)"MOVE_ARC_COUNTERCLOCK: left motor = " + leftMotor.currentPosition() + " right motor = " + rightMotor.currentPosition());
#endif
}

/*
 * Dwell in space for x miliseconds. No movement in x,y,z
 */
void exec_dwell(int time)
{
  // Just delay
  delay(time);
#ifdef DEBUG
  Serial.println((String)"DWELLED: TIME:" + time);
#endif
}

/*
 * Disables the motors and lifts the pen if possible. The
 * drawing tool will then move freely. This can mess up
 * where the code believes the motors are so be careful
 */
void exec_disable()
{
  // Disable the motors and lift the pen if it exists
 #ifdef PENLIFT
   penlift_up();
 #endif
   rMotor->release();
   lMotor->release();

#ifdef DEBUG
  Serial.println((String)"MOTORS_DISABLED");
#endif

  // Send that ready for next command
  Serial.println("READY");
}

/*
 * Engages the motors by wiggling them. This is usually called
 * after the motors have been disabled and will also likely
 * be followed by a teleport to readjust after the disable
 */
void exec_enable()
{
  // Enable the motors and lock them by wiggling them
  leftMotor.runToNewPosition(leftMotor.currentPosition()+4);
  rightMotor.runToNewPosition(rightMotor.currentPosition()+4);
  leftMotor.runToNewPosition(leftMotor.currentPosition()-4);
  rightMotor.runToNewPosition(rightMotor.currentPosition()-4);

#ifdef DEBUG
  Serial.println((String)"MOTORS_ENABLED: left motor = " + leftMotor.currentPosition() + " right motor = " + rightMotor.currentPosition());
#endif

  // Send that ready for next command
  Serial.println("READY");
}

/*
 * Sets the system to work in inches instead of mm
 */
 void exec_set_inches()
 {
   // Just change the variable and output the change to serial
   inches = true;
   Serial.println("The system is now working in Inches");
   
   // Send that ready for next command
   Serial.println("READY");
 }
 
 /*
  * Sets the system to work in mm
  */
void exec_set_mm()
{
   // just change the variable and output the change
   inches = false;
   Serial.println("The system is now working in Milimeters");

   // Send that ready for next command
   Serial.println("READY");
}

/*
 * Sets the system to have all measurements be relative
 */
void exec_set_relative()
{
  // Just change the variable and output the change
  relative = true;
  Serial.println("The system is now in relative mode");
  
  // Send that ready for next command
  Serial.println("READY");
}

/*
 * Sets the system to have all measurements be absolute
 */
void exec_set_absolute()
{
  // Just change the variable and output the change
  relative = false;
  Serial.println("The system is now in absolute mode");
  
  // Send that ready for next command
  Serial.println("READY");
}
