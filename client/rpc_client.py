from time import sleep
from typing import cast
from xmlrpc.client import ServerProxy, Fault
from core.models import EventType, GameState, WallType

class RPCCLient:

	def __init__(self, host: str = 'localhost', port: int = 8000) -> None:
		uri = f'http://{host}:{port}'
		self.__server = ServerProxy(uri)
		self.client_id = -1
		self.n_walls = 0

	def __connect(self):
		print("Conectando ao Servidor Quoridor ...")
		try:
			self.client_id = cast(int, self.__server.start_connection())
			if self.client_id >= 1:
				print(f'Conectado com sucesso! Você é o jogador {self.client_id}.')
			else:
				print('Servidor cheio! Limite de jogadores atingido.')
			return self.client_id >= 1
		except Exception as err:
			print(f'Erro ao conectar com o servidor: {err}')
			return False

	def __get_game_state(self):
		try:
			return cast(
				GameState, self.__server.get_game_state(self.client_id)
			)
		except Fault as err:
			print(f'Erro no servidor ao buscar estado: {err.faultString}')

	def __get_n_walls(self):
		return cast(int, self.__server.get_n_walls(self.client_id))

	def start(self):
		if not self.__connect():
			return
		self.n_walls = self.__get_n_walls()
		try:
			while True:
				sleep(0.2)
				game_state = self.__get_game_state()
				if not game_state:
					continue
				self.__handle_news(game_state)
				if game_state['game_over']:
					break
				if game_state['is_my_turn']:
					self.__make_play()
		except KeyboardInterrupt:
			print('\nConexão com o servidor encerrada.')

	def display_instruction_play(self):
		print(
			'Tipo da jogada: 1 - Mover peão || 2 - Colocar barreira\n'
			'Tipo da barreira: 1 - Horizontal || 2 - Vertical\n'
			'Formato da posição: {linha}{coluna}\n'
			'Formato da jogada: {tipoJogada} {posicao} {tipoBarreira}.\n'
			'Ex: 2 5C 1 - coloca uma barreira horizontal em 5C'
			'Nota: ({tipoBarreira}) somente necessário se o tipo de '
			'jogada for colocar uma barreira\n\n'
			f'Você tem {self.n_walls} barreiras disponíveis\n'
		)

	def __make_play(self, display_instruction: bool = True):
		if display_instruction:
			self.display_instruction_play()
		play = input('Informe a jogada conforme o formato indicado: ')
		try:
			play_infos = play.split(' ')
			position = play_infos[1].upper()
			if play[0] == '1':
				self.__move_pawn(position)
			else:
				orientation = int(play_infos[2])
				self.__put_wall(position, orientation)
		except (ValueError, IndexError):
			print('Formato de jogada inválido. Tente novamente\n')
			self.__make_play(False)

	def __put_wall(self, pos: str, orientation: int):
		orientation_type = WallType.HORIZONTAL if orientation == 1 else WallType.VERTICAL
		try:
			self.__server.put_wall(self.client_id, pos.upper(), orientation_type.value)
			self.n_walls = self.__get_n_walls()
		except Fault as err:
			message = err.faultString.split(':', 1)[1]
			print(f'Erro ao colocar barreira. {message}\n')
			self.__make_play(False)

	def __move_pawn(self, pos: str):
		try:
			self.__server.move_player(self.client_id, pos)
		except Fault as err:
			message = err.faultString.split(':', 1)[1]
			print(f'Erro ao mover peão. {message}\n')
			self.__make_play(False)

	def __handle_news(self, game_state: GameState):
		news = game_state['events']
		for event in news:
			event_type = event['event_type']
			if 'message' in event:
				print(event['message'])
			if event_type == EventType.WALL_PLACED.value and 'orientation' in event:
				player = event.get('player')
				position = event.get('position')
				orientation = event['orientation']
				print(f'Player {player} colocou uma barreira {orientation} em {position}')
			elif event_type == EventType.PAWN_MOVED.value:
				player = event.get('player')
				position = event.get('position')
				print(f'Player {player} se moveu para {position}')
				if 'winner' in event and event['winner']:
					print(f'O Player {event['winner']} venceu o jogo!')
			if 'board' in event:
				print(event['board'].data.decode())
			if 'next_player' in event and not game_state['game_over']:
				if game_state['is_my_turn']:
					print('É a sua vez de jogar\n')
				else:
					print(f'Aguardando o lance do Player {event['next_player']} ...')
			elif game_state['game_over']:
				print('ACABOU!!\n')
