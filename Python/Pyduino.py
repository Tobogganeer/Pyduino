
import serial
import time
import serial.tools.list_ports
import struct

# Store arduino in a class for global access
class Arduino:
    value : serial.Serial


# Basic constants
HIGH = 1
LOW = 0

MESSAGE_RETURN = 253
MESSAGE_START = 254
MESSAGE_END = 255

A0 = 14
A1 = 15
A2 = 16
A3 = 17
A4 = 18
A5 = 19

# For debug purposes, print all bytes received over serial
LogReceivedBytes = False

# Packs bytes of a float into an int for writing into messages
def floatToIntBytes(value : float) -> int:
    return int.from_bytes(struct.pack("f", value), 'little')

# Command class, stores values that are packed and sent over serial
class Command:
    class Type:
        Null = 0
        DigitalWrite = 1
        DigitalRead = 2
        AnalogWrite = 3
        AnalogRead = 4
        Tone = 5
        NoTone = 6

    # Le constructor
    def __init__(self, type : int, args : list[int], strArgs : list[str] = []):
        self.type = type
        self.args = args
        self.strArgs = strArgs

    # Static methods for different kinds of messages, classmethod instead of staticmethod so I can use constructor
    @classmethod
    def DigitalWrite(cls, port : int, output : int):
        return cls(Command.Type.DigitalWrite, [port, output])

    @classmethod
    def DigitalRead(cls, port : int):
        return cls(Command.Type.DigitalRead, [port])
    
    @classmethod
    def AnalogWrite(cls, port : int, output : int):
        return cls(Command.Type.AnalogWrite, [port, output])
    
    @classmethod
    def AnalogRead(cls, port : int):
        return cls(Command.Type.AnalogRead, [port])
    
    @classmethod
    def Tone(cls, port : int, freq : int, duration : float = 0):
        return cls(Command.Type.Tone, [port, freq, floatToIntBytes(duration)])
    
    @classmethod
    def NoTone(cls, port : int):
        return cls(Command.Type.NoTone, [port])

    #buzzers, motors, leds

# Max time to wait for messages
MAX_RECEIVE_MS = 100


# The bread and butter of the library
def Send(command : Command):
    global LogReceivedBytes

    # Byte array
    packet = [MESSAGE_START]

    # Add type, then any args in the message
    packet.append(command.type)
    if len(command.args) > 0:
        for arg in command.args:
            packet.extend(arg.to_bytes(4, 'little'))
    if len(command.strArgs) > 0:
        for strArg in command.strArgs:
            packet.append(len(strArg))
            packet.extend(bytes(strArg, "ascii"))
    packet.append(MESSAGE_END)

    # Send er
    Arduino.value.write(bytes(packet))
    
    # Wait for message to send
    Arduino.value.flush()
    #Arduino.value.flushInput()

    # Try a few times to see if data is back yet
    for i in range (int(MAX_RECEIVE_MS / 10)):
        time.sleep(0.01)

        # Message!
        if Arduino.value.in_waiting:
            # Get the message as a byte[]
            serialBytes : bytes = Arduino.value.read(Arduino.value.in_waiting)
            if LogReceivedBytes:
                print("Message: " + ", ".join([str(c) for c in serialBytes]))
            # Received data should start with MESSAGE_RETURN
            if not MESSAGE_RETURN in serialBytes:
                print(f"Did not get MESSAGE_RETURN header in response for {command.type} message")
                #print("Message: " + ", ".join([str(c) for c in serialBytes]))
                return -1
            else:
                # Return value for something like DigitalRead()
                intBytes : bytes = serialBytes[serialBytes.index(MESSAGE_RETURN) + 1:]
                return int.from_bytes(intBytes, 'little')
                #return serialBytes[serialBytes.index(MESSAGE_RETURN) + 1]
    print(f"Did not receive response for {command.type} message")
    return -1
    #command.

def Init():
    # Find arduino port
    ports = list(serial.tools.list_ports.comports())
    #serialBytes = []
    found = False
    for p in ports:
        if "Arduino" in p.description:
            # Connect to arduino
            Arduino.value = serial.Serial(port=p.device, baudrate=115200, timeout=.1)
            found = True

    if not found:
        print("No arduino found! All ports:")
        for p in ports:
            print(p)
        return -1
    return 0

# Easier functions to send commands
def DigitalWrite(port : int, output : int):
    return Send(Command.DigitalWrite(port, output))

def DigitalRead(port : int):
    return Send(Command.DigitalRead(port))

def AnalogWrite(port : int, output : int):
    return Send(Command.AnalogWrite(port, output))

def AnalogRead(port : int):
    return Send(Command.AnalogRead(port))

def Tone(port : int, freq : int, duration : float = 0):
    return Send(Command.Tone(port, freq, duration))

def NoTone(port : int):
    return Send(Command.NoTone(port))

# Custom messages
def Message(type : int, args : list[int]):
    if type <= Command.Type.NoTone:
        print("Cannot send custom message, ID must be more than 6. Passed ID: " + str(type))
        return -1
    return Send(Command(type, args))

def Message(type : int, args : list[str]):
    if type <= Command.Type.NoTone:
        print("Cannot send custom message, ID must be more than 6. Passed ID: " + str(type))
        return -1
    return Send(Command(type, [], args))

def EmptyMessage(type : int):
    if type <= Command.Type.NoTone:
        print("Cannot send custom message, ID must be more than 6. Passed ID: " + str(type))
        return -1
    return Send(Command(type, []))