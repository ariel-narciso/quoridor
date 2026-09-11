from sys import argv
from server.rpc_server import start_server

def __main():
  try:
    host, port = argv[1:3]
  except ValueError:
    print('Informe o host e a porta')
    return
  try:
    start_server(host, int(port))
  except KeyboardInterrupt:
    print('\n Servidor encerrado com sucesso')

if __name__ == '__main__':
  __main()
