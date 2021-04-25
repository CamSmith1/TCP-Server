import socket
from _thread import *
import threading

print_lock = threading.Lock()
# thread function
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Connection Closed')

            # lock released on exit
            print_lock.release()
            break
        print("Sensor sent the data : {}".format(data))
        file = open('/home/ubuntu/SensorLogs.txt', 'a')
        file.write(format(data) + '\n')
        file.close()

    c.close()


def main():
    # Set host IP to server's IP
    host = ""

    # point to port 6969
    port = 6969
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    # put the socket into listening mode
    s.listen(5)
    print("TCP Listener has started")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    main()