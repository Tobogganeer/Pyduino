#include "Pyduino.h"
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

const int LoopDelay = 10;
// Create the screen
LiquidCrystal_I2C lcd(0x27, 16, 2);

/*
const int LEFT = 3;
const int MID = 6;
const int RIGHT = 7;

int left, mid, right;
*/
// For old button code

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Select a song...");

  // Start pyduino and set the callback for changing the screen text
  Pyduino::Init();
  Pyduino::CustomMessageCallback = OnCustomMessage;

  /*
  pinMode(LEFT, INPUT);
  pinMode(MID, INPUT);
  pinMode(RIGHT, INPUT);
  */
}

void loop() {
  /*
  left = digitalRead(LEFT);
  mid = digitalRead(MID);
  right = digitalRead(RIGHT);
  */
  
  delay(LoopDelay);
  Pyduino::Tick();
  // Literally just wait for commands from python
}

// Custom message type
const int SET_LCD = 9;

long OnCustomMessage(byte* message, int len, int type)
{
  if (type == SET_LCD)
  {
    // Read a string and write it onto the screen
    int strRead = 0;
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(Pyduino::GetString(message, strRead));
  }
  /*
  else if (type == BUTTON_STATE)
  {
    if (left == HIGH)
      return 1;
    if (mid == HIGH)
      return 2;
    if (right == HIGH)
      return 3;
    return 0;
  }
  */
  
  return type;
  //return DEFAULT_MESSAGE_RETURN;
}
