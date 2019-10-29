﻿import socket
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
with open('config.json', encoding = 'utf-8-sig') as config_file:
    conf = json.load(config_file)
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 80))

sock.listen(conf['listeners'])

thread_pool = ThreadPool(thread_number = int(cfg['thread_limit']) , target = worker, args = (sock, handler, cfg['document_root'], fileManager))
thread_pool.start()
