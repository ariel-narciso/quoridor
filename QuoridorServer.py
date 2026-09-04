from Quoridor.Quoridor import Quoridor
from Quoridor.constants import Wall
from xmlrpc.client import Binary

TOTAL_PLAYERS = 4

class QuoridorServer(Quoridor):
	nConnectedClients = 0
	currentClientId = 1
	news = ['Procurando jogadores ...\n' for _ in range(TOTAL_PLAYERS)]
	__nWalls = [20 // TOTAL_PLAYERS for _ in range(TOTAL_PLAYERS)]

	def __init__(self):
		super().__init__(['5A', '1E', '5I', '9E'], ['I', '9', 'A', '1'])
		self.news[TOTAL_PLAYERS - 1] = ''

	def startConnection(self):
		if self.nConnectedClients < TOTAL_PLAYERS:
			self.nConnectedClients += 1
			if self.nConnectedClients == TOTAL_PLAYERS:
				for i in range(TOTAL_PLAYERS):
					self.news[i] += f'Jogadores conectados\n{super().__str__()}'
					if i > 0:
						self.news[i] += 'Aguardando lance do Player 1\n'
			return self.nConnectedClients
		return -1

	def getGameState(self, clientId: int) -> tuple[bool,Binary]:
		news = self.news[clientId - 1]
		self.news[clientId - 1] = ''
		if self.nConnectedClients < TOTAL_PLAYERS:
			return (False, Binary(news.encode()))
		return (self.currentClientId == clientId, Binary(news.encode()))

	def getNWalls(self, clientId: int):
		return self.__nWalls[clientId - 1]

	def putWall(self, clientId: int, pos: str, orientation: int):
		if self.currentClientId != clientId or self.__nWalls[clientId -1] == 0:
			return False
		if not self.setBorder(pos, Wall.vertical if orientation == 1 else Wall.horizontal):
			return False
		self.__nWalls[clientId - 1] -= 1
		nextPlayer = clientId % TOTAL_PLAYERS + 1
		for i in range(TOTAL_PLAYERS):
			self.news[i] = (
				f'Player {clientId} colocou uma barreira em {pos}\n'
				f'{super().__str__()}'
			)
			if i != nextPlayer - 1:
				self.news[i] += f'Aguardando lance do Player {nextPlayer}\n'
		self.currentClientId = nextPlayer
		return True

	# def movePawn(self, clientId: int);
	# 	if self.__isWinner():
	# 				mess = f'Jogador {clientId} venceu o jogo!'
	# 			else:
	# 				mess = f'Vez do jogador {nextClient}'
	# 			for i in range(TOTAL_PLAYERS):
	# 				self.news[i] = (
	# 					f'Jogador {clientId} colocou uma barreira em {pos}' +
	# 					f'\n{self.__str__()}\n{mess}'
	# 				)
	# 			if self.__isWinner():
	# 				self.news[clientId] = self.news[nextClient] = ''

	def __isWinner(self):
		return False
