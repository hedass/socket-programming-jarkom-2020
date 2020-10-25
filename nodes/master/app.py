from json.decoder import JSONDecodeError
import socket
import threading
import uuid
from collections import deque
import json

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
            job_id = utils.receive_data(conn)
            if job_id in jobs_output:
                utils.send(conn, utils.JobStatus.FINISHED.value)
            else:
                utils.send(conn, utils.JobStatus.WAITING.value)

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
            utils.send(conn, job_id)

        elif flag == utils.Request.GET_OUTPUT:
            job_id = utils.receive_data(conn)
            if job_id in jobs_output:
                utils.send(conn, jobs_output.get(job_id))
            elif job_id not in jobs:
                utils.send(conn, "FATAL: job id doesn't exist")
            else: 
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(utils.WORKER_SOCK)
                    utils.send_data(s, job_id, flag.value)
                    output = utils.receive_data(s)
                    try:
                        json.loads(output)
                        jobs_output[job_id] = output
                    except JSONDecodeError as e:
                        pass
                    utils.send(conn, output)

    conn.close()
    print('Disconnected from', addr)


utils.start(utils.MASTER_SOCK, jobs, jobs_queue, handle_connection)
