import json


class JSONMessage:
    def __init__(self, origin_account, reciever_account, amount):
        self.origin_account = origin_account
        self.reciever_account = reciever_account
        self.amount = amount

    def to_dict(self):
        return {'origin_account': self.origin_account, 'reciever_account': self.reciever_account, 'amount': self.amount}

def create_message():
    origin_account = input("Origen: ")
    reciever_account = input("Destino: ")
    amount = input("Cantidad: ")

    message = JSONMessage(origin_account, reciever_account, amount)
    message_dict = message.to_dict()
    message_json = json.dumps(message_dict, ensure_ascii=False).encode('utf-8')

    return message_json

