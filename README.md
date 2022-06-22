# Pyduino

Serial communication between Python and Arduino made simpler.


## Python
### Initialize the library:
```py
import Pyduino

Pyduino.Init()
```
### Send commands to the Arduino:
```py
# Write to a pin
Pyduino.DigitalWrite(SomePinValue, Pyduino.HIGH)
Pyduino.AnalogWrite(Pyduino.A3, 123)

# Read from a pin
readValue = Pyduino.DigitalRead(SomePinValue)
analogValue = Pyduino.AnalogRead(Pyduino.A0)

# Use a buzzer
Pyduino.Tone(SpeakerPin, Frequency, Duration)
Pyduino.NoTone(SpeakerPin)

# Send a custom message
Pyduino.Message(CustomMessageID, [5, 2, 5, 124])
Pyduino.Message(OtherMessageID, ["String args"])
```

<br/>

## Arduino
### Initialize the library:
```cpp
#include "Pyduino.h"

void setup() {
  Pyduino::Init();
  // If using custom messages
  Pyduino::CustomMessageCallback = SomeMessageHandlerFunction;
}
```
### Handle custom messages:
```cpp
long messageIDImLookingFor = 15;

long SomeMessageHandlerFunction(byte* message, int len, int type)
{
  if (type == messageIDImLookingFor)
  {
    int read = 0;
    String str = Pyduino::GetString(message, read);
    long num = Pyduino::GetInt(message, read);
    
    // Do something
  }
  
  // Return value sent to python code
  return 0;
}
```

---

Check the examples provided, basic [text printing to a screen](Python/PyduinoScreen.py), or a more [advanced buzzer speaker](Python/PyduinoMusic.py)
</br></br>Toy around and edit the source!
</br></br>Code quality may be lackluster (as an example, there was a buffer overflow when reading strings!), but I hope this proves useful as a reference to somebody.
