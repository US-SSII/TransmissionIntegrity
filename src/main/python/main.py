import time

from src.main.python.cases import *
from src.main.python.statistics import create_report


def start_connection():
    config = ConfigParser()
    config.read("config.ini")

    host = config.get("SERVER", "host")
    port = config.get("SERVER", "port")

    server = Server(host, int(port))
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    client = Client(host, int(port))
    client.connect()

    while True:
        time.sleep(0.1)
        client.send_message(create_message())
        response = client.receive_message()
        print(response)
        time.sleep(0.1)
        want_continue = input("Do you want to continue? (y/n): ")
        if want_continue.lower() != "y":
            break
    client.close()
    server.stop()
    server_thread.join()
    create_report()
    print("The client has been shut down successfully.")

if __name__ == '__main__':
    print("What did you want to do? \n 1. Start connection \n 2. Run test cases")
    option = input("Option: ")
    if option == "1":
        start_connection()
    elif option == "2":
        while True:
            print("How many iterations do you want to run?")
            iterations = input("Iterations: ")
            if iterations.isdigit():
                iterations = int(iterations)
                break
        run_aleatory(iterations)
    else:
        print("You must specify")
