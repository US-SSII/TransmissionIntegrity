from src.main.python.client import Client


class MaliciousClient(Client):
    """
    The MaliciousClient class extends the Client class and overrides the send_message method to send a malicious message.
    """
    def send_message(self, message):
        """
        Sends a malicious message to the connected server.

        Args:
            message (str): The message to be sent.
        """
        super().send_message(self.alterate_message(message))

    def alterate_message(self, message):
        """
        Sends a malicious message to the connected server.

        Args:
            message (str): The message to be sent.
        """
        message = "Malicious message"
        return message
