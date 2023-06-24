import socket
import threading
import time
import signal
import sys

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = 'localhost'
server_port = 12345

# Bind the socket to a specific address and port
server_socket.bind((server_host, server_port))

# Listen for incoming connections
server_socket.listen(5)
print('Server listening on {}:{}'.format(server_host, server_port))

# Dictionary to store client sockets and their corresponding usernames
clients = {}

def handle_client(client_socket, client_address):
    # Receive the secret key from the client
    secret_key = client_socket.recv(1024).decode()
    print('Received secret key from {}: {}'.format(client_address[0], secret_key))

    # Log the time when the client connects
    connect_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('Client connected from {} at {}'.format(client_address[0], connect_time))

    # Add your custom authentication logic here
    # You can compare the secret key against a stored key or database entry
    # For simplicity, we are using a fixed secret key "password"
    if secret_key == 'nikuu':
        client_socket.send('success'.encode())

        # Log the time when the client successfully authenticates
        auth_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print('Client authenticated from {} at {}'.format(client_address[0], auth_time))

        clients[client_socket] = client_address
        print('Authentication successful for:', client_address[0])
    else:
        client_socket.send('failure'.encode())
        client_socket.close()
        print('Authentication failed for:', client_address[0])

def close_server(signal, frame):
    print('Closing server...')
    for client_socket in clients:
        client_socket.close()
    server_socket.close()
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, close_server)

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()

    # Create a new thread for the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

server_socket.close()
