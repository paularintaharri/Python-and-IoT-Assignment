from realtcp import *
from gpio import *
from time import *

serverIP = "127.0.0.1"
serverPort = 60000

entry_button = 0
entry_door = 1
entry_led = 2
exit_button = 3
exit_door = 4
exit_led = 5
a0 = 6
a1 = 7
a2 = 8
a3 = 9

client = RealTCPClient()


def onTCPConnectionChange(type):
    print("connection changed: " + str(type))


def onTCPReceive(data):
    print("received: " + data);


def exitDoor():
    customWrite(exit_door, "1,0")
    analogWrite(exit_led, 1023)
    sleep(5)
    customWrite(exit_door, "0,1")
    analogWrite(exit_led, 0)


def entryDoor():
    customWrite(entry_door, "1,0")
    analogWrite(entry_led, 1023)
    sleep(5)
    customWrite(entry_door, "0,1")
    analogWrite(entry_led, 0)


def entryMessage():
    client.send("4:A staff member has entered to the building")


def exitMessage():
    client.send("5:A staff member has left the building")


def main():
    client.onConnectionChange(onTCPConnectionChange)
    client.onReceive(onTCPReceive)
    client.connect(serverIP, serverPort)
    count = 0
    name_sent = False
    action = False

    customWrite(entry_door, "0,1")
    customWrite(exit_door, "0,1")
    analogWrite(entry_led, 0)
    analogWrite(exit_led, 0)

    while True:

        value_entry_button = digitalRead(entry_button)
        value_exit_button = digitalRead(exit_button)

        if value_entry_button == HIGH:
            entryMessage()
            entryDoor()
            exitDoor()

        if value_exit_button == HIGH:
            exitMessage()
            exitDoor()
            entryDoor()

        if client.state() == 3:
            if name_sent == False:
                client.send("3:ACCESS CONTROL")
                name_sent = True


if __name__ == "__main__":
    main()
