from time import sleep
from typing import cast
from xmlrpc.client import ServerProxy
from core.models import EventType, GameState
from core.constants import WallType

def start_client(host: str = 'localhost', port: int = 8000):
  print('Conectando ao Servidor Quoridor ...')
  server = ServerProxy(f'http://{host}:{port}')
  client_id = cast(int, server.start_connection())
  if client_id == -1:
    print('Servidor cheio! Limite de jogadores atingido.')
    return
  print(f'Conectado com sucesso! Você é o jogador {client_id}.')
  try:
    while True:
      game_state = cast(GameState, server.get_game_state(client_id))
      handle_news(game_state)
      if game_state['game_over']:
        break
      if game_state['is_my_turn']:
        make_play(server, client_id)
      sleep(0.2)
      
  except KeyboardInterrupt:
    print('\n Conexão com o servidor encerrada.')

def handle_news(game_state: GameState):
  news = game_state['events']
  for event in news:
    event_type = event['event_type']
    if 'message' in event:
      print(event['message'])
    if event_type == EventType.WALL_PLACED.value and 'orientation' in event:
      player = event.get('player')
      position = event.get('position')
      orientation = event['orientation']
      print(f'Player {player} colocou uma barreira {orientation} em {position}')
    elif event_type == EventType.PAWN_MOVED.value:
      player = event.get('player')
      position = event.get('position')
      print(f'Player {player} se moveu para {position}')
      if 'winner' in event and event['winner']:
        print(f'O Player {event['winner']} venceu o jogo!')
    if 'board' in event:
      print(event['board'].data.decode())
    if 'next_player' in event and not game_state['game_over']:
      if game_state['is_my_turn']:
        print('É a sua vez de jogar')
      else:
        print(f'Aguardando o lance do Player {event['next_player']} ...')
    elif game_state['game_over']:
      print()

def make_play(server: ServerProxy, client_id: int):
  n_walls = cast(int, server.get_n_walls(client_id))
  if n_walls == 0:
    move_pawn(server, client_id)
  print(
    f'Você tem {n_walls} barreiras disponíveis\n'
    '1. Colocar barreira\n2. Mover peão\n'
  )
  res = input('informe o que deseja fazer (1/2): ')
  if res == '1':
    put_wall(server, client_id)
  else:
    move_pawn(server, client_id)

def put_wall(server: ServerProxy, client_id: int):
  res = input('Diga a posição da barreira e orientação: ')
  pos, orientation = res.split(' ')
  orientation = WallType.HORIZONTAL if orientation == '1' else WallType.VERTICAL
  success = server.put_wall(client_id, pos.upper(), orientation.value)
  if not success:
    print('\nMovimento inválido\n')
    make_play(server, client_id)

def move_pawn(server: ServerProxy, client_id: int):
  res = input('Informe a posição de destino: ')
  success = server.move_pawn(client_id, res.upper())
  if not success:
    print('\nMovimento inválido\n')
    make_play(server, client_id)
