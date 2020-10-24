from threading import Thread
import socket
from enum import Enum
import utils

class ExecutorThread(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        with self.conn:
            self.conn.bind(utils.EXECUTOR_SOCK)
            self.conn.listen(1)
            while True:
                c_conn, c_addr = self.conn.accept()
                c_input = c_conn.recv(utils.BUFF_SIZE).decode()

                if c_input[:-2] == utils.TOKEN and c_input[-2:] == utils.EXEC_FLAG:
                    # TODO receive then compile data
                    pass
                elif (c_input[:-2] == utils.TOKEN and c_input[-2:] == utils.REQUEST_CANCEL):
                    cancel_flag = c_conn.recv(1).decode()
                    if(cancel_flag):
                        # TODO abort process
                        pass
                else:
                    c_conn.sendall("FATAL : Authentication Error".encode())
