from typing import cast
from xmlrpc.client import ServerProxy, Binary

def start_client(host: str = 'localhost', port: int = 8000):
  print('Conectando ao Servidor Quoridor ...')
  server = ServerProxy(f'http://{host}:{port}')
  clientId = cast(int, server.startConnection())
  if clientId == -1:
    print('Servidor cheio! Limite de jogadores atingido.')
    return
  print(f'Conectado com sucesso! Você é o jogador {clientId}.')
  try:
    while True:
      myTime, data = cast(
        tuple[bool, Binary], server.getGameState(clientId)
      )
      news = data.data.decode()
      if news:
        print(news)
      if myTime:
        make_play(server, clientId)
  except KeyboardInterrupt:
    print('\n Conexão com o servidor encerrada.')

def make_play(server: ServerProxy, clientId: int):
  while True:
    res = input('Sua vez de jogar\nDiga a posição da barreira e orientação: ')
    pos, orientation = res.split(' ')
    success = server.putWall(clientId, pos, int(orientation))
    if success:
      break