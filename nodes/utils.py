import os

MASTER_HOST = '127.0.0.1'
WORKER_HOST = '0.0.0.0'
MASTER_PORT = 6000
WORKER_PORT = 7000
MASTER_SOCK = (MASTER_HOST, MASTER_PORT)
WORKER_SOCK = (WORKER_HOST, WORKER_PORT)

TOKEN = os.environ.get("TOKEN", "agA6D11")
EOF   = '@%[>!eof!<]%@'

BUFF_SIZE  = len(TOKEN)+2

UPDATE_STATUS   = "US"
GET_STATUS      = "GS"
REQUEST_CANCEL  = "RC"
GET_AVAIL       = "GA"
EXEC_FLAG       = "EX"

STATUS = [
    'FINISHED',
    'RUNNING',
    'FAILED',
    'CANCELED',
]

AVAILABILITY = [
    'ACTIVE',
    'DEAD',
    'BUSY',
]

LANGUAGE = {
    'python': 1,
    'text/x-java': 2,
}
LANGUAGE_LOOKUP = {v: k for k, v in LANGUAGE.items()}

def send(sock, data):
    sock.sendall((str(data) + EOF).encode())

def send_flag(sock, flag):
    sock.sendall((TOKEN + flag).encode())

def send_data(sock, data, flag):
    send_flag(sock,flag)
    send(sock,data)

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
