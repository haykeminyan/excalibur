import socket
import time
import os

def wait_for_service(host, port, retries=5, delay=5):
    while retries > 0:
        try:
            with socket.create_connection((host, port), timeout=5):
                print(f"Service at {host}:{port} is available.")
                return
        except (socket.timeout, socket.error):
            retries -= 1
            print(f"Service at {host}:{port} not available. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise RuntimeError(f"Service at {host}:{port} not available after multiple retries.")

if __name__ == "__main__":
    host = os.environ.get("SERVICE_HOST", "rabbitmq")
    port = int(os.environ.get("SERVICE_PORT", "5672"))
    wait_for_service(host, port)
