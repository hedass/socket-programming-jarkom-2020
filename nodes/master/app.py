from socket import SOCK_STREAM
import threading
import socket
import utils
from utils import WORKER_SOCK


def handle_client(conn, addr):
    print('Connected by', addr)

    header = conn.recv(utils.HEADER_SIZE).decode()

    if header:
        token = header[:-1]
        flag = utils.Request(int(header[-1:]))

        if token != utils.TOKEN:
            utils.send(conn, "FATAL: Authentication Error")

        elif flag == utils.Request.GET_JOB_STATUS:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(utils.WORKER_SOCK)
                utils.send_flag(s, flag)
                output = utils.receive_data(s)
                utils.send(conn, output)

        elif flag == utils.Request.GET_WORKER_STATUS:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(utils.WORKER_SOCK)
                utils.send_flag(s, flag)
                output = utils.receive_data(s)
                utils.send(conn, output)

        elif flag == utils.Request.EXECUTE_JOB:
            code = utils.receive_data(conn)
            # TODO cek semua worker apakah available
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(utils.WORKER_SOCK)
                utils.send_data(s, code, flag)
                output = utils.receive_data(s)
                utils.send(conn, output)

        elif flag == utils.Request.GET_OUTPUT:
            job_id = utils.receive_data(conn)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(WORKER_SOCK)
                utils.send_data(s, job_id, flag)
                job_id = utils.receive_data(s)
                utils.send(conn, job_id)

    conn.close()
    print('Disconnected from', addr)


def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(utils.MASTER_SOCK)
        s.listen(1)
        print('Server is listening on', utils.MASTER_SOCK)

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


start()
