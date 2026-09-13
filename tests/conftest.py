import pytest
from core.game import Game, WallType

# QUORIDOR_MAP = """
#     A   B   C   D   E   F   G   H   I
#   +━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+
# 1 ┃   ┊   ┊   ┊   ┃ ● ┊   ┃   ┊   ┊   ┃
#   + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
# 2 ┃   ┊   ┊   ┊   ┃   ┊   ┃   ┊   ┊   ┃
#   + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
# 3 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
#   + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +━━━+━━━+
# 4 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
#   +━━━+━━━+ ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
# 5 ┃ ● ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊ ● ┃
#   + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +━━━+━━━+
# 6 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
#   +━━━+━━━+ ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
# 7 ┃   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┊   ┃
#   + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
# 8 ┃   ┊   ┊   ┃   ┊   ┃   ┊   ┊   ┊   ┃
#   + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ + ┄ +
# 9 ┃   ┊   ┊   ┃   ┊ ● ┃   ┊   ┊   ┊   ┃
#   +━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+━━━+
# """
@pytest.fixture()
def walls_scenario():
  game = Game(['5A', '1E', '5I', '9E'], ['I', '9', 'A', '1'])
  # Player 1
  assert game.set_wall('5A', WallType.HORIZONTAL)
  assert game.set_wall('7A', WallType.HORIZONTAL)
  # Player 2
  assert game.set_wall('1E', WallType.VERTICAL)
  assert game.set_wall('1G', WallType.VERTICAL)
  # Player 3
  assert game.set_wall('4H', WallType.HORIZONTAL)
  assert game.set_wall('6H', WallType.HORIZONTAL)
  # Player 4
  assert game.set_wall('8D', WallType.VERTICAL)
  assert game.set_wall('8F', WallType.VERTICAL)
  return game
