import time
from socket import *

request = "GET /index.html"

clientSocket = socket(AF_INET, SOCK_STREAM)
serverIp = "127.0.0.1"
serverPort = 8080

clientSocket.connect((serverIp, serverPort))
clientSocket.send(request.encode())
response = clientSocket.recv(1024).decode()

while True:
    # Checks for response being "empty", ends loop.
    # Prevents infinite loop once response from server stops
    if response != "":
        response = clientSocket.recv(1024).decode()
        print(response)
        time.sleep(1)
    else:
        break
