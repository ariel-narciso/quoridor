from sys import argv
from client.rpc_client import RPCCLient

def __main():
		try:
			host, port = argv[1:3]
		except ValueError:
			print('Informe o host e a porta')
			return
		port = int(port)
		protocol = 'http'
		if port == 443:
			protocol = 'https'
		client = RPCCLient(protocol, host, port)
		client.start()

if __name__ == '__main__':
	 __main()
