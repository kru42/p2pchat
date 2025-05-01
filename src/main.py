from crypto import CryptoIdentity
from tor_control import start_hidden_service
from peer import listen_for_messages, send_message

import threading

identity = CryptoIdentity()
print(f"[You] Public key (b64): {identity.get_pubkey_b64()}")

my_onion = start_hidden_service()

# Spawn listener
peer_pubkey_b64 = input("Enter peer pubkey (b64): ")
threading.Thread(target=listen_for_messages, args=(identity, peer_pubkey_b64), daemon=True).start()

# Main loop
peer_onion = input("Enter peer .onion address: ")
while True:
    send_message(identity, peer_pubkey_b64, peer_onion)
