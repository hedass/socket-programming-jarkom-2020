import socket
from utils import WORKER_SOCK as SOCK
from time import sleep
from threading import Thread
from enum import Enum

class State(Enum):
    WAITING = 1
    RUNNING = 2
    FINISHED = 3

class Executor(Thread):
    def __init__(self, conn, addr, callback_function):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.callback_function = callback_function
        self.data = ''
        self.job_id = -1

    def setData(self, data):
        self.data = data

    def setJobId(self, job_id):
        self.job_id = job_id

    def run(self):
        with self.conn:
            print('Connected by', self.addr)
            while 1:
                temp_data = self.conn.recv(1024)
                if not temp_data:
                    print(temp_data)
                    break
                self.data += temp_data.decode()
            print(f'message : {self.data}')
            sleep(5)
            self.conn.sendall(f'diterima {self.data}'.encode())
            self.callback_function()

STATE_NOW = State(1)

def callback_after_executed():
    STATE_NOW = State(1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(SOCK)
    s.listen(1)
    print(f'listening to {SOCK}')
    while True:
        conn, addr = s.accept()
        if (STATE_NOW == State.RUNNING):
            with conn:
                conn.sendall(f'{STATE_NOW.value}'.encode())
                continue
        executor = Executor(conn, addr, callback_after_executed).start()
        STATE_NOW = State(2)
