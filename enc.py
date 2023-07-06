def encrypt(message, key):
    encrypted_message = ""
    for char in message:
        encrypted_message += chr(ord(char) ^ ord(key))
    return encrypted_message


def decrypt(encrypted_message, key):
    decrypted_message = ""
    for char in encrypted_message:
        decrypted_message += chr(ord(char) ^ ord(key))
    return decrypted_message

key = 'A'
message = "Nikesh123@#"

encrypted = encrypt(message, key)
print("Encrypted message:", encrypted)

decrypted = decrypt(encrypted, key)
print("Decrypted message:", decrypted)
