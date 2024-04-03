# import socket module
import os.path
from socket import *
import _thread as thread
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
port = 8080
ip = "127.0.0.1"


serverSocket.bind((ip, port))
serverSocket.listen(1)

# For multithreading. Handles receiving request, finding request and returning data

def handleClient(connectionSocket):
        message = connectionSocket.recv(1024).decode()  # Write your code here #End of your code
        print(message)
        filename = message.split()[1]
        print(filename)
        basedir = os.path.dirname(os.path.realpath(__file__))

        # Init to Null due to bad/stupid if test placement. Code works so if it ain't broke I ain't breaking it TeruKillMe
        outputData = None

        # Checks validity of request path
        if os.path.exists(basedir + filename):
            file = open(filename[1:])
            data = file.read()
            outputData = data

            # Send one HTTP header line into socket
            header = "HTTP:/1.1 200 OK\r\n\r\n"
            connectionSocket.send(header.encode())

            # Send the content of the requested file to the client
            for i in range(0, len(outputData)):
                connectionSocket.send(outputData[i].encode())
        else:
            errorNotFound = "HTTP:/1.1 404 Not found\r\n"
            connectionSocket.send(errorNotFound.encode())
            # break
            print("File finding error")

        # Close client connection
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

while True:
    # Establish the connection
    try:
        connectionSocket, address = serverSocket.accept()
        thread.start_new_thread(handleClient, (connectionSocket,))

    except IOError as error:
        print("Error")
        print(error)
        errorHeader = "HTTP:/1.1 400 Bad Request \r\n"
        connectionSocket.send(errorHeader.encode())

serverSocket.close()
sys.exit()