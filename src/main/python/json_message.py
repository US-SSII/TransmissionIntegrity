import hashlib
import hmac
import json
from configparser import ConfigParser
from datetime import datetime

from src.main.python.hashing import get_hash
from src.main.python.nonce import NonceManager


class JSONMessage:
    def __init__(self, origin_account, reciever_account, amount):
        self.origin_account = origin_account
        self.reciever_account = reciever_account
        self.amount = amount

    def to_dict(self):
        return {'origin_account': self.origin_account, 'reciever_account': self.reciever_account, 'amount': self.amount}

def create_message():
    '''
    :input: Cuenta origen, Cuenta destino, Cantidad
    :return: JSON, Resumen MAC

    Debe hacer el resumen MAC tomando el JSON, KEY y aplicando Nounce
    '''
    nonce_manager=NonceManager("../resources/nonces.json")
    origin_account = input("Origen: ")
    reciever_account = input("Destino: ")
    amount = input("Cantidad: ")

    message = JSONMessage(origin_account, reciever_account, amount)
    message_dict = message.to_dict()
    json_str= str(message_dict)

    nonce= nonce_manager.generate()
    hashing_hmac = get_hash(json_str, nonce, datetime.now())

    message_dict["nonce"]=nonce
    message_dict["mac"] = hashing_hmac
    message_dict["date"] = datetime.now()
    message_json = json.dumps(message_dict, ensure_ascii=False)

    return message_json

