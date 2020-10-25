import os
import socket
import threading
import time
from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Request(ExtendedEnum):
    GET_WORKER_STATUS = 1
    GET_JOB_STATUS = 2
    EXECUTE_JOB = 3
    CANCEL_JOB = 4
    GET_OUTPUT = 5


class WorkerStatus(ExtendedEnum):
    ACTIVE = 1
    DEAD = 2
    BUSY = 3


class JobStatus(ExtendedEnum):
    FINISHED = 1
    RUNNING = 2
    FAILED = 3
    CANCELLED = 4


class LanguageCode(ExtendedEnum):
    python = 'python'
    java = 'text/x-java'


class SchedulerAlgorithm(ExtendedEnum):
    FCFS = 1
    LCFS = 2


MASTER_HOST = '127.0.0.1'
WORKER_HOST = '0.0.0.0'
MASTER_PORT = 6000
WORKER_PORT = 7000
MASTER_SOCK = (MASTER_HOST, MASTER_PORT)
WORKER_SOCK = (WORKER_HOST, WORKER_PORT)

TOKEN = os.environ.get("TOKEN", "agA6D11")
EOF = '@%[>!eof!<]%@'
HEADER_SIZE = len(TOKEN) + 1

SCHEDULER_ALGORITHM = SchedulerAlgorithm.LCFS


def send(sock, data):
    sock.sendall((str(data) + EOF).encode())


def send_flag(sock, flag):
    sock.sendall((TOKEN + str(flag)).encode())


def send_data(sock, data, flag):
    send_flag(sock, flag)
    send(sock, data)


def receive_data(conn):
    data = ''
    chunk = True
    while chunk:
        chunk = conn.recv(1024).decode()
        if chunk:
            data += chunk
            if EOF in chunk:
                chunk = None
    return data[:-len(EOF)]


def get_job(deque):
    if SCHEDULER_ALGORITHM == SchedulerAlgorithm.FCFS:
        return deque.popleft()
    else:
        return deque.pop()


def schedule_jobs(jobs, jobs_queue):
    while True:
        time.sleep(2)
        try:
            job_id = get_job(jobs_queue)
            jobs[job_id].start()
        except:
            continue


def start(sock, jobs, jobs_queue, handle_connection):
    scheduler = threading.Thread(target=schedule_jobs, args=(jobs, jobs_queue))
    scheduler.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(sock)
        s.listen(1)
        print('Server is listening on', sock)

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_connection,
                                      args=(conn, addr))
            thread.start()
