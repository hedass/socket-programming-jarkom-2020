import socket
import threading
import utils
from component.executor import ExecutorThread
from component.status import Status

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(SOCK)
    print('Connected to', SOCK)
    s.sendall('hello my slave'.encode())
    s.shutdown(socket.SHUT_WR)
    reply = s.recv(1024)
    print(reply.decode())

Status().start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # ngebuka koneksi listen
    while 1:
        conn, addr = s.accept()
        # receive token dan flag
        c_input = conn.recv(utils.BUFF_SIZE)
        if (c_input[:-2] != utils.TOKEN):
            conn.sendall("FATAL : Authentication Error".encode())
            conn.shutdown(socket.SHUT_WR)
            continue

        if (c_input[-2:] == utils.EXEC_FLAG):
            ExecutorThread(conn,addr).start()
        elif (c_input[-2:] == utils.REQUEST_CANCEL):
            while True:
                pass
                cancel_flag = c_conn.recv(1).decode()
                if(cancel_flag):
                    # TODO abort process
                    pass
        else:
            conn.sendall("FATAL : Invalid Flag".encode())
            conn.shutdown(socket.SHUT_WR)

        ExecutorThread(conn, addr).start()
    
    pass
