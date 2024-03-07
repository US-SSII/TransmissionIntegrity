import hashlib
from configparser import ConfigParser
from datetime import datetime


def select_hash_algorithm(day: int) -> str:
    """
    Selects the hash algorithm based on the day of the month.

    Args:
        day (int): The day of the month.

    Returns:
        str: The selected hash algorithm ('sha512' or 'sha3_384').
    """
    return 'sha512' if day % 2 == 0 else 'sha3_384'



def get_hash(name: str, nonce: str, date_today: datetime) -> str:
    """
    Calculates the hash of a file using different algorithms and applies a Message Authentication Code (MAC).

    Args:
        name (str): The name or path of the file.
        date_today (datetime): The current date.

    Returns:
        str: The final hash value after applying MAC.
    """
    day = int(date_today.strftime('%d'))

    # Read the token from the configuration file
    config = ConfigParser()
    config.read("config.ini")
    token = config.get("HASHING", "token")

    # Calculate the MAC using the hash and token
    calculated_mac = hashlib.new(select_hash_algorithm(day))

    if day % 3 == 0:
        calculated_mac.update((token + name + nonce).encode())
    elif day % 3 == 1:
        calculated_mac.update((name + token + nonce).encode())
    else:
        calculated_mac.update((nonce + name + token).encode())

    return calculated_mac.hexdigest()
