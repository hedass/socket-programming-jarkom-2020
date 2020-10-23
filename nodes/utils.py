MASTER_HOST = '127.0.0.1'
WORKER_HOST = '0.0.0.0'
EXECUTOR_PORT   = 9090
STATUS_PORT     = 9091
AVAIL_PORT      = 9092
CANCEL_PORT     = 9093

EXECUTOR_SOCK   = (WORKER_HOST, EXECUTOR_PORT)
STATUS_SOCK     = (WORKER_HOST, STATUS_PORT)
AVAIL_SOCK      = (WORKER_HOST, AVAIL_PORT)
CANCEL_SOCK     = (WORKER_HOST, CANCEL_PORT)

TOKEN = "123"

BUFF_SIZE  = len(TOKEN)+2

UPDATE_STATUS   = "US"
GET_STATUS      = "GS"
REQUEST_CANCEL  = "RC"
GET_AVAIL       = "GA"
EXEC_FLAG       = "EX"

