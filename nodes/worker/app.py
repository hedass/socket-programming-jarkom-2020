import threading
from collections import deque

import utils
from worker import code_runner

# uuid4 is random so should be thread-safe on different keys
jobs = dict()
jobs_output = dict()

# deque is thread-safe
jobs_queue = deque()


def run_code(job_id, code):
    global jobs_output
    print(code)
    jobs_output[job_id] = code_runner.run(
        code[1:].encode(),
        utils.LanguageCode.list()[int(code[0]) - 1])


def handle_connection(conn, addr):
    global jobs, jobs_queue

    print('Connected by', addr)
    header = conn.recv(utils.HEADER_SIZE).decode()

    if header:
        token = header[:-1]
        flag = utils.Request(int(header[-1:]))

        if token != utils.TOKEN:
            utils.send(conn, "FATAL: Authentication Error")

        elif flag == utils.Request.GET_JOB_STATUS:
            # TODO
            pass

        elif flag == utils.Request.GET_WORKER_STATUS:
            # TODO
            pass

        elif flag == utils.Request.EXECUTE_JOB:
            text = utils.receive_data(conn)
            job_id = text[:36]
            code = text[36:]
            thread = threading.Thread(target=run_code, args=(job_id, code))
            jobs[job_id] = thread
            jobs_queue.append(job_id)

        elif flag == utils.Request.GET_OUTPUT:
            # TODO
            pass

    conn.close()
    print('Disconnected from', addr)


utils.start(utils.WORKER_SOCK, jobs, jobs_queue, handle_connection)
