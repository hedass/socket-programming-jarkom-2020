import threading
import socket
import utils

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(utils.MASTER_SOCK)

STATUS = 1

def handle_client(conn, addr):
    print('Connected by', addr)

    header = conn.recv(utils.BUFF_SIZE).decode()

    if header:
        token = header[:-2]
        flag = header[-2:]

        if token != utils.TOKEN:
            conn.sendall("FATAL: Authentication Error".encode())
        elif flag == utils.EXEC_FLAG:
            code = utils.receive_data(conn)
            # cek semua worker apakah available
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(utils.WORKER_SOCK)
                utils.send_data(s, code, utils.EXEC_FLAG)
                output = utils.receive_data(s)
                conn.sendall(output.encode())

    conn.close()
    print('Disconnected from', addr)


def start():
    server.listen(1)
    print('Server is listening on', utils.MASTER_SOCK)

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()
server.close()
