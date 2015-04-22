/**
 * Plotting Time and Space - COMMS
 * Author: Robert Ross
 *
 * This file handles communication information of the 
 *  plotter over serial and possibly I will add ethernet in
 *  the future
 */
#ifdef SERIAL_COMMS

// G code support
const static char* CMD_RAPIDMOVE = "G00";
const static char* CMD_NORMALMOVE = "G01";
const static char* CMD_CLOCKWISE_ARC = "G02";
const static char* CMD_COUNTERCLOCKWISE_ARC = "G03";
const static char* CMD_DWELL = "G04";
const static char* CMD_INCHES = "G20";
const static char* CMD_MM = "G21";
const static char* CMD_ABSOLUTE = "G90";
const static char* CMD_RELATIVE = "G91";

// Special commands non-standard
const static char* CMD_PENUP = "PENUP";
const static char* CMD_PENDOWN = "PENDOWN";
const static char* CMD_TELEPORT = "TELEPORT";
const static char* CMD_DISABLE = "DISABLE";
const static char* CMD_ENABLE = "ENABLE";

void comms_serial_setup()
{
  // Init the serial command tool with all of the known commands
  SCmd.addCommand(CMD_RAPIDMOVE, comms_moverapid);
  SCmd.addCommand(CMD_NORMALMOVE, comms_moveline);
  SCmd.addCommand(CMD_CLOCKWISE_ARC, comms_movearc_clockwise);
  SCmd.addCommand(CMD_COUNTERCLOCKWISE_ARC, comms_movearc_counterclockwise);
  SCmd.addCommand(CMD_DWELL, comms_dwell);
  SCmd.addCommand(CMD_TELEPORT, comms_teleport);
  
#ifdef PENLIFT  
  SCmd.addCommand(CMD_PENUP, penlift_up);
  SCmd.addCommand(CMD_PENDOWN, penlift_down);
#endif

  SCmd.addCommand(CMD_INCHES, exec_set_inches);
  SCmd.addCommand(CMD_MM, exec_set_mm);

// TODO These commands are not recognized due to library
//  Should use CmdMessenger in the future
  SCmd.addCommand(CMD_ABSOLUTE, exec_set_absolute);
  SCmd.addCommand(CMD_RELATIVE, exec_set_relative);
  SCmd.addCommand(CMD_DISABLE, exec_disable);
  SCmd.addCommand(CMD_ENABLE, exec_enable);

  // Add the default handler
  SCmd.addDefaultHandler(comms_unrecognized);
}

void comms_moverapid()
{
  // Grab the arguments, convert them if necessary, and then
  //  send them to the function
  char *arg[3];
  float x = currentX;
  float y = currentY;
  
  arg[0] = SCmd.next();
  arg[1] = SCmd.next();
  arg[2] = SCmd.next();
  
  for(int i = 0; i < 3; i++)
  {
    if(arg[i] != NULL)
    {
      if(arg[i][0] == 'X')
      {
        x = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'Y')
      {
        y = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'F')
      {
        #ifdef FEED_TO_PEN
        float feed = atof(arg[i] + 1);
        if(feed > 0)
        {
          penlift_up();
        }
        else
        {
          penlift_down();
        }
        #endif
      }
    }
  }
  // Now that we have x and y, let us check some stuff
  if(inches)
  {
    // Convert x and y to mm
    x = x * 25.4;
    y = y * 25.4;
  }
  if(relative)
  {
    // Convert x and y to absolute
    x = currentX + x;
    y = currentY + y;
  }
  
  // Now call the function
  exec_moverapid(x,y);

#ifdef DEBUG
  Serial.println((String)"NEW_POSITION: X:" + currentX + " Y:" + currentY);
#endif
}

void comms_moveline()
{
  // Grab the arguments, convert them if necessary, and then
  //  send them to the function
  char *arg[3];
  float x = currentX;
  float y = currentY;
  
  arg[0] = SCmd.next();
  arg[1] = SCmd.next();
  arg[2] = SCmd.next();
  
  for(int i = 0; i < 3; i++)
  {
    if(arg[i] != NULL)
    {
      if(arg[i][0] == 'X')
      {
        x = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'Y')
      {
        y = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'F')
      {
        #ifdef FEED_TO_PEN
        float feed = atof(arg[i] + 1);
        if(feed > 0)
        {
          penlift_up();
        }
        else
        {
          penlift_down();
        }
        #endif
      }
    }
  }
  // Now that we have x and y, let us check some stuff
  if(inches)
  {
    // Convert x and y to mm
    x = x * 25.4;
    y = y * 25.4;
  }
  if(relative)
  {
    // Convert x and y to absolute
    x = currentX + x;
    y = currentY + y;
  }
  
  // Now call the function
  exec_moveline(x,y);

#ifdef DEBUG
  Serial.println((String)"NEW_POSITION: X:" + currentX + " Y:" + currentY);
#endif
}

