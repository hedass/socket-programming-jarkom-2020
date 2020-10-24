import os

MASTER_HOST = '127.0.0.1'
WORKER_HOST = '0.0.0.0'
MASTER_PORT = 6000
WORKER_PORT = 7000
MASTER_SOCK = (WORKER_HOST, MASTER_PORT)

TOKEN = os.environ.get("TOKEN", "agA6D11")
EOF   = '@%[>!eof!<]%@'

BUFF_SIZE  = len(TOKEN)+2

UPDATE_STATUS   = "US"
GET_STATUS      = "GS"
REQUEST_CANCEL  = "RC"
GET_AVAIL       = "GA"
EXEC_FLAG       = "EX"


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
