import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

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

        # Receive the encrypted message
        encrypted_message = conn.recv(1024)
        app.send_message(f"Encrypted message from {addr}: {binascii.hexlify(encrypted_message)}")

        # Decrypt the message using the server's private key
        decryptor = PKCS1_OAEP.new(keyPair)
        decrypted_message = decryptor.decrypt(encrypted_message)
        app.send_message(f"Decrypted message from {addr}: {decrypted_message.decode()}")
    except Exception as e:
        app.send_message(f"Error with {addr}: {e}")
    finally:
        conn.close()
        app.send_message(f"Connection with {addr} closed.")

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
