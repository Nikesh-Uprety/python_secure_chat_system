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

# List to store all the client threads
client_threads = []

def handle_client(client_socket):
    # Send the encryption key to the client
    client_socket.send(key)
    
    while True:
        # Receive the encrypted message from the client
        encrypted_message = client_socket.recv(1024)
        
        # Decrypt the message
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        
        print('Received:', decrypted_message)
        
        # Get the message to send from the server
        message = input('Server: ')
        
        # Encrypt the message
        encrypted_message = cipher_suite.encrypt(message.encode())
        
        # Send the encrypted message to the client
        client_socket.send(encrypted_message)
        
        # Close the connection if the client requests it
        if message.lower() == 'bye':
            break
    
    # Close the client socket
    client_socket.close()

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Connected to client:', client_address)
    
    # Create a new thread for the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    
    # Add the client thread to the list
    client_threads.append(client_thread)
    
    # Remove finished threads from the list
    client_threads = [thread for thread in client_threads if thread.is_alive()]

# Close all client sockets and the server socket
for client_thread in client_threads:
    client_thread.join()

server_socket.close()