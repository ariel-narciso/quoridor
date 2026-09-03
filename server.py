from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
from QuoridorServer import QuoridorServer

class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 8000), RequestHandler, logRequests=False) as server:
	server.register_introspection_functions()
	server.register_instance(QuoridorServer())
	server.serve_forever()