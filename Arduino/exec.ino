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
  long leftPos = round(sqrt(sq(pageTopPaddingMM+y) + sq(pageLeftPaddingMM+x)) / lengthPerStepMM);
  long rightPos = round(sqrt(sq(pageTopPaddingMM+y) + sq(motorWidthMM-pageLeftPaddingMM-x)) / lengthPerStepMM);
  leftMotorPos = leftPos;
  rightMotorPos = rightPos;
  
  // Set the new x and y
  currentX = x;
  currentY = y;
  
#ifdef DEBUG
  Serial.println((String)"TELEPORT: left motor = " + leftMotor.currentPosition() + " right motor = " + rightMotor.currentPosition());
#endif
}

/*
 * Move the drawing tool to the xy position given in a line
 * This method uses a different stepping method in an
 * attempt to keep the line straighter
 */
void exec_moveline(float x, float y)
{  
  // Calculate the start and end positions and initial conditions
  long x1 = round(sqrt(sq(pageTopPaddingMM+y) + sq(pageLeftPaddingMM+x)) / lengthPerStepMM);
  long y1 = round(sqrt(sq(pageTopPaddingMM+y) + sq(motorWidthMM-pageLeftPaddingMM-x)) / lengthPerStepMM);
  long x0 = leftMotorPos;
  long y0 = rightMotorPos;
  long dx = x1 - x0;
  long dy = y1 - y0;
  long dxabs = abs(dx);
  long dyabs = abs(dy);
  int signx = dx<0?BACKWARD:FORWARD;
  int signy = dy<0?FORWARD:BACKWARD;
  float err = 0.0;
  if(dxabs > dyabs)
  {
    // Shallow line
    float deltaerr = (float)dyabs / (float)dxabs;
    for(int i = 0; i <= dxabs; i++)
    {
      leftStep(signx);
      err += deltaerr;
      if(err > 0.5)
      {
        rightStep(signy);
        err -= 1;
      }
    }
  }
  else
  {
    // Steep line
    float deltaerr = (float)dxabs / (float)dyabs;
    for(int i = 0; i <= dyabs; i++)
    {
      rightStep(signy);
      err += deltaerr;
      if(err > 0.5)
      {
        leftStep(signx);
        err -= 1;
      }
    }
  }
  
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
  // For now just move line will be the same as move rapid
  exec_moveline(x, y);
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
  // Disable the motors
   rMotor->release();
   lMotor->release();

#ifdef DEBUG
  Serial.println(F("MOTORS_DISABLED"));
#endif

  // Send that ready for next command
  comms_ready();
}

/*
 * Engages the motors by wiggling them. This is usually called
 * after the motors have been disabled and will also likely
 * be followed by a teleport to readjust after the disable
 */
void exec_enable()
{
  // Enable the motors and lock them by wiggling them
  rightStep(FORWARD);
  leftStep(FORWARD);
  rightStep(BACKWARD);
  leftStep(BACKWARD);

#ifdef DEBUG
  Serial.println((String)"MOTORS_ENABLED: left motor = " + leftMotor.currentPosition() + " right motor = " + rightMotor.currentPosition());
#endif

  // Send that ready for next command
  comms_ready();
}

/*
 * Sets the system to work in inches instead of mm
 */
 void exec_set_inches()
 {
   // Just change the variable and output the change to serial
   inches = true;
   Serial.println(F("The system is now working in Inches"));
   
   // Send that ready for next command
   comms_ready();
 }
 
 /*
  * Sets the system to work in mm
  */
void exec_set_mm()
{
   // just change the variable and output the change
   inches = false;
   Serial.println(F("The system is now working in Milimeters"));

   // Send that ready for next command
   comms_ready();
}

/*
 * Sets the system to have all measurements be relative
 */
void exec_set_relative()
{
  // Just change the variable and output the change
  relative = true;
  Serial.println(F("The system is now in relative mode"));
  
  // Send that ready for next command
  comms_ready();
}

/*
 * Sets the system to have all measurements be absolute
 */
void exec_set_absolute()
{
  // Just change the variable and output the change
  relative = false;
  Serial.println(F("The system is now in absolute mode"));
  
  // Send that ready for next command
  comms_ready();
}
