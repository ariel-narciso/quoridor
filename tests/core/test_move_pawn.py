import pytest
from core.game import Game, WallType

class TestMovePawn:
  @pytest.fixture
  def validator(self):
    return Game(['5A', '1E', '5I', '9E'], ['I', '9', 'A', '1'])

  @pytest.fixture
  def pawns_together_scenario(self):
    return Game(['5E', '4E', '5F', '6E'], ['I', '9', 'A', '1'])

  @pytest.fixture
  def pawns_together_with_walls_scenario(self, pawns_together_scenario: Game):
    assert pawns_together_scenario.set_wall('4D', WallType.HORIZONTAL)
    assert pawns_together_scenario.set_wall('4E', WallType.VERTICAL)
    assert pawns_together_scenario.set_wall('5G', WallType.VERTICAL)
    assert pawns_together_scenario.set_wall('7E', WallType.HORIZONTAL)
    return pawns_together_scenario

  @pytest.mark.parametrize('player_id, pos', [
    (1, '4A'), (1, '6A'), (1, '5B'),
    (2, '2E'), (2, '1D'), (2, '1F'),
    (3, '4I'), (3, '6I'), (3, '5H'),
    (4, '8E'), (4, '9D'), (4, '9F'),
  ])
  def test_valid_move_pawn(self, validator: Game, player_id: int, pos: str):
    assert validator.move_pawn(player_id, pos)
    x, y = validator.convert_position(pos)
    assert validator.player_positions[player_id - 1] == (x, y)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '3A'), (2, '1G'), (3, '7I'), (4, '9C'),
  ])
  def test_invalid_move_pawn(self, validator: Game, player_id: int, pos: str):
    x, y = validator.player_positions[player_id - 1]
    with pytest.raises(ValueError):
      validator.move_pawn(player_id, pos)
    assert validator.player_positions[player_id - 1] == (x, y)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '4A'), (2, '1D'), (3, '6I'), (4, '9F'), (2, '1E')
  ])
  def test_invalid_move_pawn_wall(self, walls_scenario: Game, player_id: int, pos: str):
    x, y = walls_scenario.player_positions[player_id - 1]
    with pytest.raises(ValueError):
      walls_scenario.move_pawn(player_id, pos)
    assert walls_scenario.player_positions[player_id - 1] == (x, y)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '4E'), (1, '6E'), (1, '5F'),
    (2, '5E'), (3, '5E'), (4, '5E'),
    (2, '6E'), (4, '4E'),
  ])
  def test_invalid_move_pawn_filled_position(self, pawns_together_scenario: Game, player_id: int, pos: str):
    x, y = pawns_together_scenario.player_positions[player_id - 1]
    with pytest.raises(ValueError):
      pawns_together_scenario.move_pawn(player_id, pos)
    assert pawns_together_scenario.player_positions[player_id - 1] == (x, y)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '3E'), (1, '5G'), (1, '7E'), (3, '5D')
  ])
  def test_valid_move_pawn_double_jump(self, pawns_together_scenario: Game, player_id: int, pos: str):
    assert pawns_together_scenario.move_pawn(player_id, pos)
    x, y = pawns_together_scenario.convert_position(pos)
    assert pawns_together_scenario.player_positions[player_id - 1] == (x, y)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '3E'), (1, '5G'), (1, '7E'), (3, '5D')
  ])
  def test_invalid_move_pawn_double_jump(self, pawns_together_with_walls_scenario: Game, player_id: int, pos: str):
    x, y = pawns_together_with_walls_scenario.player_positions[player_id - 1]
    with pytest.raises(ValueError):
      pawns_together_with_walls_scenario.move_pawn(player_id, pos)
    assert pawns_together_with_walls_scenario.player_positions[player_id - 1] == (x, y)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '4F'), (1, '6D'), (1, '6F'),
  ])
  def test_valid_move_pawn_diagonal(self, pawns_together_with_walls_scenario: Game, player_id: int, pos: str):
    assert pawns_together_with_walls_scenario.move_pawn(player_id, pos)
    x, y = pawns_together_with_walls_scenario.convert_position(pos)
    assert pawns_together_with_walls_scenario.player_positions[player_id - 1] == (x, y)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '4D'), (2, '5D'), (4, '5D'),
  ])
  def test_invalid_move_pawn_diagonal(self, pawns_together_with_walls_scenario: Game, player_id: int, pos: str):
    x, y = pawns_together_with_walls_scenario.player_positions[player_id - 1]
    with pytest.raises(ValueError): 
      pawns_together_with_walls_scenario.move_pawn(player_id, pos)
    assert pawns_together_with_walls_scenario.player_positions[player_id - 1] == (x, y)

  def test_custom_invalid_move_pawn_diagonal(self, pawns_together_with_walls_scenario: Game):
    assert pawns_together_with_walls_scenario.set_wall('6D', WallType.HORIZONTAL)
    x, y = pawns_together_with_walls_scenario.player_positions[0]
    with pytest.raises(ValueError):
      pawns_together_with_walls_scenario.move_pawn(1, '6D')
      pawns_together_with_walls_scenario.move_pawn(1, '6F')
    assert pawns_together_with_walls_scenario.player_positions[0] == (x, y)
