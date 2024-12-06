import socket
import threading
from Crypto.PublicKey import RSA
import binascii
import aes_rsa as aes
import json
import tkinter as tk
from time import sleep
import select

# Generate RSA key pair (Kade's code integration)
keyPair = RSA.generate(3072)
pubKey = keyPair.publickey()
pubKeyPEM = pubKey.exportKey()
privKeyPEM = keyPair.exportKey()

# Server Configuration
HOST = '127.0.0.1'
PORT = 65432

def handle_client(conn, addr, app):
    try:
        app.send_message(f"Connected by {addr}")

        # Send the server's public key to the client
        conn.sendall(pubKeyPEM)
        app.send_message(f"Public key sent to {addr}.")

        while True:
            # Receive the encrypted message
            encrypted_message, key = json.loads(handle_messages(conn, app).decode())
            encrypted_message = encrypted_message.encode()
            key = key.encode()

            # Decrypt the message using the server's private key and the AES key
            decrypted_message = aes.decrypt([encrypted_message, key], privKeyPEM)
            app.send_message(f"Decrypted message from {addr}: {decrypted_message.decode()}")
            app.message_area.yview(tk.END)

    except Exception as e:
        app.send_message(f"Error with {addr}: {e}")

def handle_messages(conn, app):
    message = None
    while message is None:
        message = conn.recv(1024) if select.select([conn], [], [], 1) else None
        sleep(1)
    return message

def start_server(app):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            app.send_message(f"Server started. Listening on {HOST}:{PORT}...")

            while True:
                conn, addr = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(conn, addr, app))
                client_thread.start()
