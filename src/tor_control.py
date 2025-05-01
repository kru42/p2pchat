from stem.control import Controller
import os

def start_hidden_service():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # uses cookie auth
        result = controller.create_ephemeral_hidden_service(
            {12345: 12345}, await_publication=True
        )
        onion = result.service_id + ".onion"
        print(f"[Tor] Hidden service started: {onion}:12345")
        return onion
