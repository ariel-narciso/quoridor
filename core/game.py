from core.constants import (
	QUORIDOR_MAP,
	MAP_UPPER_BOUNDARY,
	BASE_COORD,
	COLOR_PAWNS,
	WALL_HORIZONTAL_CHAR,
	WALL_VERTICAL_CHAR,
	ORIGINAL_HORIZONTAL_WALL,
	ORIGINAL_VERTICAL_WALL,
	WallType,
)

class Game:

	def __init__(self, player_positions: list[str], player_targets: list[str]):
		self.map = [list(x) for x in QUORIDOR_MAP.split('\n')]
		self.valid_postions = list(range(1, MAP_UPPER_BOUNDARY + 1)) #[1, 2, 3, 4, 5, 6, 7, 8, 9]
		self.player_positions = player_positions
		self.player_targets = player_targets
		self.visited_cells: list[str] = []
		self.set_players()

	def __get_cell_coord(self, pos: str):
		x, y = BASE_COORD
		a, b = self.__get_int_coords(pos)
		a -= 1
		b += 1
		return (x + 2 * a, y * b)

	def __get_wall_cell_coord(self, pos: str):
		x, y = self.__get_cell_coord(pos)
		return (x - 1, y - 2)

	def set_wall(self, pos: str, wall_orientation: WallType):
		pos = pos.upper()
		if not self.__validate_put_wall(pos, wall_orientation):
			return False
		x, y = self.__get_wall_cell_coord(pos)
		if wall_orientation == WallType.HORIZONTAL:
			for i in [1, 2, 3, 5, 6, 7]:
				self.map[x][y + i] = WALL_HORIZONTAL_CHAR
			if not self.__has_way_out():
				for i in [1, 2, 3, 5, 6, 7]:
					self.map[x][y + i] = ORIGINAL_HORIZONTAL_WALL[i - 1 if i <= 3 else i - 5]
				return False
			return True
		# vertical case
		self.map[x + 1][y] = self.map[x + 3][y] = WALL_VERTICAL_CHAR
		if not self.__has_way_out():
			self.map[x + 1][y] = self.map[x + 3][y] = ORIGINAL_VERTICAL_WALL
			return False
		return True

	def __validate_put_wall(self, pos: str, wall_orientation: WallType):
		x, y = self.__get_int_coords(pos)
		if not x in self.valid_postions or not (y + 1) in self.valid_postions:
			return False
		x, y = self.__get_wall_cell_coord(pos)
		if wall_orientation == WallType.HORIZONTAL:
			if self.map[x][y + 1] == WALL_HORIZONTAL_CHAR or self.map[x][y + 5] == WALL_HORIZONTAL_CHAR:
				return False
		# vertical case
		elif self.map[x + 1][y] == WALL_VERTICAL_CHAR or self.map[x + 3][y] == WALL_VERTICAL_CHAR:
			return False
		return True

	def __validate_move_player(self, player: int, new_pos: str):
		# TODO: verificar colisão; movimento duplo e diagonal
		x_destiny, y_destiny = self.__get_int_coords(new_pos) 
		old_pos = self.player_positions[player - 1]
		x, y = self.__get_int_coords(old_pos)
		if not x_destiny in self.valid_postions or not (y_destiny + 1) in self.valid_postions:
			return False
		diff_x = abs(x_destiny - x)
		diff_y = abs(y_destiny - y)
		if diff_x > 1 or diff_y > 1 or diff_x == diff_y:
			return False
		return self.__validade_move_on_wall(old_pos, new_pos)

	def __validade_move_on_wall(self, oldPos: str, newPos: str):
		x_destiny, y_destiny = self.__get_int_coords(newPos)
		x, y = self.__get_int_coords(oldPos)
		if x_destiny > x:
			x_wall, y_wall = self.__get_wall_cell_coord(newPos)
			return self.map[x_wall][y_wall + 1] != WALL_HORIZONTAL_CHAR
		if x_destiny < x:
			x_wall, y_wall = self.__get_wall_cell_coord(oldPos)
			return self.map[x_wall][y_wall + 1] != WALL_HORIZONTAL_CHAR
		if y_destiny > y:
			x_wall, y_wall = self.__get_wall_cell_coord(newPos)
			return self.map[x_wall + 1][y_wall] != WALL_VERTICAL_CHAR
		if y_destiny < y:
			x_wall, y_wall = self.__get_wall_cell_coord(oldPos)
			return self.map[x_wall + 1][y_wall] != WALL_VERTICAL_CHAR
		return False

	def __get_int_coords(self, pos: str):
		return (int(pos[0]), ord(pos[1]) - ord('A'))

	def __has_way_out(self):
		for i in range(len(self.player_positions)):
			self.visited_cells = []
			res = self.__dfs(self.player_positions[i], self.player_targets[i])
			if not res:
				return False
		return True

	def __dfs(self, pos: str, final_line: str):
		# TODO: testar 
		if final_line in pos:
			return True
		self.visited_cells.append(pos)
		x, y = self.__get_int_coords(pos)
		adj_cells: list[str] = []
		if x > 1:
			adj_cells.append(f'{x - 1}{pos[1]}')
		if x < MAP_UPPER_BOUNDARY:
			adj_cells.append(f'{x + 1}{pos[1]}')
		if y > 0:
			adj_cells.append(f'{x}{chr(ord(pos[1]) - 1)}')
		if y < MAP_UPPER_BOUNDARY - 1:
			adj_cells.append(f'{x}{chr(ord(pos[1]) + 1)}')
		for cell in adj_cells:
			if cell not in self.visited_cells and self.__validade_move_on_wall(pos, cell):
				ret = self.__dfs(cell, final_line)
				if ret:
					return True
		return False

	def move_player(self, player: int, new_pos: str):
		new_pos = new_pos.upper()
		if self.__validate_move_player(player, new_pos):
			old_pos = self.player_positions[player - 1]
			x, y = self.__get_cell_coord(old_pos)
			self.map[x][y] = ' '
			x, y = self.__get_cell_coord(new_pos)
			self.map[x][y] = COLOR_PAWNS[player - 1]
			self.player_positions[player - 1] = new_pos
			return True
		return False
			
	def set_players(self):
		for i in range(len(self.player_positions)):
			pos = self.player_positions[i]
			x, y = self.__get_cell_coord(pos)
			self.map[x][y] = COLOR_PAWNS[i]

	def __str__(self) -> str:
		strMap = ''
		for line in self.map:
			strMap += ''.join(line) + '\n'
		return strMap
