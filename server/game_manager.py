from core.game import Game
from core.models import WallType, EventType, GameNews, GameState, Binary

PLAYER_POSITIONS = ['5A', '1E', '5I', '9E']
PLAYER_TARGETS = ['I', '9', 'A', '1']

class GameManager(Game):

	def __init__(self, n_players: int = 4):
		self.n_players = n_players
		self.n_connected_clients = 0
		self.current_client_id = 1
		self.news = ['Procurando jogadores ...\n' for _ in range(n_players)]
		self.news[n_players - 1] = ''
		self.events: list[list[GameNews]] = [[] for _ in range(n_players)]
		self.__n_walls = [20 // n_players for _ in range(n_players)]
		self.has_winner = False
		super().__init__(PLAYER_POSITIONS[:n_players], PLAYER_TARGETS[:n_players])

	def broadcast_event(self, data: GameNews):
		for i in range(self.n_players):
			self.events[i].append((data))

	def send_event(self, client_id: int, data: GameNews):
		self.events[client_id - 1].append(data)

	def start_connection(self):
		if self.n_connected_clients >= self.n_players:
			return -1
		self.n_connected_clients += 1
		client_id = self.n_connected_clients
		if self.n_connected_clients == self.n_players:
			self.broadcast_event({
				'event_type': EventType.GAME_START.value,
				'message': 'Todos os jogadores conectados! O jogo começou.',
				'board': Binary(super().__str__().encode()),
				'next_player': 1,
			})
		else:
			self.send_event(client_id, {
				'event_type': EventType.WAITING.value,
				'message': f'Aguardando mais jogadores ({client_id}/{self.n_players}) ...'
			})
		return self.n_connected_clients

	def get_game_state(self, client_id: int) -> GameState:
		client_events = self.events[client_id - 1].copy()
		self.events[client_id - 1].clear()
		return {
			'is_my_turn': (
				self.n_connected_clients == self.n_players and
				self.current_client_id == client_id
			),
			'events': client_events,
			'game_over': self.has_winner
		}

	def get_n_walls(self, client_id: int):
		return self.__n_walls[client_id - 1]

	def put_wall(self, client_id: int, pos: str, orientation: str):
		enum_orientation = WallType.HORIZONTAL
		if orientation == WallType.VERTICAL.value:
			enum_orientation = WallType.VERTICAL
		if self.current_client_id != client_id or self.__n_walls[client_id - 1] == 0:
			return False
		if not self.set_wall(pos, enum_orientation):
			return False
		self.__n_walls[client_id - 1] -= 1
		next_player = client_id % self.n_players + 1
		self.broadcast_event({
			'event_type': EventType.WALL_PLACED.value,
			'player': client_id,
			'position': pos,
			'orientation': orientation,
			'next_player': next_player,
			'board': Binary(super().__str__().encode())
		})
		self.current_client_id = next_player
		return True

	def move_pawn(self, client_id: int, pos: str):
		if (self.current_client_id != client_id):
			return False
		if not self.move_player(client_id, pos):
			return False
		next_player = client_id % self.n_players + 1
		self.has_winner = self.player_targets[client_id - 1] in pos
		event: GameNews = {
			'event_type': EventType.PAWN_MOVED.value,
			'player': client_id,
			'position': pos,
			'next_player': next_player,
			'board': Binary(super().__str__().encode())
		}
		if self.has_winner:
			event['winner'] = client_id
		self.broadcast_event(event)
		self.current_client_id = next_player
		return True
