import socket
import sys
import threading

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

# Receive the username from the user
username = input('Enter your username: ')
client_socket.send(username.encode())

def receive_messages():
    while True:
        try:
            # Receive the encrypted message from the server
            encrypted_message = client_socket.recv(1024)
            
            if not encrypted_message:
                break
            
            # Decrypt the message
            decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
            
            print(decrypted_message)
        except Exception as e:
            print('Error:', str(e))
            break

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

def send_message():
    while True:
        # Get the message to send from the client
        message = input("Send Message : ")
        
        # Encrypt the message
        encrypted_message = cipher_suite.encrypt(message.encode())
        
        # Send the encrypted message to the server
        client_socket.send(encrypted_message)
        
        # Close the connection if the client requests it
        if message.lower() == 'disco':
            client_socket.close()
            sys.exit()

# Start a thread to send messages to the server
send_thread = threading.Thread(target=send_message)
send_thread.start()

# Wait for both threads to finish
receive_thread.join()
send_thread.join()
