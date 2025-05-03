from stem.control import Controller
import os
import time
import subprocess
import platform

def _get_tor_binary():
    os_name = platform.system().lower()
    if os_name == "windows":
        return os.path.abspath("tor/windows/tor.exe")
    elif os_name == "linux":
        return os.path.abspath("tor/linux/tor")
    elif os_name == "darwin":
        return os.path.abspath("tor/mac/tor")
    else:
        raise RuntimeError("Unsupported OS")

def launch_tor_if_needed():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            return  # Already running
    except:
        pass

    tor_path = _get_tor_binary()
    torrc = os.path.abspath("tor/torrc")
    subprocess.Popen([tor_path, "-f", torrc])
    print("[tor_control] Launching Tor...")

    # Wait until control port is up
    for _ in range(30):
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                print("[tor_control] Connected to Tor control port.")
                return
        except:
            time.sleep(1)
    raise RuntimeError("Tor did not start")

def start_hidden_service():
    launch_tor_if_needed()

    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        hidden_service_dir = "tor/hidden_service"
        os.makedirs(hidden_service_dir, exist_ok=True)

        result = controller.create_hidden_service(
            hidden_service_dir,
            80,
            target_port=5000  # Assumes your app listens here
        )
        onion_address = result.service_id + ".onion"
        print(f"[tor_control] Hidden service is {onion_address}")
        return onion_address
