sudo systemctl stop TcpServer-py.service
sudo systemctl daemon-reload
sudo systemctl enable TcpServer-py.service
sudo systemctl start TcpServer-py.service
echo service rebuilt