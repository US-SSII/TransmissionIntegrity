from src.main.python.server import Server

if __name__ == "__main__":
    server = Server("0.0.0.0", 12345)
    server.start()