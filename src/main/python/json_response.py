class JSONResponse:
    def __init__(self, status):
        self.status = status

    def to_dict(self):
        return {'origin_account': self.origin_account, 'reciever_account': self.reciever_account, 'amount': self.amount}


def create_response(message:str):
    #status = check_integrity

    return message_json