void comms_movearc_clockwise()
{
  // Grab the arguments, convert them if necessary, and then
  //  send them to the function
  char *arg[5];
  float x = currentX;
  float y = currentY;
  float i = currentX;
  float j = currentY;
  
  arg[0] = SCmd.next();
  arg[1] = SCmd.next();
  arg[2] = SCmd.next();
  arg[3] = SCmd.next();
  arg[4] = SCmd.next();
  
  for(int i = 0; i < 5; i++)
  {
    if(arg[i] != NULL)
    {
      if(arg[i][0] == 'X')
      {
        x = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'Y')
      {
        y = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'I')
      {
        i = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'J')
      {
        i = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'F')
      {
        #ifdef FEED_TO_PEN
        float feed = atof(arg[i] + 1);
        if(feed > 0)
        {
          penlift_up();
        }
        else
        {
          penlift_down();
        }
        #endif
      }
    }
  }
  // Now that we have x and y, let us check some stuff
  if(inches)
  {
    // Convert x and y to mm
    x = x * 25.4;
    y = y * 25.4;
    i = i * 25.4;
    j = j * 25.4;
  }
  if(relative)
  {
    // Convert x and y to absolute
    x = currentX + x;
    y = currentY + y;
    i = currentX + i;
    j = currentY + j;
  }
  
  // Now call the function
  exec_movearc_clockwise(x,y,i,j);

#ifdef DEBUG
  Serial.println((String)"NEW_POSITION: X:" + currentX + " Y:" + currentY);
#endif
}

void comms_movearc_counterclockwise()
{
  // Grab the arguments, convert them if necessary, and then
  //  send them to the function
  char *arg[5];
  float x = currentX;
  float y = currentY;
  float i = currentX;
  float j = currentY;
  
  arg[0] = SCmd.next();
  arg[1] = SCmd.next();
  arg[2] = SCmd.next();
  arg[3] = SCmd.next();
  arg[4] = SCmd.next();
  
  for(int i = 0; i < 5; i++)
  {
    if(arg[i] != NULL)
    {
      if(arg[i][0] == 'X')
      {
        x = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'Y')
      {
        y = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'I')
      {
        i = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'J')
      {
        i = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'F')
      {
        #ifdef FEED_TO_PEN
        float feed = atof(arg[i] + 1);
        if(feed > 0)
        {
          penlift_up();
        }
        else
        {
          penlift_down();
        }
        #endif
      }
    }
  }
  // Now that we have x and y, let us check some stuff
  if(inches)
  {
    // Convert x and y to mm
    x = x * 25.4;
    y = y * 25.4;
    i = i * 25.4;
    j = j * 25.4;
  }
  if(relative)
  {
    // Convert x and y to absolute
    x = currentX + x;
    y = currentY + y;
    i = currentX + i;
    j = currentY + j;
  }
  
  // Now call the function
  exec_movearc_counterclockwise(x,y,i,j);

#ifdef DEBUG
  Serial.println((String)"NEW_POSITION: X:" + currentX + " Y:" + currentY);
#endif
}

void comms_dwell()
{
  // Grab the arguments, convert them if necessary, and then
  //  send them to the function
  char *arg;
  float time = 0;
  
  arg = SCmd.next();

  if(arg != NULL)
  {
    if(arg[0] == 'P')
    {
      time = atof(arg + 1);
    }
    else if(arg[0] == 'X')
    {
      time = atof(arg + 1) * 1000.0;
    }
  }
  
  exec_dwell(time);
}

void comms_teleport()
{
  // Grab the arguments, convert them if necessary, and then
  //  send them to the function
  char *arg[2];
  float x = currentX;
  float y = currentY;
  
  arg[0] = SCmd.next();
  arg[1] = SCmd.next();
  
  for(int i = 0; i < 2; i++)
  {
    if(arg[i] != NULL)
    {
      if(arg[i][0] == 'X')
      {
        x = atof(arg[i] + 1);
      }
      else if(arg[i][0] == 'Y')
      {
        y = atof(arg[i] + 1);
      }
    }
  }
  // Now that we have x and y, let us check some stuff
  if(inches)
  {
    // Convert x and y to mm
    x = x * 25.4;
    y = y * 25.4;
  }
  if(relative)
  {
    // Convert x and y to absolute
    x = currentX + x;
    y = currentY + y;
  }
  
  // Now call the function
  exec_teleport(x,y);

#ifdef DEBUG
  Serial.println((String)"NEW_POSITION: X:" + currentX + " Y:" + currentY);
#endif
}

void comms_unrecognized()
{
  Serial.println("Command unrecognized");
}
#endif
