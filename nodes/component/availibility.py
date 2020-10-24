from threading import Thread
import socket
from enum import Enum
import utils


class Avail(Enum):
    ACTIVE = 1
    DEAD = 2
    NOT_AVAIL = 3

AVAIL_NOW = Avail(3)

class AvailThread(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        with self.conn:
            self.conn.bind(utils.AVAIL_SOCK)
            self.conn.listen(1)
            while True:
                c_conn, c_addr = self.conn.accept()
                c_input = c_conn.recv(utils.BUFF_SIZE).decode()

                if c_input[:-2] == utils.TOKEN and c_input[-2:] == utils.GET_AVAIL:
                    c_conn.sendall((utils.TOKEN + utils.GET_AVAIl + get_avail()).encode())
                
                elif c_input[:-2] == utils.TOKEN and c_input[-2:] == utils.UPDATE_AVAIL:
                    new_status = c_conn.recv(1).decode()
                    set_avail(new_status)

                else:
                    c_conn.sendall("FATAL : Authentication Error".encode())

def set_avail(number=1):
    global AVAIL_NOW
    AVAIL_NOW = Avail(number)

def get_avail():
    return AVAIL_NOW
