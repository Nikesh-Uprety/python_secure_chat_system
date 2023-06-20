import socket
import threading
import paramiko

from cryptography.fernet import Fernet

# Generate a unique key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = 'localhost'
server_port = 8888

# Bind the socket to a specific address and port
server_socket.bind((server_host, server_port))

# Listen for incoming connections
server_socket.listen(5)
print('Server listening on {}:{}'.format(server_host, server_port))

# Dictionary to store client sockets and their corresponding usernames
clients = {}

# SSH key file paths
private_key_path = 'Ssh_Keys/NIK_KEYGEN.pem'
public_key_path = 'Ssh_Keys/NIK_KEYGEN.pub'

def check_auth(username, key):
    # Add your custom authentication logic here
    # You can check the username and public key against your authorized keys list or database
    # Return True if the authentication is successful, otherwise return False
    return True

def ssh_handler(client_channel, addr):
    username = client_channel.get_username()
    if username and check_auth(username, client_channel.get_remote_server_key()):
        clients[client_channel] = username
        print('Connected:', username)
        while True:
            try:
                command = client_channel.recv(1024)
                if not command:
                    break
                decrypted_message = cipher_suite.decrypt(command).decode()
                print('Received from', username + ':', decrypted_message)
                broadcast_message(client_channel, username + ': ' + decrypted_message)
            except Exception as e:
                print('Error:', str(e))
                break
        client_channel.close()
        del clients[client_channel]
        print('Disconnected:', username)
    else:
        print('Authentication failed for:', client_channel.get_username())
        client_channel.close()

def broadcast_message(sender, message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    for client_channel in clients:
        if client_channel != sender:
            client_channel.sendall(encrypted_message)

# Start the SSH server
while True:
    try:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        
        # SSH server configuration
        ssh_server = paramiko.Transport(client_socket)
        ssh_server.load_server_moduli()
        ssh_server.add_server_key(paramiko.RSAKey(filename=private_key_path))
        ssh_server.start_server(server=server_socket)
        
        # Create a new thread for the SSH client connection
        client_thread = threading.Thread(target=ssh_handler, args=(ssh_server, client_address))
        client_thread.start()
    except Exception as e:
        print('Error:', str(e))
        break

# Close the server socket
server_socket.close()
