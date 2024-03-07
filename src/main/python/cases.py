import threading
from configparser import ConfigParser
from typing import Optional, List

from src.main.python.client import Client
from src.main.python.json_message import create_message
from src.main.python.malicious_client import MaliciousClient
from src.main.python.server import Server


def run_scenario(client_class: type, modification_keys: Optional[List[str]] = None, replay_count: int = 1) -> None:
    """
    Executes a specific scenario with the provided client class and optional modification keys.

    Args:
        client_class (type): The client class to be used (Client or MaliciousClient).
        modification_keys (Optional[List[str]]): Keys to be modified in the message for malicious scenarios.
        replay_count (int): Number of times to replay messages in the replay scenario.
    """
    config = ConfigParser()
    config.read("config.ini")

    # SERVER
    host = config.get("SERVER", "host")
    port = config.get("SERVER", "port")

    server = Server(host, int(port))
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    client = client_class(host, int(port))
    client.connect()

    try:
        for _ in range(replay_count):
            message = create_message()

            if modification_keys:
                client.send_message(message, keys=modification_keys)
            else:
                client.send_message(message)

            response = client.receive_message()
            print(response)
    except KeyboardInterrupt:
        client.close()

    server_thread.join()

def fine() -> None:
    """
    Executes the fine scenario, where a clean client communicates with the server.
    """
    run_scenario(Client)

def modification_message() -> None:
    """
    Executes the modification_message scenario, where a malicious client modifies specific keys in the message.
    """
    run_scenario(MaliciousClient, modification_keys=['origin_account', 'receiver_account', 'amount'])

def replay() -> None:
    """
    Executes the replay scenario, where a malicious client replays messages multiple times.
    """
    run_scenario(MaliciousClient, replay_count=5)

def modification_and_replay() -> None:
    """
    Executes the modification_and_replay scenario, where a malicious client modifies a message and replays it.
    """
    run_scenario(MaliciousClient, modification_keys=['origin_account', 'receiver_account', 'amount'], replay_count=2)


