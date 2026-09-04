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

	def __init__(self, playerPositions: list[str], playerTargets: list[str]):
		self.map = [list(x) for x in QUORIDOR_MAP.split('\n')]
		self.validPostions = list(range(1, MAP_UPPER_BOUNDARY + 1)) #[1, 2, 3, 4, 5, 6, 7, 8, 9]
		self.playerPositions = playerPositions
		self.playerTargets = playerTargets
		self.visitedCells: list[str] = []
		self.setPlayers()

	def __getCellCoord(self, pos: str):
		x, y = BASE_COORD
		a, b = self.__getIntCoords(pos)
		a -= 1
		b += 1
		return (x + 2 * a, y * b)

	def __getWallCellCoord(self, pos: str):
		x, y = self.__getCellCoord(pos)
		return (x - 1, y - 2)

	def setBorder(self, pos: str, wallOrientation: WallType):
		if not self.__validateSetWall(pos, wallOrientation):
			return False
		x, y = self.__getWallCellCoord(pos)
		if wallOrientation == WallType.HORIZONTAL:
			for i in [1, 2, 3, 5, 6, 7]:
				self.map[x][y + i] = WALL_HORIZONTAL_CHAR
			if not self.__hasWayOut():
				for i in [1, 2, 3, 5, 6, 7]:
					self.map[x][y + i] = ORIGINAL_HORIZONTAL_WALL[i - 1 if i <= 3 else i - 5]
				return False
			return True
		# vertical case
		self.map[x + 1][y] = self.map[x + 3][y] = WALL_VERTICAL_CHAR
		if not self.__hasWayOut():
			self.map[x + 1][y] = self.map[x + 3][y] = ORIGINAL_VERTICAL_WALL
			return False
		return True

	def __validateSetWall(self, pos: str, wallOrientation: WallType):
		x, y = self.__getIntCoords(pos)
		if not x in self.validPostions or not (y + 1) in self.validPostions:
			return False
		x, y = self.__getWallCellCoord(pos)
		if wallOrientation == WallType.HORIZONTAL:
			if self.map[x][y + 1] == WALL_HORIZONTAL_CHAR or self.map[x][y + 5] == WALL_HORIZONTAL_CHAR:
				return False
		# vertical case
		elif self.map[x + 1][y] == WALL_VERTICAL_CHAR or self.map[x + 3][y] == WALL_VERTICAL_CHAR:
			return False
		return True

	def __validateMovePlayer(self, player: int, newPos: str):
		# TODO: verificar colisão; movimento duplo e diagonal
		xDestiny, yDestiny = self.__getIntCoords(newPos) 
		oldPos = self.playerPositions[player - 1]
		x, y = self.__getIntCoords(oldPos)
		if not xDestiny in self.validPostions or not (yDestiny + 1) in self.validPostions:
			return False
		diffX = abs(xDestiny - x)
		diffY = abs(yDestiny - y)
		if diffX > 1 or diffY > 1 or diffX == diffY:
			return False
		return self.__validadeMoveOnWall(oldPos, newPos)

	def __validadeMoveOnWall(self, oldPos: str, newPos: str):
		xDestiny, yDestiny = self.__getIntCoords(newPos)
		x, y = self.__getIntCoords(oldPos)
		if xDestiny > x:
			xBorder, yBorder = self.__getWallCellCoord(newPos)
			return self.map[xBorder][yBorder + 1] != WALL_HORIZONTAL_CHAR
		if xDestiny < x:
			xBorder, yBorder = self.__getWallCellCoord(oldPos)
			return self.map[xBorder][yBorder + 1] != WALL_HORIZONTAL_CHAR
		if yDestiny > y:
			xBorder, yBorder = self.__getWallCellCoord(newPos)
			return self.map[xBorder + 1][yBorder] != WALL_VERTICAL_CHAR
		if yDestiny < y:
			xBorder, yBorder = self.__getWallCellCoord(oldPos)
			return self.map[xBorder + 1][yBorder] != WALL_VERTICAL_CHAR
		return False

	def __getIntCoords(self, pos: str):
		return (int(pos[0]), ord(pos[1].upper()) - ord('A'))

	def __hasWayOut(self):
		for i in range(len(self.playerPositions)):
			self.visitedCells = []
			res = self.__dfs(self.playerPositions[i], self.playerTargets[i])
			if not res:
				return False
		return True

	def __dfs(self, pos: str, finalLine: str):
		# TODO: testar 
		if finalLine in pos:
			return True
		self.visitedCells.append(pos)
		x, y = self.__getIntCoords(pos)
		adjCells: list[str] = []
		if x > 1:
			adjCells.append(f'{x - 1}{pos[1]}')
		if x < MAP_UPPER_BOUNDARY:
			adjCells.append(f'{x + 1}{pos[1]}')
		if y > 0:
			adjCells.append(f'{x}{chr(ord(pos[1]) - 1)}')
		if y < MAP_UPPER_BOUNDARY - 1:
			adjCells.append(f'{x}{chr(ord(pos[1]) + 1)}')
		for cell in adjCells:
			if cell not in self.visitedCells and self.__validadeMoveOnWall(pos, cell):
				ret = self.__dfs(cell, finalLine)
				if ret:
					return True
		return False

	def movePlayer(self, player: int, newPos: str):
		if self.__validateMovePlayer(player, newPos):
			oldPos = self.playerPositions[player - 1]
			x, y = self.__getCellCoord(oldPos)
			self.map[x][y] = ' '
			x, y = self.__getCellCoord(newPos)
			self.map[x][y] = COLOR_PAWNS[player - 1]
			self.playerPositions[player - 1] = newPos
			
	def setPlayers(self):
		for i in range(len(self.playerPositions)):
			pos = self.playerPositions[i]
			x, y = self.__getCellCoord(pos)
			self.map[x][y] = COLOR_PAWNS[i]
			
		# coordP1 = self.__getCellCoord(self.playerPositions[0])
		# coordP2 = self.__getCellCoord(self.playerPositions[1])
		# x, y = coordP1
		# x, y = coordP2
		# self.map[x][y] = COLOR_PAWNS[1]

	def __str__(self) -> str:
		strMap = ''
		for line in self.map:
			strMap += ''.join(line) + '\n'
		return strMap
