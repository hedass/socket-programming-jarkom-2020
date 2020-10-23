from threading import Thread
import socket
from enum import Enum
import utils

class CancelThread(Thread):
    def __init__(self, conn, addr, exe_sock):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.exe_sock = exe_sock

    def run(self):
        with self.conn:
            self.conn.bind(utils.CANCEL_SOCK)
            self.conn.listen(1)
            while True:
                c_conn, c_addr = self.conn.accept()
                c_input = c_conn.recv(utils.BUFF_SIZE).decode()

                if c_input[:-2] == utils.TOKEN and c_input[-2:] == utils.REQUEST_CANCEL:
                    self.exe_sock.sendall((utils.TOKEN + utils.REQUEST_CANCEL + "1").encode())
                else:
                    c_conn.sendall("FATAL : Authentication Error".encode())
