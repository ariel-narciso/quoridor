from core.board import (
	MAP_SIZE,
	ORIGINAL_HORIZONTAL_WALL,
	ORIGINAL_VERTICAL_WALL,
	WALL_HORIZONTAL_CHAR,
	WALL_VERTICAL_CHAR,
	COLOR_PAWNS
)

from core.models import WallType, Point

class Game:

	def __init__(self, player_positions: list[str], player_targets: list[str]):
		self.v_walls: list[list[bool]] = [[i in [0, MAP_SIZE] for i in range(MAP_SIZE + 1)] for _ in range(MAP_SIZE)]
		self.h_walls: list[list[bool]] = [[i in [0, MAP_SIZE] for _ in range(MAP_SIZE)] for i in range(MAP_SIZE + 1)]
		self.player_positions: list[Point] = []
		self.player_targets: list[str] = player_targets
		self.__visited_positions_dfs: list[Point] = []
		self.set_player_positions(player_positions)

	def convert_position(self, pos: str):
		if len(pos) != 2:
			raise ValueError('Formato de coordenada inválido')
		x, y = [int(pos[0]), ord(pos[1]) - ord('A')]
		if x == 0 or y < 0 or y >= MAP_SIZE:
			raise ValueError('Coordenada fora dos limites do mapa')
		return (x - 1, y)

	def set_player_positions(self, player_positions: list[str]):
		player_id = 1
		for pos in player_positions:
			x, y = self.convert_position(pos)
			self.player_positions.append((x, y))
			player_id += 1

	def set_wall(self, pos: str, wall_type: WallType):
		x, y = self.convert_position(pos)
		if wall_type == WallType.HORIZONTAL:
			if y == 8:
				raise ValueError('Coordenada fora dos limites do mapa')
			if self.h_walls[x][y] or self.h_walls[x][y + 1]:
				raise ValueError('Essa posição já tem uma barreira')
			self.h_walls[x][y] = self.h_walls[x][y + 1] = True
		else:
			if x == 8:
				raise ValueError('Coordenada fora dos limites do mapa')
			if self.v_walls[x][y] or self.v_walls[x + 1][y]:
				raise ValueError('Essa posição já tem uma barreira')
			self.v_walls[x][y] = self.v_walls[x + 1][y] = True
		ok, player_id = self.__has_way_out()
		if not ok:
			if wall_type == WallType.HORIZONTAL:
				self.h_walls[x][y] = self.h_walls[x][y + 1] = False
			else:
				self.v_walls[x][y] = self.v_walls[x + 1][y] = False
			raise ValueError(
				f'Colocar barreira {wall_type.value} em {pos} '
				f'deixa o jogador {player_id + 1} sem saída'
			)
		return True

	def __has_way_out(self):
		for i in range(len(self.player_positions)):
			self.__visited_positions_dfs = []
			x, y = self.player_positions[i]
			ret = self.__dfs((x, y), self.player_targets[i])
			if not ret:
				return (False, i)
		return (True, 0)

	def __dfs(self, pos: Point, target: str):
		x, y = pos
		if target.isdigit() and x + 1 == int(target):
			return True
		elif not target.isdigit() and chr(ord('A') + y) == target:
			return True
		self.__visited_positions_dfs.append((x, y))
		adj_positions = self.get_adj_positions(pos)
		for adj_pos in adj_positions:
			if adj_pos not in self.__visited_positions_dfs:
				ret = self.__dfs(adj_pos, target)
				if ret:
					return True
		return False

	def get_adj_positions(self, pos: Point):
		x, y = pos
		adj_positions: list[Point] = []
		if x > 0 and not self.h_walls[x][y]:
			adj_positions.append((x - 1, y))
		if x < MAP_SIZE - 1 and not self.h_walls[x + 1][y]:
			adj_positions.append((x + 1, y))
		if y > 0 and not self.v_walls[x][y]:
			adj_positions.append((x, y - 1))
		if y < MAP_SIZE - 1 and not self.v_walls[x][y + 1]:
			adj_positions.append((x, y + 1))
		return adj_positions

	def move_pawn(self, player_id: int, pos: str):
		new_x, new_y = self.convert_position(pos)
		current_x, current_y = self.player_positions[player_id - 1]
		if (new_x, new_y) in self.player_positions:
			raise ValueError('A posição de destino deve estar vazia')
		manhatan_distance = abs(new_x - current_x) + abs(new_y - current_y)
		if manhatan_distance == 2:
			return self.__double_jump(player_id, pos)
		if manhatan_distance != 1:
			raise ValueError('Movimento inválido')
		adj_positions = self.get_adj_positions((current_x, current_y))
		if not (new_x, new_y) in adj_positions:
			raise ValueError('O peão não pode pular barreira')
		self.player_positions[player_id - 1] = (new_x, new_y)
		return True

	def __double_jump(self, player_id: int, pos: str):
		new_x, new_y = self.convert_position(pos)
		current_x, current_y = self.player_positions[player_id - 1]
		if abs(new_x - current_x) == 1:
			ok = self.__diagonal_jump(current_x, current_y, new_x, new_y)
		else:
			ok = (
				self.__v_double_jump(current_x, current_y, new_x) or
				self.__h_double_jump(current_x, current_y, new_y)
			)
		if ok:
			self.player_positions[player_id - 1] = (new_x, new_y)
			return True
		raise ValueError('Movimento duplo inválido')

	def __v_double_jump(self, current_x: int, current_y: int, new_x: int):
		if new_x == current_x + 2:
			return (
				(current_x + 1, current_y) in self.player_positions and
				not self.h_walls[current_x + 1][current_y] and
				not self.h_walls[current_x + 2][current_y]
			)
		if new_x == current_x - 2:
			return (
				(current_x - 1, current_y) in self.player_positions and
				(
					not self.h_walls[current_x][current_y] and
					not self.h_walls[current_x - 1][current_y]
				)
			)
		return False

	def __h_double_jump(self, current_x: int, current_y: int, new_y: int):
		if new_y == current_y + 2:
			return (
				(current_x, current_y + 1) in self.player_positions and
				not self.v_walls[current_x][current_y + 1] and
				not self.v_walls[current_x][current_y + 2]
			)
		if new_y == current_y - 2:
			return (
				(current_x, current_y - 1) in self.player_positions and
				not self.v_walls[current_x][current_y] and
				not self.v_walls[current_x][current_y - 1]
			)
		return False

	def __diagonal_jump(self, current_x: int, current_y: int, new_x: int, new_y: int):
		first_top_path, first_bottom_path, first_rigth_path, first_left_path = (
			self._get_diagonal_first_paths(current_x, current_y, new_x, new_y)
		)
		if new_x == current_x + 1:
			if new_y == current_y + 1: # inferior direito
				if first_bottom_path and not self.v_walls[new_x][new_y]:
					return True
				if first_rigth_path and not self.h_walls[new_x][new_y]:
					return True
			else: # inferior esquerdo
				if first_bottom_path and not self.v_walls[new_x][current_y]:
					return True
				if first_left_path and not self.h_walls[new_x][new_y]:
					return True
		else:
			if new_y == current_y + 1: # superior direito
				if first_top_path and not self.v_walls[new_x][new_y]:
					return True
				if first_rigth_path and not self.h_walls[current_x][new_y]:
					return True
			else: # superior esquerdo
				if first_top_path and not self.v_walls[new_x][current_y]:
					return  True
				if first_left_path and not self.h_walls[current_x][new_y]:
					return True
		return False

	def _get_diagonal_first_paths(self, current_x: int, current_y: int, new_x: int, new_y: int):
		return [
			# first_top_path
			(
				not self.h_walls[current_x][current_y] and
				(new_x, current_y) in self.player_positions and
				(
					self.h_walls[new_x][current_y] or
					(new_x - 1, current_y) in self.player_positions
				)
				#TODO Não necessariamente precisa haver uma parede (pode ser um peão na proxima casa)
			),
			# first_bottom_path
			(
				not self.h_walls[new_x][current_y] and
				(new_x, current_y) in self.player_positions and
				(
					self.h_walls[new_x + 1][current_y] or
					(new_x + 1, current_y) in self.player_positions
				)
			),
			# first_rigth_path
			(
				not self.v_walls[current_x][new_y] and
				(current_x, new_y) in self.player_positions and
				(
					self.v_walls[current_x][new_y + 1] or
					(current_x, new_y + 1) in self.player_positions
				)
			),
			# first_left_path
			(
				not self.v_walls[current_x][current_y] and
				(current_x, new_y) in self.player_positions and
				(
					self.v_walls[current_x][new_y] or
					(current_x, new_y - 1) in self.player_positions
				)
			)
		]

	def __str__(self) -> str:
		str_map = '\n    A   B   C   D   E   F   G   H   I\n'
		for i in range(MAP_SIZE):
			line = '  '
			for j in range(MAP_SIZE):
				wall = WALL_HORIZONTAL_CHAR if self.h_walls[i][j] else ORIGINAL_HORIZONTAL_WALL
				line += f'+{wall}'
			str_map += f'{line}+\n'
			line = f'{i + 1} '
			for j in range(MAP_SIZE):
				wall = WALL_VERTICAL_CHAR if self.v_walls[i][j] else ORIGINAL_VERTICAL_WALL
				char = ''
				try:
					idx = self.player_positions.index((i, j))
					char = COLOR_PAWNS[idx]
				except ValueError:
					char = ' '
				line += f'{wall} {char} '
			str_map += f'{line}{WALL_VERTICAL_CHAR}\n'
		str_map += '  +━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+\n'
		return str_map
