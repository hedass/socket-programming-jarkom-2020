import socket
import threading
import utils
from worker import code_runner
from uuid import uuid4
import multiprocessing


STATUS = utils.JobStatus.FINISHED
AVAILABLE = utils.WorkerStatus.ACTIVE

DICT_JOB = multiprocessing.Manager().dict()
DICT_OUTPUT = multiprocessing.Manager().dict()

def do_it(job_uuid, code):
    global STATUS, AVAILABLE
    output = code_runner.run(
                code[1:].encode(),
                utils.LanguageCode.list()[int(code[0]) - 1])
    DICT_OUTPUT[job_uuid] = output
    print(DICT_OUTPUT)
    del DICT_JOB[job_uuid]
    STATUS = utils.JobStatus.FINISHED
    AVAILABLE = utils.WorkerStatus.ACTIVE

def handle_client(conn, addr):
    global STATUS, AVAILABLE, DICT_JOB, DICT_OUTPUT
    print('Connected by', addr)

    header = conn.recv(utils.HEADER_SIZE).decode()

    if header:
        token = header[:-1]
        flag = utils.Request(int(header[-1:]))

        if token != utils.TOKEN:
            utils.send(conn, "FATAL: Authentication Error")

        elif flag == utils.Request.GET_JOB_STATUS:
            utils.send(conn, STATUS.value)

        elif flag == utils.Request.GET_WORKER_STATUS:
            utils.send(conn, AVAILABLE.value)

        elif flag == utils.Request.EXECUTE_JOB:
            if (AVAILABLE != utils.WorkerStatus.ACTIVE):
                utils.send(conn, AVAILABLE.value)
                conn.close()
                print('Disconnected from', addr)
                return

            job_uuid = str(uuid4())
            code = utils.receive_data(conn)
            STATUS = utils.JobStatus.RUNNING
            AVAILABLE = utils.WorkerStatus.BUSY
            process = multiprocessing.Process(target=do_it, args=(job_uuid, code))
            DICT_JOB[job_uuid] = process
            process.start()
            utils.send(conn, job_uuid)

        elif flag == utils.Request.CANCEL_JOB:
            job_id = utils.receive_data(conn)
            if (DICT_JOB.get(job_id) != None):
                DICT_JOB[job_id].kill()
                del DICT_JOB[job_id]
                utils.send(conn, 0)
            utils.send(conn, -1)


        elif flag == utils.Request.GET_OUTPUT:
            job_id = utils.receive_data(conn)
            print(job_id)
            print(DICT_OUTPUT)
            if (DICT_JOB.get(job_id) == None):
                utils.send(conn, -1)
                conn.close()
                print('Disconnected from', addr)
                return

            output = DICT_OUTPUT[job_id]
            utils.send(conn, output)
            del DICT_OUTPUT[job_id]

    conn.close()
    print('Disconnected from', addr)


def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(utils.WORKER_SOCK)
        s.listen(1)
        print('Server is listening on', utils.WORKER_SOCK)

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


start()
