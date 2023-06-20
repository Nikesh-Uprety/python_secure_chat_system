import socket

from cryptography.fernet import Fernet

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = 'localhost'
server_port = 12345

# Connect to the server
client_socket.connect((server_host, server_port))
print('Connected to server at {}:{}'.format(server_host, server_port))

# Receive the encryption key from the server
key = client_socket.recv(1024)

# Create a cipher suite using the received key
cipher_suite = Fernet(key)

while True:
    # Get the message to send from the client
    message = input('Client: ')
    
    # Encrypt the message
    encrypted_message = cipher_suite.encrypt(message.encode())
    
    # Send the encrypted message to the server
    client_socket.send(encrypted_message)
    
    # Receive the encrypted message from the server
    encrypted_message = client_socket.recv(1024)
    
    # Decrypt the message
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    
    print('Received:', decrypted_message)
    
    # Close the connection if the server requests it
    if message.lower() == 'bye':
        break

# Close the client socket
client_socket.close()
