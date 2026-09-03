from xmlrpc.client import ServerProxy

server = ServerProxy('http://localhost:8000')

clientId = server.startConnection()

