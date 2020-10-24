import socket
import utils
from time import sleep
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(utils.WORKER_SOCK)


def handle_client(conn, addr):
    print('Connected by', addr)

    header = conn.recv(utils.BUFF_SIZE).decode()

    if header:
        token = header[:-2]
        flag = header[-2:]

        if token != utils.TOKEN:
            conn.sendall("FATAL: Authentication Error".encode())
        elif flag == utils.EXEC_FLAG:
            # cek semua worker apakah available
            code = utils.receive_data(conn)
            conn.sendall(f"kodingan anda bagus {utils.EOF}".encode())

    conn.close()
    print('Disconnected from', addr)


def start():
    server.listen(1)
    print('Server is listening on', utils.WORKER_SOCK)

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()
server.close()
