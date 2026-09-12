import pytest
from core.game import Game
from core.models import WallType

class TestGameWall:

  @pytest.fixture
  def validator(self):
    game = Game(['5A', '5I'], ['I', 'A'])
    assert game.set_wall('5E', WallType.HORIZONTAL)
    assert game.set_wall('5E', WallType.VERTICAL)
    return game

  @pytest.mark.parametrize('pos, wall_type', [
    ('1C', WallType.HORIZONTAL),
    ('2A', WallType.VERTICAL),
    ('4I', WallType.HORIZONTAL),
    ('9F', WallType.VERTICAL),
    ('5F', WallType.HORIZONTAL),
    ('5D', WallType.HORIZONTAL),
    ('6E', WallType.VERTICAL),
    ('4E', WallType.VERTICAL),
  ])
  def test_invalid_set_wall(self, validator: Game, pos: str, wall_type: WallType):
    with pytest.raises(ValueError):
      validator.set_wall(pos, wall_type)

  @pytest.mark.parametrize('pos, wall_type', [
    ('2A', WallType.HORIZONTAL),
    ('1C', WallType.VERTICAL),
    ('3H', WallType.HORIZONTAL),
    ('8D', WallType.VERTICAL),
    ('5C', WallType.HORIZONTAL),
    ('5G', WallType.HORIZONTAL),
    ('3E', WallType.VERTICAL),
    ('7E', WallType.VERTICAL),
  ])
  def test_valid_set_wall(self, validator: Game, pos: str, wall_type: WallType):
    ret = validator.set_wall(pos, wall_type)
    assert ret
    x, y = validator.convert_position(pos)
    if wall_type == WallType.HORIZONTAL:
      assert validator.h_walls[x][y]
      assert validator.h_walls[x][y + 1]
      assert not validator.v_walls[x][y + 1]
    else:
      assert validator.v_walls[x][y]
      assert validator.v_walls[x + 1][y]
      assert not validator.h_walls[x + 1][y]
