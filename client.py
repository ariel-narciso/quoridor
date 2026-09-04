from xmlrpc.client import ServerProxy, Binary
from typing import cast

def main():
	server = ServerProxy('http://localhost:8000')
	clientId = server.startConnection()
	if clientId == -1:
		return
	while True:
		myTime, data = cast(tuple[bool,Binary], server.getGameState(clientId))
		news = data.data.decode()
		if news:
			print(news)
		if myTime:
			while True:
				res = input('Sua vez de jogar\nDiga a posição da barreira e orientação: ')
				pos, orientation = res.split(' ')
				success = server.putWall(clientId, pos, int(orientation))
				if success:
					break

main()
