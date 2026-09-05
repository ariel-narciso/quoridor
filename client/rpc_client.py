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
      if myTime:
        make_play(server, client_id)
  except KeyboardInterrupt:
    print('\n Conexão com o servidor encerrada.')

def make_play(server: ServerProxy, client_id: int):
  while True:
    res = input('Sua vez de jogar\nDiga a posição da barreira e orientação: ')
    pos, orientation = res.split(' ')
    success = server.put_wall(client_id, pos, int(orientation))
    if success:
      break