import json
import uuid

import json
import uuid


class NonceManager:
    """
    NonceManager: Manage nonces to prevent replay attacks.
    """

    def __init__(self, path_old_nonces):
        """
        Initialize NonceManager.

        Args:
            path_old_nonces (str): Path to the file storing old nonces.
        """
        self.path_old_nonces = path_old_nonces

    def generate(self):
        """
        Generate a new nonce.

        Returns:
            str: Newly generated nonce.
        """
        return str(uuid.uuid4())

    def not_repeated(self, nonce):
        """
        Check if the nonce is not repeated and update the file accordingly.

        Args:
            nonce (str): Nonce to check.

        Returns:
            bool: True if the nonce is not repeated, False otherwise.
        """
        try:
            with open(self.path_old_nonces, "r") as file:
                old_nonces = json.load(file)
        except FileNotFoundError:
            old_nonces = []

        if nonce in old_nonces:
            return False
        else:
            old_nonces.append(nonce)
            with open(self.path_old_nonces, "w") as file:
                json.dump(old_nonces, file)
            return True

