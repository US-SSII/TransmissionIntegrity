from datetime import datetime

from src.main.python.hashing import calculate_mac


def validate_message(message: str, nonce: str, date_today: datetime, expected_hash: str) -> bool:
    """
    Validates the integrity of a message by comparing the calculated hash with the expected hash.

    Args:
        message (str): The message content to be validated.
        nonce (str): Nonce value used in the message hashing process.
        date_today (datetime): The current date and time.
        expected_hash (str): The expected hash value for validation.

    Returns:
        bool: True if the message integrity is valid, False otherwise.
    """
    # Calculate the hash for the received message
    calculated_hash = calculate_mac(message, nonce, date_today)

    # Compare the calculated hash with the expected hash
    return calculated_hash == expected_hash
