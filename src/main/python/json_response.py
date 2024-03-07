import json


class JSONResponse:
    def __init__(self, status):
        self.status = status

    def to_dict(self):
        return {'status': self.status}


def create_response(server_response:str):
    response = JSONResponse(server_response)
    response_dict = response.to_dict()
    response_json = json.dumps(response_dict, ensure_ascii=False)

    return response_json