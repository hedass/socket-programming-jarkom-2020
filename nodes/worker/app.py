import socket
from utils import WORKER_ADDR

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(WORKER_ADDR)
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
