from core.board import (
	MAP_SIZE,
)

from core.models import WallType

class Game:

  def __init__(self, player_positions: list[str], player_targets: list[str]):
    self.v_walls: list[list[bool]] = [[i == 0 for i in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    self.h_walls: list[list[bool]] = [[i == 0 for _ in range(MAP_SIZE)] for i in range(MAP_SIZE)]
    self.positions: list[list[int]] = [[0 for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    self.player_positions: list[tuple[int,int]] = []
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
      self.positions[x][y] = player_id
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
    return True

    #   self.v_walls[x][y] = True

  # IndexError
  
