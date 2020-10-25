import os
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


MASTER_HOST = '127.0.0.1'
WORKER_HOST = '0.0.0.0'
MASTER_PORT = 6000
WORKER_PORT = 7000
MASTER_SOCK = (MASTER_HOST, MASTER_PORT)
WORKER_SOCK = (WORKER_HOST, WORKER_PORT)

TOKEN = os.environ.get("TOKEN", "agA6D11")
EOF = '@%[>!eof!<]%@'
HEADER_SIZE = len(TOKEN) + 1


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
