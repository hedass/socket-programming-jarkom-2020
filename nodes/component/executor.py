from threading import Thread
import socket
from enum import Enum
import utils

class ExecutorThread(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.code = ""

    def run(self):
        with self.conn:
            while True:
                code = self.conn.recv(1024).decode()
                if not code:
                    break
                self.code += code
            # kalo worker execute kodingan
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s
