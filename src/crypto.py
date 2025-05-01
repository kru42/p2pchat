from nacl.public import PrivateKey, Box
from nacl.encoding import Base64Encoder
from nacl.exceptions import CryptoError

class CryptoIdentity:
    def __init__(self):
        self.priv = PrivateKey.generate()
        self.pub = self.priv.public_key

    def get_pubkey_b64(self):
        return self.pub.encode(encoder=Base64Encoder).decode()

    def encrypt(self, message: bytes, peer_pubkey_b64: str) -> bytes:
        peer_pubkey = self._decode_pubkey(peer_pubkey_b64)
        box = Box(self.priv, peer_pubkey)
        return box.encrypt(message)

    def decrypt(self, ciphertext: bytes, peer_pubkey_b64: str) -> bytes:
        peer_pubkey = self._decode_pubkey(peer_pubkey_b64)
        box = Box(self.priv, peer_pubkey)
        try:
            return box.decrypt(ciphertext)
        except CryptoError:
            return b"[DECRYPTION FAILED]"

    def _decode_pubkey(self, b64: str):
        from nacl.public import PublicKey
        return PublicKey(b64.encode(), encoder=Base64Encoder)
