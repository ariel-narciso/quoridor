from server.rpc_server import start_server

if __name__ == '__main__':
  try:
    start_server()
  except KeyboardInterrupt:
    print('\n Servidor encerrado com sucesso')
