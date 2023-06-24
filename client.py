import socket
import time

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server address and port
server_host = 'localhost'
server_port = 12345

# Connect to the server
client_socket.connect((server_host, server_port))
print('Connected to server at {}:{}'.format(server_host, server_port))

# Receive the server's encryption key
key = client_socket.recv(1024)

# Prompt the user to enter the secret key
secret_key = input('Enter the secret key: ')

# Send the secret key to the server
client_socket.send(secret_key.encode())

# Receive the authentication status from the server
auth_status = client_socket.recv(1024).decode()

# Check if authentication was successful
if auth_status == 'success':
    print('Authentication successful')
    # Send messages to the server
    while True:
        message = input('Enter a message: ')
        client_socket.send(message.encode())
else:
    print('Authentication failed')
    client_socket.close()

# Close the client socket
client_socket.close()
