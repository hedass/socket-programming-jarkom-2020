import socket
from utils import WORKER_ADDR

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(WORKER_ADDR)
    print('Connected to', WORKER_ADDR)
