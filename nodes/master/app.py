import socket
from utils import WORKER_SOCK as SOCK

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(SOCK)
    print('Connected to', SOCK)
