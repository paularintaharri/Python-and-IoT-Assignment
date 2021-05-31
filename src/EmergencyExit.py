from realtcp import *
from gpio import *
from time import *

serverIP = "127.0.0.1"
serverPort = 60000

door = 0
siren = 1
d2 = 2
d3 = 3
d4 = 4
d5 = 5
a0 = 6
a1 = 7
a2 = 8
a3 = 9

client = RealTCPClient()


def onTCPConnectionChange(type):
    print("connection changed: " + str(type))


def onTCPReceive(data):
    print("received: " + data);


def main():
    client.onConnectionChange(onTCPConnectionChange)
    client.onReceive(onTCPReceive)
    client.connect(serverIP, serverPort)
    count = 0
    name_sent = False
    action = False

    while True:

        value_door = customRead(door)
        if value_door == "1,0":
            customWrite(siren, "1")
            if action == False:
                client.send("2:Emergency exit open")
                action = True
        else:
            customWrite(siren, "0")
            action = False

        if client.state() == 3:
            if name_sent == False:
                client.send("1:EMERGENCY EXIT ")
                name_sent = True

        sleep(1)


if __name__ == "__main__":
    main()
