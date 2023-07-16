import socket
import threading

# XOR encryption functions
def xor_encrypt(message, key):
    encrypted = ""
    for i in range(len(message)):
        encrypted += chr(ord(message[i]) ^ ord(key[i % len(key)]))
    return encrypted

def xor_decrypt(ciphertext, key):
    decrypted = ""
    for i in range(len(ciphertext)):
        decrypted += chr(ord(ciphertext[i]) ^ ord(key[i % len(key)]))
    return decrypted

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# Chat server class
class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((SERVER_HOST, SERVER_PORT))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    def broadcast_message(self, message, sender):
        encrypted_message = xor_encrypt(message, sender.key)
        for client in self.clients:
            if client != sender:
                client.socket.send(encrypted_message.encode())

    def handle_client(self, client):
        while True:
            try:
                encrypted_message = client.socket.recv(1024).decode()
                message = xor_decrypt(encrypted_message, client.key)
                self.broadcast_message(message, client)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.socket.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast_message(f'{nickname} left the chat!', client)
                break

    def start(self):
        while True:
            client_socket, client_address = self.server.accept()
            client = ChatClient(client_socket)
            nickname = client.socket.recv(1024).decode()
            client.set_nickname(nickname)
            self.clients.append(client)
            self.nicknames.append(nickname)
            self.broadcast_message(f'{nickname} joined the chat!', client)
            client.socket.send('Connected to the server!'.encode())
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()

# Chat client class
class ChatClient:
    def __init__(self, socket):
        self.socket = socket
        self.key = "secretkey"

    def set_nickname(self, nickname):
        self.nickname = nickname

# Main function
def main():
    server = ChatServer()
    server.start()

if __name__ == '__main__':
    main()
