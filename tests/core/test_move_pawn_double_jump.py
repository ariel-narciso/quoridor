import pytest
from core.game import Game, WallType

class TestMovePawnDoubleJump:

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
