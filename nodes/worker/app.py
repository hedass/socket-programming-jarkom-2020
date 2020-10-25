from json import dumps
import threading
from collections import deque

import utils
from worker import code_runner

# uuid4 is random so should be thread-safe on different keys
jobs = dict()
jobs_output = dict()

# deque is thread-safe
jobs_queue = deque()
IS_RUNNING = False

def run_code(job_id, code):
    global jobs_output, IS_RUNNING
    IS_RUNNING = True
    jobs_output[job_id] = code_runner.run(
        code[1:].encode(),
        utils.LanguageCode.list()[int(code[0]) - 1])
    jobs_output[job_id]['code'] = code[1:]
    jobs_output[job_id]['language'] = int(code[0])
    jobs_output[job_id]['stdout'] = jobs_output[job_id]['stdout'].decode()
    jobs_output[job_id]['stderr'] = jobs_output[job_id]['stderr'].decode()
    jobs_output[job_id] = dumps(jobs_output[job_id])
    IS_RUNNING = False


def handle_connection(conn, addr):
    global jobs, jobs_queue

    print('Connected by', addr)
    header = conn.recv(utils.HEADER_SIZE).decode()

    if header:
        token = header[:-1]
        flag = utils.Request(int(header[-1:]))

        if token != utils.TOKEN:
            utils.send(conn, "FATAL: Authentication Error")

        elif flag == utils.Request.GET_WORKER_STATUS:
            if IS_RUNNING:
                utils.send(conn, utils.WorkerStatus.RUNNING.value)
            else:
                utils.send(conn, utils.WorkerStatus.FREE.value)

        elif flag == utils.Request.EXECUTE_JOB:
            text = utils.receive_data(conn)
            job_id = text[:36]
            code = text[36:]
            thread = threading.Thread(target=run_code, args=(job_id, code))
            jobs[job_id] = thread
            jobs_queue.append(job_id)

        elif flag == utils.Request.GET_OUTPUT:
            job_id = utils.receive_data(conn)
            if (job_id in jobs_output):
                utils.send(conn, jobs_output.get(job_id))
            else:
                utils.send(conn, "RUNNING")

    conn.close()
    print('Disconnected from', addr)


utils.start(utils.WORKER_SOCK, jobs, jobs_queue, handle_connection)
