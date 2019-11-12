from handler import handler

def worker(socket, moduleHandler, rootDir, fileManager):
	socket.listen(4) 
	while True: 
		conn, addr = socket.accept() 
		moduleHandler.handler(conn, rootDir, addr[0], fileManager)