from enum import Enum

QUORIDOR_MAP = """
    A   B   C   D   E   F   G   H   I
  +━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+
1 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
  + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
2 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
  + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
3 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
  + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
4 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
  + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
5 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
  + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
6 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
  + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
7 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
  + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
8 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
  + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
9 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
  +━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+
"""

BASE_COORD = (3, 4)

MAP_UPPER_BOUNDARY = 9

COLOR_PAWNS = [
  "\033[91m●\033[0m", # B_VERMELHO
  "\033[92m●\033[0m", # B_VERDE
  "\033[93m●\033[0m", # B_AMARELO
  "\033[94m●\033[0m", # B_AZUL
]

ORIGINAL_HORIZONTAL_WALL = ' ┄ '
ORIGINAL_VERTICAL_WALL = '┊'

class Wall(Enum):
  vertical = 1
  horizontal = 2
  horizontalChar = '━'
  verticalChar = '┃'