from threading import Thread
import socket
from enum import Enum
import utils

class Status(Enum):
    FINISH = 1
    FAILED = 2
    RUNNING = 3
    CANCELED = 4

STATUS_NOW = Status(3)

class StatusThread(Thread):
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.conn.bind(utils.STATUS_SOCK)
            self.conn.listen(1)
            while True:
                c_conn, c_addr = self.conn.accept()
                c_input = c_conn.recv(utils.BUFF_SIZE).decode()

                if c_input[:-2] == utils.TOKEN and c_input[-2:] == utils.GET_STATUS:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect(WORKER_STATUS_SOCK)

                    c_conn.sendall((utils.TOKEN + utils.GET_STATUS + get_status()).encode())

                elif c_input[:-2] == utils.TOKEN and c_addr[1] == utils.UPDATE_STATUS:
                    new_status = c_conn.recv(1).decode()
                    set_status(new_status)

                else:
                    c_conn.sendall("FATAL : Authentication Error".encode())

def set_status(number=1):
    global STATUS_NOW
    STATUS_NOW = Status(number)

def get_status():
    return STATUS_NOW
