# Import socket module
import socket


def Main():
    # local host IP '127.0.0.1'
    host = '100.26.239.195'

    # Define the port on which you want to connect
    port = 6969
    for x in range(0, 500):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
        s.connect((host, port))
        message = "SENT FROM Sensor " + str(x)
        s.send(message.encode('ascii'))
        s.close()

    print("FINISHED LOAD TEST")
if __name__ == '__main__':
    Main()