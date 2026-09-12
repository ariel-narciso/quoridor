import pytest
from core.game import Game
from core.models import WallType

class TestGameWall:

  @pytest.fixture
  def validator(self):
    return Game([], [])

  @pytest.mark.parametrize('pos, wall_type', [
    ('1C', WallType.HORIZONTAL),
    ('2A', WallType.VERTICAL),
    ('4I', WallType.HORIZONTAL),
    ('9F', WallType.VERTICAL),
  ])
  def test_invalid_set_wall(self, validator: Game, pos: str, wall_type: WallType):
    with pytest.raises(ValueError):
      validator.set_wall(pos, wall_type)

  @pytest.mark.parametrize('pos, wall_type', [
    ('2A', WallType.HORIZONTAL),
    ('1C', WallType.VERTICAL),
    ('3H', WallType.HORIZONTAL),
    ('8D', WallType.VERTICAL),
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

  def test_valid_set_wall_dfs(self):
    pass