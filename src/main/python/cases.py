import random
import threading
from configparser import ConfigParser
from typing import Optional, List

from src.main.python.client import Client
from src.main.python.create_message import random_message, create_message
from src.main.python.malicious_client import MaliciousClient
from src.main.python.server import Server

class Scenario:
    """
    A class representing different scenarios for client-server interactions.
    """

    def __init__(self):
        self.server_thread = None
        self.client = None
        self.creation_message = random_message
        self.client_class = None
        self.iterations = 0
        self.modification_keys: Optional[List[str]] = None
        self.replay_count = 0

    def run(self):
        """
        Executes the scenario by sending messages between the client and server.
        """
        try:
            for _ in range(self.iterations):
                message = self.creation_message()
                for _ in range(self.replay_count):
                    if self.modification_keys:
                        self.client.send_message(message, keys=self.modification_keys)
                    else:
                        self.client.send_message(message)
                    self.client.receive_message()
        except KeyboardInterrupt:
            self.stop_client()
            self.stop_server()

    def start_server(self):
        """
        Starts the server in a separate thread.
        """
        config = ConfigParser()
        config.read("config.ini")

        host = config.get("SERVER", "host")
        port = config.get("SERVER", "port")

        self.server = Server(host, port, True)
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.start()

    def stop_server(self):
        """
        Stops the server thread.
        """
        # Mata el proceso del servidor
        self.server.stop()
        self.server_thread.join()


    def start_client(self):
        """
        Starts the client and establishes a connection.
        """
        config = ConfigParser()
        config.read("config.ini")

        host = config.get("SERVER", "host")
        port = config.get("SERVER", "port")

        self.client = self.client_class(host, int(port))
        self.client.connect()

    def stop_client(self):
        """
        Closes the client connection.
        """
        self.client.close()

    def fine_scenario(self, iterations: Optional[int] = None):
        """
        Executes the fine scenario where a clean client communicates with the server.

        Args:
            iterations (int): Number of iterations for the scenario.
        """
        self.client_class = Client
        self.iterations = iterations or random.randint(1, 10)
        self.modification_keys = []
        self.replay_count = 1

    def modification_scenario(self, iterations: Optional[int] = None, modification_keys: Optional[List[str]] = None, replay_count: int = 1):
        """
        Executes the modification scenario where a malicious client modifies specific keys in the message.

        Args:
            iterations (int): Number of iterations for the scenario.
            modification_keys (Optional[List[str]]): Keys to be modified in the message.
            replay_count (int): Number of times to replay messages in the replay scenario.
        """
        self.client_class = MaliciousClient
        self.iterations = iterations or random.randint(1, 10)
        self.modification_keys = modification_keys or ['origin_account', 'receiver_account', 'amount']
        self.replay_count = replay_count

    def replay_scenario(self, iterations: Optional[int] = None, replay_count: Optional[int] = None):
        """
        Executes the replay scenario where a malicious client replays messages multiple times.

        Args:
            iterations (int): Number of iterations for the scenario.
            replay_count (int): Number of times to replay messages.
        """
        self.client_class = MaliciousClient
        self.iterations = iterations or random.randint(2, 10)
        self.modification_keys = []
        self.replay_count = replay_count or random.randint(2, 10)

    def modification_and_replay_scenario(self, iterations: Optional[int] = None, modification_keys: Optional[List[str]] = None, replay_count: Optional[int] = None):
        """
        Executes the modification_and_replay scenario where a malicious client modifies a message and replays it.

        Args:
            iterations (int): Number of iterations for the scenario.
            modification_keys (Optional[List[str]]): Keys to be modified in the message.
            replay_count (int): Number of times to replay messages.
        """
        self.client_class = MaliciousClient
        self.iterations = iterations or random.randint(2, 10)
        self.modification_keys = modification_keys or ['origin_account', 'receiver_account', 'amount']
        self.replay_count = replay_count or random.randint(2, 10)

def run_aleatory(iterations: int):
    """
    Runs random scenarios for the specified number of iterations.

    Args:
        iterations (int): Number of iterations.
    """
    scenarios = [
        'fine_scenario',
        'modification_scenario',
        'replay_scenario',
        'modification_and_replay_scenario'
    ]

    weights = [200, 3, 2, 1]  # Adjust weights based on desired probabilities
    scenario = Scenario()

    scenario.start_server()

    for _ in range(iterations):
        selected_scenario = random.choices(scenarios, weights=weights)[0]
        getattr(scenario, selected_scenario)()
        scenario.start_client()
        scenario.run()
        scenario.stop_client()

    scenario.stop_server()





