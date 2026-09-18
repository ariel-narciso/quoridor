import pytest
from core.game import Game, WallType

class TestMovePawnDoubleJump:

	@pytest.mark.parametrize('player_id, pos', [
		(1, '3E'), (1, '5G'), (1, '7E'), (3, '5D')
	])
	def test_valid_move_double_jump(self, pawns_together_scenario: Game, player_id: int, pos: str):
		assert pawns_together_scenario.move_pawn(player_id, pos)
		x, y = pawns_together_scenario.convert_position(pos)
		assert pawns_together_scenario.player_positions[player_id - 1] == (x, y)

	@pytest.mark.parametrize('player_id, pos', [
		(1, '3E'), (1, '5G'), (1, '7E'), (3, '5D')
	])
	def test_invalid_move_double_jump(self, pawns_together_with_walls_scenario: Game, player_id: int, pos: str):
		x, y = pawns_together_with_walls_scenario.player_positions[player_id - 1]
		with pytest.raises(ValueError):
			pawns_together_with_walls_scenario.move_pawn(player_id, pos)
		assert pawns_together_with_walls_scenario.player_positions[player_id - 1] == (x, y)

	@pytest.mark.parametrize('player_id, pos', [
		(1, '4F'), (1, '6D'), (1, '6F'),
	])
	def test_valid_move_diagonal(self, pawns_together_with_walls_scenario: Game, player_id: int, pos: str):
		assert pawns_together_with_walls_scenario.move_pawn(player_id, pos)
		x, y = pawns_together_with_walls_scenario.convert_position(pos)
		assert pawns_together_with_walls_scenario.player_positions[player_id - 1] == (x, y)

	@pytest.mark.parametrize('player_id, pos', [
		(1, '4D'), (2, '5D'), (4, '5D'),
	])
	def test_invalid_move_diagonal_wall(self, pawns_together_with_walls_scenario: Game, player_id: int, pos: str):
		x, y = pawns_together_with_walls_scenario.player_positions[player_id - 1]
		with pytest.raises(ValueError):
			pawns_together_with_walls_scenario.move_pawn(player_id, pos)
		assert pawns_together_with_walls_scenario.player_positions[player_id - 1] == (x, y)

	def test_invalid_move_diagonal_wall_2(self, pawns_together_with_walls_scenario: Game):
		assert pawns_together_with_walls_scenario.set_wall('6D', WallType.HORIZONTAL)
		x, y = pawns_together_with_walls_scenario.player_positions[0]
		with pytest.raises(ValueError):
			pawns_together_with_walls_scenario.move_pawn(1, '6D')
			pawns_together_with_walls_scenario.move_pawn(1, '6F')
		assert pawns_together_with_walls_scenario.player_positions[0] == (x, y)

	@pytest.mark.parametrize('player_positions, player_id, pos', [
		(['2A', '1A'], 1, '2B'), (['1B', '1A'], 1, '2A'),
		(['2I', '1I'], 1, '1H'), (['1H', '1I'], 1, '2I'),
		(['8A', '9A'], 1, '9B'), (['9B', '9A'], 1, '8A'),
		(['8I', '9I'], 1, '9H'), (['9H', '9I'], 1, '8I'),
	])
	def test_valid_move_diagonal_borders(self, player_positions: list[str], player_id: int, pos: str):
		game = Game(player_positions, [])
		assert game.move_pawn(player_id, pos)
		x, y = game.convert_position(pos)
		assert game.player_positions[player_id - 1] == (x, y)

	@pytest.mark.parametrize('player_positions, player_id, pos', [
		(['1C', '1B', '1A'], 1, '2B'), (['3A', '2A', '1A'], 1, '2B'),
		(['1G', '1H', '1I'], 1, '2H'), (['3I', '2I', '1I'], 1, '2H'),
		(['9C', '9B', '9A'], 1, '8B'), (['7A', '8A', '9A'], 1, '8B'),
		(['9G', '9H', '9I'], 1, '8H'), (['7I', '8I', '9I'], 1, '8H'),
	])
	def test_valid_move_diagonal_by_filled_position(self, player_positions: list[str], player_id: int, pos: str):
		game = Game(player_positions, [])
		assert game.move_pawn(player_id, pos)
		x, y = game.convert_position(pos)
		assert game.player_positions[player_id - 1] == (x, y)
