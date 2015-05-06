/**
 * Plotting Time and Space - CONFIGURATION
 * Author: Robert Ross
 *
 * This file contains all of the configuration options for
 *  the plotting time and space controller
 */
 
// Motor Information
// Remember that the number of steps per rev depends on the 
//  step type taken.
const int motorStepsPerRev = 400;
const float motorMaxStepsPerSec = 200.0;
const float motorMaxAcceleration = 200.0;
const int stepType = INTERLEAVE;
const float lengthPerStepMM = 0.4;
 
// Sizing Information
const float motorWidthMM = 641.35;
const float pageWidthMM = 457.2;
const float pageHeightMM = 457.2;
const float pageTopPaddingMM = 425.45;
const float pageLeftPaddingMM = 163.5;
 
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
