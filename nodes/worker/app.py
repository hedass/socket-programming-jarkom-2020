import socket
import utils
import threading
from worker import code_runner

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(utils.WORKER_SOCK)

STATUS = 1 # Default FINISHED
AVAILABLE = 1 # Default ACTIVE

def handle_client(conn, addr):
    global STATUS, AVAILABLE
    print('Connected by', addr)

    header = conn.recv(utils.BUFF_SIZE).decode()

    if header:
        token = header[:-2]
        flag = header[-2:]

        if token != utils.TOKEN:
            conn.sendall("FATAL: Authentication Error".encode())
        
        elif flag == utils.GET_STATUS:
            utils.send(conn, STATUS)

        elif flag == utils.GET_AVAIL:
            # Ngubah STATUS
            utils.send(conn, AVAILABLE)

        elif flag == utils.EXEC_FLAG:
            # cek semua worker apakah available
            code = utils.receive_data(conn)
            STATUS = 2
            AVAILABLE = 3
            output = code_runner.run(code[1:].encode(), utils.LANGUAGE_LOOKUP[int(code[0])])
            STATUS = 1
            utils.send(conn, output)
            AVAILABLE = 1

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
