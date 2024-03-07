import threading
from configparser import ConfigParser
from datetime import time

from server import Server
from src.main.python.client import Client
from src.main.python.json_message import create_message

if __name__ == '__main__':
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




