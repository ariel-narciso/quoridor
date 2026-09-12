import pytest
from core.game import Game, Point

class TestGamePosition:

  @pytest.fixture
  def validator(self):
    return Game(['5A', '1E', '5I', '9E'], ['I', '9', 'A', '1'])

  @pytest.mark.parametrize('input, expected_output', [
    ('1A', (0, 0)),
    ('9A', (8, 0)),
    ('1I', (0, 8)),
    ('9I', (8, 8)),
    ('5E', (4, 4)),
  ])
  def test_valid_positions(self, validator: Game, input: str, expected_output: Point):
    ret = validator.convert_position(input)
    assert ret == expected_output

  @pytest.mark.parametrize('input', [('2'), ('8J'), ('0B'), ('4b'), ('44'), ('m2')])
  def test_invalid_positions_raise_error(self, validator: Game, input: str):
    with pytest.raises(ValueError):
      validator.convert_position(input)

  def test_set_player_positions_populates_list(self):
    game = Game([], [])
    assert game.player_positions == []
    game.set_player_positions(['1A', '9I'])
    assert game.player_positions == [(0, 0), (8, 8)]
    assert game.positions[0][0] == 1
    assert game.positions[8][8] == 2
    assert game.positions[4][4] == 0
