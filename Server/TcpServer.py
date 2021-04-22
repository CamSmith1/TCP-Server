import socket
# set sockets to point to TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Google says this line is important
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to all the interfaces on port 6969
sock.bind(("0.0.0.0", 6969))

sock.listen(2)
print ("Server has started listening")
while True:
    (client, (ip, port)) = sock.accept()
    print('Sensor connected with ip as {} and port {}'.format(ip, port))
    data = client.recv(2048)
    while len(data):
        print("Sensor sent the data : {}".format(data))

        file = open('SensorLogs.txt', 'a')
        file.write(format(data) + '\n')
        file.close()
        client.send(data.upper())
        data = client.recv(2048)
    print("Sensor closed connection ")
    client.close()


