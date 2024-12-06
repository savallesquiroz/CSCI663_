import base64
import json
import os

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Cipher import AES

BLOCK_SIZE = 16

random_generator = Random.new().read

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
    chr(BLOCK_SIZE - len(s) % BLOCK_SIZE).encode()
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def get_random_key_readable(key_size):
    ulen = int(key_size/4*3)
    key = base64.b64encode(os.urandom(ulen))
    return key

def encrypt(msg: bytes, key_rsa_pub: bytes):
    # generate aes key
    key_aes_rand = get_random_key_readable(BLOCK_SIZE)

    # Encrypt the original information with AES and base64 (urlsafe_b64encode is required for network transmission)
    encrypted_msg = AES.new(key_aes_rand, AES.MODE_ECB).encrypt(pad(msg))
    base64ed_encrypted_msg = base64.urlsafe_b64encode(encrypted_msg)

    # RSA encryption is performed on the AES random key
    encrypted_key_aes_rand = Cipher_pkcs1_v1_5.new(RSA.importKey(key_rsa_pub)).encrypt(key_aes_rand)

    base64ed_encrypted_key_aes_rand = base64.urlsafe_b64encode(encrypted_key_aes_rand)
    return json.dumps([base64ed_encrypted_msg.decode(), base64ed_encrypted_key_aes_rand.decode()]).encode()

def decrypt(source: list, key_rsa_pri: bytes):
    # Split the received data into base64ed_encrypted_msg and base64ed_encrypted_key_aes_rand
    base64ed_encrypted_msg, base64ed_encrypted_key_aes_rand = source[0], source[1]

    # Performs base64 decryption on base64ed_encrypted_key_aes_rand to obtain encrypted_key_aes_rand
    encrypted_key_aes_rand = base64.urlsafe_b64decode(base64ed_encrypted_key_aes_rand)

    # To decrypt encrypted_key_aes_rand, use the RSA private key key_rsa_pri to obtain key_aes_rand
    key_aes_rand = Cipher_pkcs1_v1_5.new(RSA.importKey(key_rsa_pri)).decrypt(encrypted_key_aes_rand, random_generator)

    encrypted_msg = base64.urlsafe_b64decode(base64ed_encrypted_msg)
    msg = unpad(AES.new(key_aes_rand, AES.MODE_ECB).decrypt(encrypted_msg))
    return msg
