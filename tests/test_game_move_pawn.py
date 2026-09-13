import pytest
from core.game import Game

class TestGameMovePawn:
  @pytest.fixture
  def validator(self):
    return Game(['5A', '1E', '5I', '9E'], ['I', '9', 'A', '1'])

  @pytest.fixture
  def pawns_together_scenario(self):
    return Game(['5E', '4E', '5F', '6E'], ['I', '9', 'A', '1'])

  @pytest.mark.parametrize('player_id, pos', [
    (1, '4A'), (1, '6A'), (1, '5B'),
    (2, '2E'), (2, '1D'), (2, '1F'),
    (3, '4I'), (3, '6I'), (3, '5H'),
    (4, '8E'), (4, '9D'), (4, '9F'),
  ])
  def test_valid_move_pawn(self, validator: Game, player_id: int, pos: str):
    assert validator.move_pawn(player_id, pos)
    assert validator.player_positions[player_id - 1] == validator.convert_position(pos)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '3A'), (2, '1G'), (3, '7I'), (4, '9C'),
  ])
  def test_invalid_move_pawn(self, validator: Game, player_id: int, pos: str):
    with pytest.raises(ValueError):
      validator.move_pawn(player_id, pos)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '4A'), (2, '1D'), (3, '6I'), (4, '9F'), (2, '1E')
  ])
  def test_invalid_move_pawn_wall(self, walls_scenario: Game, player_id: int, pos: str):
    with pytest.raises(ValueError):
      walls_scenario.move_pawn(player_id, pos)

  @pytest.mark.parametrize('player_id, pos', [
    (1, '4E'), (1, '6E'), (1, '5F'),
    (2, '5E'), (3, '5E'), (4, '5E'),
  ])
  def test_invalid_move_pawn_filled_position(self, pawns_together_scenario: Game, player_id: int, pos: str):
    with pytest.raises(ValueError):
      pawns_together_scenario.move_pawn(player_id, pos)
