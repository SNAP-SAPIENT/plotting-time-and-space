/**
 * Plotting Time and Space - CONFIGURATION
 * Author: Robert Ross
 *
 * This file contains all of the configuration options for
 *  the plotting time and space controller
 */
 
// Motor Information
const int motorStepsPerRev = 200;
const float motorMaxStepsPerSec = 200.0;
const float motorMaxAcceleration = 200.0;
const int stepType = INTERLEAVE;
const float lengthPerStepMM = 0.3625;
 
// Sizing Information
// TODO set all of this information in eeprom
float motorWidthMM = 698.0;
float pageWidthMM = 579.35;
float pageHeightMM = 579.35;
float pageTopPaddingMM = 400;
float pageLeftPaddingMM = 100;
 
// Pen Lift servo information if it exists
#ifdef PENLIFT
const int penliftUpPosition = 20;
const int penliftDownPosition = 0;
const int penliftServoPin = 10;
const int penliftDelay = 500;
#endif
 
   
// Set up the Motor Shield and functions
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *lMotor = AFMS.getStepper(motorStepsPerRev, 1);
Adafruit_StepperMotor *rMotor = AFMS.getStepper(motorStepsPerRev, 2);
 
void forwardL() { lMotor->onestep(FORWARD, stepType); }
void backwardL() { lMotor->onestep(BACKWARD, stepType); }
void forwardR() { rMotor->onestep(FORWARD, stepType); }
void backwardR() { rMotor->onestep(BACKWARD, stepType); }
void leftStep(int dir) { lMotor->onestep(dir, stepType); }
void rightStep(int dir) { lMotor->onestep(dir, stepType); }
 
AccelStepper leftMotor(forwardL, backwardL);
AccelStepper rightMotor(backwardR, forwardR); 
 
void configuration_setup()
{
   // Begin the motor shield
   AFMS.begin();
   
   // Set the max speeds, min speeds, and acceleration of the motors
   leftMotor.setMaxSpeed(motorMaxStepsPerSec);
   rightMotor.setMaxSpeed(motorMaxStepsPerSec);
   leftMotor.setAcceleration(motorMaxAcceleration);
   rightMotor.setAcceleration(motorMaxAcceleration);
   
   // Set the starting position of the motors to be the
   //  top left of the page (0,0) of the coordinate system
   float startLengthLeft = sqrt(sq(pageTopPaddingMM) + sq(pageLeftPaddingMM)) / lengthPerStepMM;
   float startLengthRight = sqrt(sq(pageTopPaddingMM) + sq(motorWidthMM - pageLeftPaddingMM)) / lengthPerStepMM;
   leftMotor.setCurrentPosition(startLengthLeft);
   rightMotor.setCurrentPosition(startLengthRight);
   
   // Set up the servo for the pen if it exists
#ifdef PENLIFT
   penlift_setup();
#endif

   // Set up the comms over serial if it exists
#ifdef SERIAL_COMMS
   comms_serial_setup();
#endif

   // Set up the comms over ethernet if it exists
#ifdef ETHERNET_COMMS
   comms_ethernet_setup();
#endif
}

void conf_set_motor_width()
{
  // Adjust the motor width
  motorWidthMM = atof(SCmd.next());
  // Send that ready for next command
  comms_ready();
}

void conf_set_left_padding()
{
  // Adjust the left padding
  pageLeftPaddingMM = atof(SCmd.next());
  // Send that ready for next command
  comms_ready();
}

void conf_set_top_padding()
{
  // Adjust the top padding
  pageTopPaddingMM = atof(SCmd.next());
  // Send that ready for next command
  comms_ready();
}

void conf_set_canvas_width()
{
  // Adjust the canvas width
  pageWidthMM = atof(SCmd.next());
  // Send that ready for next command
  comms_ready();
}

void conf_set_canvas_height()
{
  // Adjust the canvas height
  pageHeightMM = atof(SCmd.next());
  // Send that ready for next command
  comms_ready();
}
