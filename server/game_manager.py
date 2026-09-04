from core.game import Game, WallType
from xmlrpc.client import Binary

TOTAL_PLAYERS = 4

class GameManager(Game):

	def __init__(self):
		self.nConnectedClients = 0
		self.currentClientId = 1
		self.news = ['Procurando jogadores ...\n' for _ in range(TOTAL_PLAYERS)]
		self.news[TOTAL_PLAYERS - 1] = ''
		self.__nWalls = [20 // TOTAL_PLAYERS for _ in range(TOTAL_PLAYERS)]
		super().__init__(['5A', '1E', '5I', '9E'], ['I', '9', 'A', '1'])

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
		if not self.setBorder(pos, WallType.VERTICAL if orientation == 1 else WallType.HORIZONTAL):
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

	# def __isWinner(self):
	# 	return False
