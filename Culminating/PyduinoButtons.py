import Pyduino
import time

BUTTON = 3

SCREEN_MESSAGE_TYPE = 9
BUTTON_MESSAGE_TYPE = 10

Pyduino.Init()

num = 0
oldNum = 0

while 1:
    time.sleep(0.2)
    state = Pyduino.DigitalRead(BUTTON)
    print("State: " + str(state))
    #time.sleep(0.3)
    if oldNum != num:
        oldNum = num
        #Pyduino.Message(SCREEN_MESSAGE_TYPE, [f"Num: {num}"])