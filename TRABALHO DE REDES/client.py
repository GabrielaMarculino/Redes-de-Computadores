# 172.27.3.200 ip virtualmachine
# Gabriela Marculino e Lincoln Amorim
# Import socket module
import socket           
import sys

BUFLEN=8192

# Create a socket object
s = socket.socket()        
 
# Define the port on which you want to connect
port = int(sys.argv[1])              
 
# connect to the server on local computer
s.connect(('', port))

# send the url to access and receive the message
url = input("Request: ")
s.send(url.encode())

# receive data from the server and decoding to get the string.
print (s.recv(BUFLEN).decode('utf-8'))

print (s.recv(BUFLEN).decode())
# close the connection
s.close() 