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


def handle_client(conn, addr):
    try:
        print(f"Connected by {addr}")

        # Send the server's public key to the client
        conn.sendall(pubKeyPEM)
        print(f"Public key sent to {addr}.")

        # Receive the encrypted message
        encrypted_message = conn.recv(1024)
        print(f"Encrypted message from {addr}: {binascii.hexlify(encrypted_message)}")

    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server started. Listening on {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == "__main__":
    start_server()
