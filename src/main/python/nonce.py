import uuid


class NonceManager:
    def generate_nonce(self):
        nonce = str(uuid.uuid4())
        return nonce
