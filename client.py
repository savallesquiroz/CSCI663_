import socket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import binascii
import tkinter as tk 
from tkinter import messagebox

# Server Configuration
HOST = '127.0.0.1'
PORT = 65432


def start_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            print("Connected to server.")

            # Receive the server's public key
            server_public_key_pem = client_socket.recv(2048)
            server_public_key = RSA.importKey(server_public_key_pem)
            print("Received server's public key.")

            # Encrypt the message using the server's public key
            message = input("Enter your message: ").encode()
            encryptor = PKCS1_OAEP.new(server_public_key)
            encrypted_message = encryptor.encrypt(message)
            print("Encrypted message:", binascii.hexlify(encrypted_message))

            # Send the encrypted message to the server
            client_socket.sendall(encrypted_message)
            print("Encrypted message sent to the server.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    start_client()
