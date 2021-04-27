sudo systemctl stop TcpServer-py.service
sudo systemctl enable TcpServer-py.service
sudo systemctl start TcpServer-py.service
status=$(sudo systemctl status TcpServer-py.service)
echo $status
