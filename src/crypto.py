from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder
from nacl.exceptions import CryptoError

class KeyPair:
    def __init__(self):
        self.private_key = PrivateKey.generate()
        self.public_key = self.private_key.public_key

    def public_key_b64(self) -> str:
        return self.public_key.encode(encoder=Base64Encoder).decode()

    def encrypt(self, message: bytes, peer_pubkey_b64: str) -> bytes:
        peer_pubkey = PublicKey(peer_pubkey_b64.encode(), encoder=Base64Encoder)
        box = Box(self.private_key, peer_pubkey)
        return box.encrypt(message)

    def decrypt(self, ciphertext: bytes, peer_pubkey_b64: str) -> bytes:
        peer_pubkey = PublicKey(peer_pubkey_b64.encode(), encoder=Base64Encoder)
        box = Box(self.private_key, peer_pubkey)
        try:
            return box.decrypt(ciphertext)
        except CryptoError:
            return b"[DECRYPTION FAILED]"
