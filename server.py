import socket
import os
import json
import httpHeandlers as httpParser
import file as fileController
from worker import worker 
from threadPool import ThreadPool
# from configParser import get_config_params
import handler
import config
import multiprocessing as mp


def createSocket(ip, port, max_connections):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(max_connections)

    return server



def cpusFork():
    server = createSocket('', 80, 64)
    fileManager = fileController.FileManager()
    procs = list()
    for cpu in range(4):
        d = dict(server=server, fileManager=fileManager)
        p = mp.Process(target=main, kwargs=d)
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
        print('joined')

def main(server,fileManager):
    thread_pool = ThreadPool(thread_number = 2 , target = worker, args = (server, handler, '/var/www/html', fileManager))
    thread_pool.start()
    
cpusFork()