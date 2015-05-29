/**
 * Plotting Time and Space Controller
 * Author: Robert Ross
 *
 * Some aspects of this software has been inspired by
 *  Polargraph controller written by Sandy Nobel and the
 *  Makeangelo controller written by MarginallyClever
 *
 * Plotting Time and Space software is designed to be for
 *  specific hardware in order to keep the code small enough
 *  for the UNO. It might be made more generic in the future
 *  by having multiple versions in the future.
 *
 * The file structure consists of:
 * - comms - Handles communication over serial and possibly ethernet in the future
 * - configuration - Handles all configuration things
 * - exec - Executes the commands retrieved from comms
 * - time_and_space - The mains file that runs setup and loop
 */

// Comment out the defines for features that do not exist
//--------------------------------------------------------
#define PENLIFT

//#define ETHERNET_COMMS
#define SERIAL_COMMS

#define FEED_TO_PEN // Feed rate of 0 means pen up

#define DEBUG
//---------------------------------------------------------

// Include the Adafruit Motorshield v2 libs
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"
#include <AccelStepper.h>  // Let us move two motors at once

// This would be nice to pull out of here and put in comms but not now
#include <SerialCommand.h>
SerialCommand SCmd;

// Global variables to be used
boolean relative = false;
boolean inches = false;
float currentX = 0.0;
float currentY = 0.0;

void setup() {
  // Init the serial stuff
  Serial.begin(57600);
  Serial.println(F("Time and Space Plotter ON"));
  Serial.println(F("-------------------------------"));

  // Call the config setup function
  configuration_setup();

  // Lift the pen if that function exists
#ifdef PENLIFT
  penlift_down();
#endif

  // Enable and lock the motors
  exec_enable();
  
  // Indicate that setup is done
  Serial.println(F("Setup Complete ... "));
  
  // Send that ready for next command
  comms_ready();
}

void loop() {
  // Look for the commands to come in from whichever source
#ifdef SERIAL_COMMS
  SCmd.readSerial();  // Constantly look for a command
#endif

#ifdef ETHERNET_COMMS
  // TODO add comms over ethernet
#endif
}
