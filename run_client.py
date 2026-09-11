from sys import argv
from client.rpc_client import start_client

def __main():
    try:
      host, port = argv[1:3]
    except ValueError:
      print('Informe o host e a porta')
      return
    start_client(host, int(port))

if __name__ == '__main__':
   __main()