from sys import argv
from client.rpc_client import RPCCLient

def __main():
		try:
			host, port = argv[1:3]
		except ValueError:
			print('Informe o host e a porta')
			return
		client = RPCCLient(host, int(port))
		client.start()

if __name__ == '__main__':
	 __main()
