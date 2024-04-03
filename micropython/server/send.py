# TODO:
# 1- Slice Data
# 2- Send Data
# 3- Recieve Data
import socket
import time

def client_program():
    host = "192.168.4.1"
    port = 80

    client_socket = socket.socket()
    client_socket.connect((host, port))

    f = open("test.raw", "rb")
    size = int(len(f.read()) / 2048)
    f.seek(0)

    for i in range(size):
        chunk = f.read(2048)
        # print(chunk)
        client_socket.send(chunk)

    client_socket.close()  # close the connection


if __name__ == "__main__":
    client_program()
