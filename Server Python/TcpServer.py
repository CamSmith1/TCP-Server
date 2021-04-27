import json
import socket
from _thread import *
import threading
import requests
import uuid
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

        # convert data to utf-8 format then into a dataArray
        dataArr = data.decode('utf-8')
        dataArr = list(dataArr)
        # Write data to DynamoDB (Only insert x2 report type)
        uploadData(dataArr)
        #   Write to log file
        file = open('/home/ubuntu/SensorLogs.txt', 'a')
        file.write(format(data) + '\n')
        file.close()



        # send back reversed string to client
        # data = data[::-1]
        #c.send(data)
        #break
    c.close()


def uploadData(dataArr):
    reportType = dataArr[6] + dataArr[7]
    print("Starting upload")
    print(reportType)
    if reportType == "02":
        packetSize = dataArr[8] + dataArr[9]
        height = dataArr[10] + dataArr[11] + dataArr[12] + dataArr[13]
        temperature = dataArr[14] + dataArr[15] + dataArr[16] + dataArr[17]
        batteryVoltage = dataArr[26] + dataArr[27] + dataArr[28] + dataArr[29]
        RSPR = dataArr[30] + dataArr[31] + dataArr[32] + dataArr[33] + dataArr[34] + dataArr[35] + dataArr[36] + dataArr[37]
        FRAM = dataArr[38] + dataArr[39] + dataArr[40] + dataArr[41]
        IMEI = dataArr[42] + dataArr[43] + dataArr[44] + dataArr[45] + dataArr[6] + dataArr[47] + dataArr[48] + dataArr[49] + dataArr[50] + dataArr[51] + dataArr[52] + dataArr[53] + dataArr[54] + dataArr[55] + dataArr[56] + dataArr[57]

        # Variable calculations
        height = int(height, 16)    # (Hex to decimal)
        temperature = int(temperature, 16)  # (Hex to decimal)
        batteryVoltage = int(batteryVoltage, 16) * 10   # (Hex value x 10 = voltage)
        transID = uuid.uuid4()
        payload = {
             "transactionID": str(transID),
             "reportType": reportType,
             "packetSize": packetSize,
             "height": height,
             "temperature": temperature,
             "batteryVoltage": batteryVoltage,
             "RSPR": RSPR,
             "FRAM": FRAM,
             "IMEI": IMEI
        }
        jsonStr = json.dumps(payload)
        endpoint = "https://ksq19dmqh4.execute-api.us-east-1.amazonaws.com/InsertData"

        req = requests.post(endpoint, data=jsonStr)
        print(req.text)



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