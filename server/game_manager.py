from core.game import Game, WallType
from xmlrpc.client import Binary

TOTAL_PLAYERS = 4

class GameManager(Game):

	def __init__(self):
		self.n_connected_clients = 0
		self.current_client_id = 1
		self.news = ['Procurando jogadores ...\n' for _ in range(TOTAL_PLAYERS)]
		self.news[TOTAL_PLAYERS - 1] = ''
		self.__n_walls = [20 // TOTAL_PLAYERS for _ in range(TOTAL_PLAYERS)]
		self.has_winner = False
		super().__init__(['5A', '1E', '5I', '9E'], ['D', '9', 'A', '1'])

	def start_connection(self):
		if self.n_connected_clients < TOTAL_PLAYERS:
			self.n_connected_clients += 1
			if self.n_connected_clients == TOTAL_PLAYERS:
				for i in range(TOTAL_PLAYERS):
					self.news[i] += f'Jogadores conectados\n{super().__str__()}'
					if i > 0:
						self.news[i] += 'Aguardando lance do Player 1\n'
			return self.n_connected_clients
		return -1

	def get_game_state(self, client_id: int) -> tuple[bool,Binary]:
		news = self.news[client_id - 1]
		self.news[client_id - 1] = ''
		if self.n_connected_clients < TOTAL_PLAYERS:
			return (False, Binary(news.encode()))
		return (
			self.current_client_id == client_id and not self.has_winner,
			Binary(news.encode())
		)

	def get_n_walls(self, client_id: int):
		return self.__n_walls[client_id - 1]

	def put_wall(self, client_id: int, pos: str, orientation: int):
		if self.current_client_id != client_id or self.__n_walls[client_id - 1] == 0:
			return False
		if not self.set_wall(pos, WallType.VERTICAL if orientation == 1 else WallType.HORIZONTAL):
			return False
		self.__n_walls[client_id - 1] -= 1
		next_player = client_id % TOTAL_PLAYERS + 1
		for i in range(TOTAL_PLAYERS):
			self.news[i] = (
				f'Player {client_id} colocou uma barreira em {pos}\n'
				f'{super().__str__()}'
			)
			if i != next_player - 1:
				self.news[i] += f'Aguardando lance do Player {next_player}\n'
		self.current_client_id = next_player
		return True

	def move_pawn(self, client_id: int, pos: str):
		pos = pos.upper()
		if (self.current_client_id != client_id):
			return False
		if not self.move_player(client_id, pos):
			return False
		next_player = client_id % TOTAL_PLAYERS + 1
		winner = self.player_targets[client_id - 1] in pos
		for i in range(TOTAL_PLAYERS):
			self.news[i] = (
				f'Player {client_id} se moveu para {pos}\n'
				f'{super().__str__()}'
			)
			if i != next_player - 1 and not winner:
				self.news[i] += f'Aguardando lance do Player {next_player}\n'
		if winner:
			self.has_winner = True
			for i in range(TOTAL_PLAYERS):
				self.news[i] += f'Player {client_id} venceu o jogo!\n'
		self.current_client_id = next_player
		return True

	# def __isWinner(self):
	# 	return False
