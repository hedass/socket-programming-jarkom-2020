import socket
from utils import WORKER_SOCK as SOCK

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(SOCK)
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
