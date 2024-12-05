import socket
from Crypto.Cipher import PKCS1_OAEP
import aes_encryption as aes
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import binascii
import gui
import tkinter as tk
from time import sleep

# Server Configuration
HOST = '127.0.0.1'
PORT = 65432

def start_client(app):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            app.send_message("Connected to server.")

            # Receive the server's public key
            server_public_key_pem = client_socket.recv(2048)
            server_public_key = RSA.importKey(server_public_key_pem)
            app.send_message("Received server's public key.")

            while True:
                # Generate the AES key
                aes_key = get_random_bytes(16)

                # Encrypt the message using the AES key and the server's public key
                message = str(aes.encrypt(handle_messages(app) + str(aes_key), aes_key)).encode()
                encryptor = PKCS1_OAEP.new(server_public_key)
                encrypted_message = encryptor.encrypt(message)
                app.send_message(f"Encrypted message:{binascii.hexlify(encrypted_message)}")

                # Send the encrypted message to the server
                client_socket.sendall(encrypted_message)
                app.send_message("Encrypted message sent to the server.")
                app.message_area.yview(tk.END)

    except Exception as e:
        app.send_message(f"Error: {e}")

def handle_messages(app):
    message = None
    while message is None:
        message = app.message_queue.get_nowait() if not app.message_queue.empty() else None
        sleep(1)
    return message
