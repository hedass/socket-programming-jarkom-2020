import socket
import threading
import utils
from worker import code_runner

STATUS = utils.JobStatus.FINISHED
AVAILABLE = utils.WorkerStatus.ACTIVE


def handle_client(conn, addr):
    global STATUS, AVAILABLE
    print('Connected by', addr)

    header = conn.recv(utils.HEADER_SIZE).decode()

    if header:
        token = header[:-1]
        flag = utils.Request(int(header[-1:]))

        if token != utils.TOKEN:
            utils.send(conn, "FATAL: Authentication Error")

        elif flag == utils.Request.GET_JOB_STATUS:
            utils.send(conn, STATUS.value)

        elif flag == utils.Request.GET_WORKER_STATUS:
            utils.send(conn, AVAILABLE.value)

        elif flag == utils.Request.EXECUTE_JOB:
            if (AVAILABLE != utils.WorkerStatus.ACTIVE):
                utils.send(conn, AVAILABLE.value)
                conn.close()
                return
            code = utils.receive_data(conn)
            STATUS = utils.JobStatus.RUNNING
            AVAILABLE = utils.WorkerStatus.BUSY
            output = code_runner.run(
                code[1:].encode(),
                utils.LanguageCode.list()[int(code[0]) - 1])
            STATUS = utils.JobStatus.FINISHED
            utils.send(conn, output)
            AVAILABLE = utils.WorkerStatus.ACTIVE

    conn.close()
    print('Disconnected from', addr)


def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(utils.WORKER_SOCK)
        s.listen(1)
        print('Server is listening on', utils.WORKER_SOCK)

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


start()
