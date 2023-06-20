import socket
from cryptography.fernet import Fernet
import threading

# Generate a unique key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

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

def broadcast_message(sender_socket, message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(encrypted_message)

def handle_client(client_socket, client_address):
    # Send the encryption key to the client
    client_socket.send(key)
    
    # Receive the username from the client
    username = client_socket.recv(1024).decode()
    clients[client_socket] = username
    print('Connected: {}:{}'.format(client_address[0], client_address[1]), 'Username:', username)
    
    while True:
        try:
            # Receive the encrypted message from the client
            encrypted_message = client_socket.recv(1024)
            
            if not encrypted_message:
                break
            
            # Decrypt the message
            decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
            
            print('Received from', username + ':', decrypted_message)
            
            # Broadcast the message to all connected clients
            broadcast_message(client_socket, username + ': ' + decrypted_message)
        except Exception as e:
            print('Error:', str(e))
            break
    
    # Close the client socket
    client_socket.close()
    del clients[client_socket]
    print('Disconnected:', username)

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    
    # Create a new thread for the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

server_socket.close()
