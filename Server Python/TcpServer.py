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

        # start reading data
        dataArr = data.decode('utf-8')
        dataArr = list(dataArr)
        reportType = dataArr[6] + dataArr[7]

        # If the report type is 02 store all the data in DB
        if reportType == "02":
            packetSize = dataArr[8] + dataArr[9]
            height = dataArr[10] + dataArr[11] + dataArr[12] + dataArr[13]
            temperature = dataArr[14] + dataArr[15] + dataArr[16] + dataArr[17]
            batteryVoltage = dataArr[26] + dataArr[27] + dataArr[28] + dataArr[29]
            RSPR = dataArr[30] + dataArr[31] + dataArr[32] + dataArr[33] + dataArr[34] + dataArr[35] + dataArr[36] + dataArr[37]
            FRAM = dataArr[38] + dataArr[39] + dataArr[40] + dataArr[41]
            IMEI = dataArr[42] + dataArr[43] + dataArr[44] + dataArr[45] + dataArr[6] + dataArr[47] + dataArr[48] + dataArr[49] + dataArr[50] + dataArr[51] + dataArr[52] + dataArr[53] + dataArr[54] + dataArr[55] + dataArr[56] + dataArr[57]

            print("packetSize " + packetSize)
            print("Height " + height)
            print("temperature " + temperature)
            print("batteryVoltage " + batteryVoltage)
            print("RSPR " + RSPR)
            print("FRAM " + FRAM)
            print("IMEI " + IMEI)
            break
        data = data[::-1]
        # send back reversed string to client
        c.send(data)
        #file = open('/home/ubuntu/SensorLogs.txt', 'a')
        #file.write(format(data) + '\n')
        #file.close()

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