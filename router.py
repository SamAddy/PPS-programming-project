import socket
from threading import Thread
import time
"""
use class BGP_router to create router objects.

I have used Multi Threading to run servers and clients concurrently.

steps:

1- use a loop to create 10 different objects with 10 different IPs. you can use list
interface_list to do so.

2- each needs to listen and accept a connection by calling the functions. to be put in the main function.

3- states are changed based on the content of messages. this part is left to Sam.
it should be done by looking into the RFCs related to BGP and based on what exist
in the headers in binary format.

4- should you have any question feel free to ask me anytime.
"""


# The following class creates a server socket (each port can be used as either server or client.
# no port can be used as both
class RouterServer:
    def __init__(self, name, state, ip, port):
        self.name = name
        self.state = state
        self.ip = ip
        self.port = port
        self.routerobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.routerobject.bind((self.ip, self.port))
        self.clientsocket = 0
        self.clientaddress = "0.0.0.0"  # sample will never be used
        self.incoming_msg = ""
        self.path_table = {"sample_router_name": ("Network", "Next Hop", "Weight")}

    def listen(self):
        self.routerobject.listen(11)

        # print('p1')

    def accept(self):
        while True:
            # print('p2')

            self.clientsocket, self.clientaddress = self.routerobject.accept()
            print("received connection from: " + str(self.clientaddress) + "\r\n")
            # print('p3')
            self.clientsocket.send("connection accepted".encode("ascii"))
            self.clientsocket.close()


#  ------------------------------------------------------------------
# the following class makes client socket objects


class RouterClient:
    def __init__(self, name, state, ip, port):
        # print('a') for debugging
        self.name = name
        self.state = state
        self.ip = ip
        self.port = port
        self.routerobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.incoming_msg = ""

    def connect(self, server_ip, server_port):
        # print('c1') for debugging

        self.routerobject.connect((server_ip, server_port))

        self.incoming_msg = self.routerobject.recv(1024)
        # print('c2') for debugging

        print(self.incoming_msg.decode("ascii"))
        # print('c3') gor debugging


def router_listener():
    a1_l = RouterServer(
        "a1", "IDLE", "10.0.2.15", 444
    )  # a1_l = a1 listener & a1_s = a1 sender
    a1_l.listen()
    a1_l.accept()


def router_sender():
    time.sleep(
        15
    )  # Will cause an error if deleted. required time for router to become stable.
    a1_s = RouterClient("a1", "IDLE", "10.0.2.15", 557)
    a1_s.connect("10.0.2.6", 444)


if __name__ == "__main__":
    Thread(target=router_listener).start()
    Thread(target=router_sender).start()

# a3.connect(a1.ip,a1.port)

# a2.listen()
# a2.accept()
# this part creates a list of potential useful IPs for simulating 10 different routers
ip_oct = [i for i in range(2, 14)]
interfacce_list = []
for i in ip_oct:
    interfacce_list.append("127.0.0." + str(i))
