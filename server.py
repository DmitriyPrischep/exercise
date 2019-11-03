import socket
import os
import json
import httpHeandlers as httpParser
import file as fileController
from worker import worker 
from threadPool import ThreadPool
from configParser import get_config_params
import handler

CONFIG = os.environ['CONFIG']  # '/etc/httpd.conf'
cfg = get_config_params(CONFIG)
if not cfg:
	exit('correct config expected')

fileManager = fileController.FileManager()

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 80))

sock.listen(10)

thread_pool = ThreadPool(thread_number = int(cfg['thread_limit']) , target = worker, args = (sock, handler, cfg['document_root'], fileManager))
thread_pool.start()

