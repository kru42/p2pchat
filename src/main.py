from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
)
from crypto import KeyPair
from tor_control import start_hidden_service
from peer import Peer
import sys
import threading


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("p2p Tor Chat")
        self.resize(400, 600)

        layout = QVBoxLayout()

        self.key_label = QLabel("Loading...")
        self.onion_label = QLabel("Starting Tor...")
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.peer_input = QLineEdit()
        self.peer_input.setPlaceholderText("Enter peer .onion")

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message")

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        layout.addWidget(self.key_label)
        layout.addWidget(self.onion_label)
        layout.addWidget(self.chat_display)
        layout.addWidget(self.peer_input)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.keypair = KeyPair()
        self.key_label.setText(f"Public Key: {self.keypair.public_key_b64()}")

        self.peer = Peer(
            onion_address="",
            keypair=self.keypair,
            on_message=self.receive_message,
        )
        threading.Thread(target=self.run_peer, daemon=True).start()

    def run_peer(self):
        onion = start_hidden_service()
        self.onion_label.setText(f"Your Onion: {onion}")
        self.peer.listen()

    def receive_message(self, msg):
        self.chat_display.append(f"[Peer] {msg}")

    def send_message(self):
        onion = self.peer_input.text().strip()
        msg = self.message_input.text().strip()
        if onion and msg:
            self.chat_display.append(f"[You] {msg}")
            threading.Thread(
                target=self.peer.send, args=(onion, msg), daemon=True
            ).start()
            self.message_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
