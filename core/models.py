
from xmlrpc.client import Binary
from typing import TypedDict, Required
from enum import Enum

type Point = tuple[int,int]

class WallType(Enum):
  VERTICAL = 'vertical'
  HORIZONTAL = 'horizontal'

class EventType(Enum):
	WAITING = 1
	GAME_START = 2
	WALL_PLACED = 3
	PAWN_MOVED = 4

class GameNews(TypedDict, total=False):
  event_type: Required[int]
  player: int
  position: str
  orientation: str
  message: str
  board: Binary
  next_player: int
  winner: int

class GameState(TypedDict):
  is_my_turn: bool
  events: list[GameNews]
  game_over: bool
