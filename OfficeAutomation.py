from realtcp import *
from gpio import *
from time import *

room_door = 0
lock_switch = 1
fan = 2
light = 3
d4 = 4
d5 = 5
a0 = 6
a1 = 7
a2 = 8
a3 = 9


def main():
    DOOR_OPEN = False
    people_in = False

    while True:

        value_door = customRead(room_door)
        value_switch = digitalRead(lock_switch)

        if value_door == "1,0" and people_in == False:
            # open
            DOOR_OPEN = True

        if value_door == "1,0" and people_in == True:
            # open
            DOOR_OPEN = False

        if value_door == "0,0" and DOOR_OPEN == True:
            people_in = True
            print("people_in", people_in)

        if value_door == "0,0" and DOOR_OPEN == False:
            people_in = False
            print("people_in", people_in)

        if people_in == True:
            customWrite(light, "1")
            customWrite(fan, "1")

            # if people in the room, door can be locked
            if value_switch == 0:
                customWrite(room_door, "0,0")
            else:
                customWrite(room_door, "0,1")

        elif people_in == False:
            customWrite(light, "0")
            customWrite(fan, "0")


if __name__ == "__main__":
    main()
