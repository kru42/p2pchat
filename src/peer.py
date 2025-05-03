# src/peer.py

import threading
import socket
import socks  # PySocks
from typing import Callable
from crypto import KeyPair

class Peer:
    def __init__(self, onion_address: str, keypair: KeyPair, on_message: Callable[[bytes], None]):
        self.onion_address = onion_address
        self.keypair = keypair
        self.on_message = on_message
        self.sock = socks.socksocket()
        self.sock.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)

    def connect(self, port=12345):
        try:
            self.sock.connect((self.onion_address, port))
            threading.Thread(target=self._listen_loop, daemon=True).start()
        except Exception as e:
            print(f"[Peer] Connection failed: {e}")

    def send(self, message: bytes, peer_pubkey_b64: str):
        ciphertext = self.keypair.encrypt(message, peer_pubkey_b64)
        try:
            self.sock.sendall(ciphertext)
        except Exception as e:
            print(f"[Peer] Failed to send message: {e}")

    def _listen_loop(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if data:
                    # You may want to store the remote pubkey on first handshake
                    plaintext = self.keypair.decrypt(data, self.onion_address)  # Simplification
                    self.on_message(plaintext)
            except Exception as e:
                print(f"[Peer] Error receiving data: {e}")
                break
