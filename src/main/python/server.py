import concurrent.futures
import os
import socket
import threading
import time
from typing import Callable

import select

from src.main.python.logger import load_logger


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
        Process incoming messages and perform corresponding actions.

        Args:
            received_message (str): The received message.

        Returns:
            str: The response message.
        """
        # TODO: Modify this function to perform actions based on the received message
        message = f"Received message: {received_message}"
        return message
