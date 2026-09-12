import pytest
from core.game import Game
from core.models import WallType, Point

class TestGameWallDFS():

	@pytest.fixture()
	def validator(self):
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

	@pytest.mark.parametrize('pos, expected_output', [
		((4, 0), [(5, 0), (4, 1)]),
		((0, 4), [(1, 4), (0, 5)]),
		((3, 7), [(4, 7), (3, 6), (3, 8)]),
		((7, 3), [(6, 3), (8, 3), (7, 4)]),
		((8, 4), [(7, 4), (8, 3)]),
	])
	def test_get_adj_positions(self, validator: Game, pos: Point, expected_output: list[Point]):
		ret = validator.get_adj_positions(pos)
		assert set(ret) == set(expected_output)

	@pytest.mark.parametrize('pos, wall_type', [
		('5C', WallType.VERTICAL),
		('3E', WallType.HORIZONTAL),
		('4H', WallType.VERTICAL),
		('8D', WallType.HORIZONTAL),
	])
	def test_invalid_set_wall_dfs(self, validator: Game, pos: str, wall_type: WallType):
		with pytest.raises(ValueError):
			validator.set_wall(pos, wall_type)

	@pytest.mark.parametrize('pos, wall_type', [
		('4C', WallType.VERTICAL),
		('3D', WallType.HORIZONTAL),
		('5H', WallType.VERTICAL),
		('8E', WallType.HORIZONTAL),
	])
	def test_valid_set_wall_dfs(self, validator: Game, pos: str, wall_type: WallType):
		ret = validator.set_wall(pos, wall_type)
		assert ret