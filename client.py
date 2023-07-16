import socket
import threading

# XOR encryption functions
def xor_encrypt(message, key):
    encrypted = b""
    for i in range(len(message)):
        encrypted += bytes([message[i] ^ key[i % len(key)]])
    return encrypted

def xor_decrypt(ciphertext, key):
    decrypted = b""
    for i in range(len(ciphertext)):
        decrypted += bytes([ciphertext[i] ^ key[i % len(key)]])
    return decrypted

# Client configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# Chat client class
class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, nickname):
        self.client.connect((SERVER_HOST, SERVER_PORT))
        self.client.send(nickname.encode())
        self.key = b"secretkey"
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

    def send_message(self, message):
        encrypted_message = xor_encrypt(message.encode(), self.key)
        self.client.send(encrypted_message)

    def receive_message(self):
        while True:
            try:
                encrypted_message = self.client.recv(1024)
                message = xor_decrypt(encrypted_message, self.key).decode()
                print(message)
            except:
                print("An error occurred. Disconnected from the server.")
                self.client.close()
                break

# Main function
def main():
    nickname = input("Enter your nickname: ")
    client = ChatClient()
    client.connect(nickname)

    while True:
        message = input("> ")
        if message.lower() == 'exit':
            break
        client.send_message(message)

if __name__ == '__main__':
    main()
