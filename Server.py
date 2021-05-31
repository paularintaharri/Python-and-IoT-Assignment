import socket
import selectors
import types
import datetime


class MyDevice:
    def __init__(self, host, port,):
        self.host = host
        self.port = port

    def check_match(self, host, port):
        if self.host == host and self.port == port:
            return True
        else:
            return False

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("A new device has linked to the server.")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr)
    events = selectors.EVENT_READ
    sel.register(conn, events, data=data)
    IoT_devices.append(MyDevice(addr[0], addr[1]))

members = 0

def count_members(num):
    global members
    if num == 0:
        members = 0
    elif num == 1:
        members += 1
    else:
        members -= 1
    return "Number of staff members in the building: {0}".format(members)

def write_to_file(output):
    curr_date = datetime.datetime.now()
    curr_date = str(curr_date.strftime("%d/%m/%y %H:%M:%S"))
    the_file = open("log", "a")
    message = curr_date + ", " + output + ", " + str(members) + "\n"
    the_file.write(message)
    the_file.close()

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    host = data.addr[0]
    port = data.addr[1]
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            #Emergency exit
            if repr(recv_data)[2] == "1":
                print(recv_data[2:-1].decode('utf-8'))
            elif repr(recv_data)[2] == "2":
                print(recv_data[2:-1].decode('utf-8'))
                print(count_members(0))
                write_to_file("Emergency exit")

            #Access control
            elif repr(recv_data)[2] == "3":
                print(recv_data[2:-1].decode('utf-8'))
            # Access control entry
            elif repr(recv_data)[2] == "4":
                print(recv_data[2:-1].decode('utf-8'))
                print(count_members(1))
                write_to_file("Staff member")
            # Access control exit
            elif repr(recv_data)[2] == "5":
                print(recv_data[2:-1].decode('utf-8'))
                print(count_members(-1))
                write_to_file("Staff member")
        else:
            print("A device has been de-linked.")
            del IoT_devices[find_device(host, port)]
            sel.unregister(sock)
            sock.close()

def find_device(host, port):
    for i in range(0, len(IoT_devices)):
        if IoT_devices[i].check_match(host, port):
            return i
    return -1

HOST = '127.0.0.1'
PORT = 60000
IoT_devices = list()

sel = selectors.DefaultSelector()
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.bind((HOST, PORT))
serv_sock.listen()
print("listening on:", (HOST, PORT))

serv_sock.setblocking(False)
sel.register(serv_sock, selectors.EVENT_READ, data=None)

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
    print("-" * 50)
