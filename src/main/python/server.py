import json
import socket
import threading

import select

from src.main.python.integrity_verifier import validate_message
from src.main.python.logger import load_logger
from src.main.python.nonce import NonceManager


class Server:
    """
    This class implements a simple TCP server that listens for incoming connections
    and sends back a response to any message it receives. The server also tracks the
    number of messages it has received and returns that count in its response.
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Initialize the server with the specified host and port.

        Args:
            host (str): The hostname or IP address to bind to.
            port (int): The port number to listen on.
        """
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self) -> None:
        """
        Start the server listening for incoming connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Increased the number of connections in the queue
        load_logger()

        # Execute self.repository.all_files() in the background every 10 seconds

        while True:
            client_socket, _ = self.server_socket.accept()  # Accept incoming connection

            # Handle communication with the client in a separate thread
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket: socket) -> None:
        """
        Handle an incoming client connection by sending a response to any messages it sends.

        Args:
            client_socket (socket): The socket for the incoming connection.
        """
        try:
            while True:
                try:
                    active, _, _ = select.select([client_socket], [], [], 1)

                    if len(active) == 0:
                        continue

                    data = client_socket.recv(1024)  # Receive data from the client
                    if not data:
                        break  # If no data, the client has closed the connection

                    received_message = data.decode()

                    message = self.actions(received_message)

                    chunk_size = 512
                    for i in range(0, len(message), chunk_size):
                        chunk = message[i:i + chunk_size]
                        client_socket.sendall(chunk.encode("utf-8"))

                    # Send the end indicator
                    client_socket.sendall("END".encode("utf-8"))

                except socket.timeout:
                    pass  # Timeout reached, continue with the next cycle

        except Exception:
            pass
        finally:
            client_socket.close()

    def actions(self, received_message: str) -> str:
        """
        Orchestrates a series of actions based on the received message.

        Actions:
            1. Save the nonce.
            2. Invoke the integrity verifier to detect tampering.
               - Returns 'Integrity Failed' on verification failure.
            3. Verify the uniqueness of the nonce.
               - Returns 'Nonce repeated' if repeated.
            4. If both integrity check and nonce validation succeed, returns 'OK'.
            5. Sends an appropriate response to the client.
        """
        nonce_manager = NonceManager("../resources/nonces.json")

        message_dict = json.loads(received_message)

        if validate_message(message_dict["message"], message_dict["nonce"], message_dict["date"], message_dict["mac"]):
            if nonce_manager.not_repeated(message_dict["nonce"]):
                message = f"Received message: {received_message}"
            else:
                message = "Nonce Repeated"
        else:
            message = "Integrity Failed"

        return message
