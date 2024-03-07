import threading
from configparser import ConfigParser

from src.main.python.client import Client
from src.main.python.json_message import create_message
from src.main.python.malicious_client import MaliciousClient
from src.main.python.server import Server


def fine():
    config = ConfigParser()
    config.read("config.ini")

    # SERVER
    host = config.get("SERVER", "host")
    port = config.get("SERVER", "port")

    server = Server(host, int(port))
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    client = Client(host, int(port))
    client.connect()

    try:
        while True:
            message = create_message()
            client.send_message(message)
            response = client.receive_message()
            print(response)
    except KeyboardInterrupt:
        client.close()

    server_thread.join()

def modification_message():
    config = ConfigParser()
    config.read("config.ini")

    # SERVER
    host = config.get("SERVER", "host")
    port = config.get("SERVER", "port")

    server = Server(host, int(port))
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    client = MaliciousClient(host, int(port))
    client.connect()

    try:
        while True:
            message = create_message()
            client.send_message(message, keys=['origin_account', 'receiver_account', 'amount'])
            response = client.receive_message()
            print(response)
    except KeyboardInterrupt:
        client.close()

    server_thread.join()

def replay(self):
    config = ConfigParser()
    config.read("config.ini")

    # SERVER
    host = config.get("SERVER", "host")
    port = config.get("SERVER", "port")

    server = Server(host, int(port))
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    client = MaliciousClient(host, int(port))
    client.connect()

    try:
        while True:
            message = create_message()
            for _ in range(5):
                client.send_message(message)
                response = client.receive_message()
                print(response)
    except KeyboardInterrupt:
        client.close()

    server_thread.join()