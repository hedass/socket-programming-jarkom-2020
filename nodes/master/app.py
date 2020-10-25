import socket
import threading
import uuid
from collections import deque

import utils

# uuid4 is random so should be thread-safe on different keys
jobs = dict()
jobs_output = dict()

# deque is thread-safe
jobs_queue = deque()


def forward_code(job_id, code, flag):
    global jobs_output

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.WORKER_SOCK)
        utils.send_data(s, job_id + code, flag.value)


def handle_connection(conn, addr):
    global jobs, jobs_queue

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
                utils.send_flag(s, flag.value)
                output = utils.receive_data(s)
                utils.send(conn, output)

        elif flag == utils.Request.GET_WORKER_STATUS:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(utils.WORKER_SOCK)
                utils.send_flag(s, flag.value)
                output = utils.receive_data(s)
                utils.send(conn, output)

        elif flag == utils.Request.EXECUTE_JOB:
            code = utils.receive_data(conn)
            job_id = str(uuid.uuid4())
            thread = threading.Thread(target=forward_code,
                                      args=(job_id, code, flag))
            jobs[job_id] = thread
            jobs_queue.append(job_id)

        elif flag == utils.Request.GET_OUTPUT:
            # TODO
            pass

    conn.close()
    print('Disconnected from', addr)


utils.start(utils.MASTER_SOCK, jobs, jobs_queue, handle_connection)
