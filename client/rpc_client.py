from time import sleep
from typing import cast
from xmlrpc.client import ServerProxy, Binary

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
      myTime, data = cast(
        tuple[bool, Binary], server.get_game_state(client_id)
      )
      news = data.data.decode()
      if news:
        print(news)
        if 'venceu' in news:
          break
      if myTime:
        print('Sua vez de jogar\n')
        make_play(server, client_id)
      sleep(0.2)
      
  except KeyboardInterrupt:
    print('\n Conexão com o servidor encerrada.')

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
  success = server.put_wall(client_id, pos, int(orientation))
  if not success:
    print('\nMovimento inválido\n')
    make_play(server, client_id)

def move_pawn(server: ServerProxy, client_id: int):
  res = input('Informe a posição de destino: ')
  success = server.move_pawn(client_id, res)
  if not success:
    print('\nMovimento inválido\n')
    make_play(server, client_id)
