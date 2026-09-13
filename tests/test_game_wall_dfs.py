import pytest
from core.game import Game, WallType, Point

class TestGameWallDFS():

	@pytest.mark.parametrize('pos, expected_output', [
		((4, 0), [(5, 0), (4, 1)]),
		((0, 4), [(1, 4), (0, 5)]),
		((3, 7), [(4, 7), (3, 6), (3, 8)]),
		((7, 3), [(6, 3), (8, 3), (7, 4)]),
		((8, 4), [(7, 4), (8, 3)]),
	])
	def test_get_adj_positions(self, walls_scenario: Game, pos: Point, expected_output: list[Point]):
		ret = walls_scenario.get_adj_positions(pos)
		assert set(ret) == set(expected_output)

	@pytest.mark.parametrize('pos, wall_type', [
		('5C', WallType.VERTICAL),
		('3E', WallType.HORIZONTAL),
		('4H', WallType.VERTICAL),
		('8D', WallType.HORIZONTAL),
	])
	def test_invalid_set_wall_dfs(self, walls_scenario: Game, pos: str, wall_type: WallType):
		with pytest.raises(ValueError):
			walls_scenario.set_wall(pos, wall_type)

	@pytest.mark.parametrize('pos, wall_type', [
		('4C', WallType.VERTICAL),
		('3D', WallType.HORIZONTAL),
		('5H', WallType.VERTICAL),
		('8E', WallType.HORIZONTAL),
	])
	def test_valid_set_wall_dfs(self, walls_scenario: Game, pos: str, wall_type: WallType):
		ret = walls_scenario.set_wall(pos, wall_type)
		assert ret