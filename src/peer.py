import socket
import threading
import socks

def listen_for_messages(identity, peer_pubkey_b64):
    s = socket.socket()
    s.bind(('127.0.0.1', 12345))
    s.listen(1)
    print("[*] Listening for messages...")

    while True:
        conn, _ = s.accept()
        data = conn.recv(4096)
        if data:
            msg = identity.decrypt(data, peer_pubkey_b64)
            print(f"\n[RECEIVED] {msg.decode(errors='ignore')}")
        conn.close()

def send_message(identity, peer_pubkey_b64, peer_onion):
    msg = input("Enter message: ").encode()
    encrypted = identity.encrypt(msg, peer_pubkey_b64)

    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    s.connect((peer_onion, 12345))
    s.sendall(encrypted)
    s.close()
