/**
 * Plotting Time and Space - COMMS
 * Author: Robert Ross
 *
 * This file handles communication information of the 
 *  plotter over serial and possibly I will add ethernet in
 *  the future
 */
#ifdef SERIAL_COMMS
  
void comms_serial_setup()
{
  // Init the serial command tool with all of the known commands
  SCmd.addCommand("G00", comms_moverapid);
  SCmd.addCommand("G01", comms_moveline);
  SCmd.addCommand("G02", comms_movearc_clockwise);
  SCmd.addCommand("G03", comms_movearc_counterclockwise);
  SCmd.addCommand("G04", comms_dwell);
  SCmd.addCommand("TELEPORT", comms_teleport);
  SCmd.addCommand("G20", exec_set_inches);
  SCmd.addCommand("G21", exec_set_mm);
  SCmd.addCommand("G90", exec_set_absolute);
  SCmd.addCommand("G91", exec_set_relative);
  
#ifdef PENLIFT  
  SCmd.addCommand("PENUP", penlift_up);
  SCmd.addCommand("PENDOWN", penlift_down);
#endif
  SCmd.addCommand("DISABLE", exec_disable);
  SCmd.addCommand("ENABLE", exec_enable);

  SCmd.addCommand("MWIDTH", conf_set_motor_width);
  SCmd.addCommand("LPADDING", conf_set_left_padding);
  SCmd.addCommand("TPADDING", conf_set_top_padding);
  SCmd.addCommand("CWIDTH", conf_set_canvas_width);
  SCmd.addCommand("CHEIGHT", conf_set_canvas_height);

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

  // Send that ready for next command
  comms_ready();
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

  // Send that ready for next command
  comms_ready();
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

  // Send that ready for next command
  comms_ready();
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

  // Send that ready for next command
  comms_ready();
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
  
  // Send that ready for next command
  comms_ready();
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

  // Send that ready for next command
  comms_ready();
}

void comms_unrecognized()
{
  Serial.println(F("Command unrecognized"));
  // Send that ready for next command
  comms_ready();
}

void comms_ready()
{
  // Make a function because its called often
  Serial.println(F("READY"));
}
#endif
