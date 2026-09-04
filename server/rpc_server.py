from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
from server.game_manager import GameManager

class RequestHandler(SimpleXMLRPCRequestHandler):
  rpc_paths = ('/RPC2',)

def start_server(host: str = 'localhost', port: int = 8000):
  print(f'Servidor Quoridor rodando em http://{host}:{port}')
  with SimpleXMLRPCServer(
    (host, port), RequestHandler, logRequests=False
  ) as server:
    server.register_introspection_functions()
    game_manager = GameManager()
    server.register_instance(game_manager)
    server.serve_forever()
