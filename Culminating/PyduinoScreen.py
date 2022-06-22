import Pyduino
import time

Pyduino.Init()

PRINT_MESSAGE_TYPE = 9

value = 0

#Pyduino.LogReceivedBytes = True

while 1:
    time.sleep(1.5)
    Pyduino.Message(PRINT_MESSAGE_TYPE, [f"Value: {value}"])
    value += 1