class JSONResponse:
    def __init__(self, status):
        self.status = status

    def to_dict(self):
        return {'origin_account': self.origin_account, 'reciever_account': self.reciever_account, 'amount': self.amount}


def create_response(message):
    #status = check_integrity
    message = JSONMessage(origin_account, reciever_account, amount)
    message_dict = message.to_dict()
    message_json = json.dumps(message_dict, ensure_ascii=False).encode('utf-8')

    return message_json