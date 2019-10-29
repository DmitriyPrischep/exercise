import os
from httpTypes import httpTypes
import httpHeandlers as httpParser
import threading

def handler(conn, rootDir, ip, fileManager): 
	lock = threading.RLock()
	resp = httpParser.HTTPResponse()
	if not rootDir:
		rootDir = './'
	while True: 
		# print("while True:")
		req = httpParser.HttpRequest() 
		data = conn.recv(1024) 
		if not data: 
			break

		req.process(data.decode('utf-8'))

		if req.giveError() == 'Unknown method':
			print('--- Unknown method')
			resp.set_status(400, 'Bad Request')
		elif req.giveError() == 'Root directory escape':
			print('--- Root directory escape')
			resp.set_status(403, 'Forbidden')
		elif req.giveMethod() in [ 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE', 'TRACE', 'CONNECT']:
			print('--- Method Not Allowed')
			resp.set_status(405, 'Method Not Allowed')
		else:
			resp.add_header('Server', 'HowleServ')
			fullPath = os.path.join(rootDir, req.path)
			print("fullPath", fullPath, "rootDir: ", rootDir)
			if not os.path.exists(fullPath):
				resp.set_status(404, 'Not Found')
				print("Send 404", fullPath)
				conn.send(resp.generate_response())
				break

			if os.path.isdir(fullPath):
				fullPathIndex = os.path.join(fullPath, 'index.html')
				if os.path.exists(fullPathIndex):
					fullPath = fullPathIndex
					req.fileType = 'html'
				else:
					resp.set_status(403, 'Forbidden')
					print("Sended 403")
					conn.send(resp.generate_response())
					break
			print("Read File")
			with lock:
				body = fileManager.takeFile(fullPath)
			# print("Type of body: ", type(body), body)

			if req.file_type in httpTypes.keys():
				resp.add_header('Content-Type', F'{httpTypes[req.file_type]}')
			else:
				resp.add_header('Content-Type', 'text/plain')

			resp.add_header('Content-Length', len(body))
			if req.giveMethod() == 'GET':
				# print("Get: ", body[:30], len(body))
				resp.add_body(body)
		print("Send Return")
		conn.send(resp.generate_response())
		break

	conn.close()
