import pytest
from core.game import Game, WallType

@pytest.fixture()
def standard_scenario():
	return Game(['5A', '1E', '5I', '9E'], ['I', '9', 'A', '1'])

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

@pytest.fixture
def pawns_together_scenario():
	return Game(['5E', '4E', '5F', '6E'], ['I', '9', 'A', '1'])

@pytest.fixture()
def pawns_together_with_walls_scenario(pawns_together_scenario: Game):
	assert pawns_together_scenario.set_wall('4D', WallType.HORIZONTAL)
	assert pawns_together_scenario.set_wall('4E', WallType.VERTICAL)
	assert pawns_together_scenario.set_wall('5G', WallType.VERTICAL)
	assert pawns_together_scenario.set_wall('7E', WallType.HORIZONTAL)
	return pawns_together_scenario
