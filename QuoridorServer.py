from Quoridor.Quoridor import Quoridor

TOTAL_PLAYERS = 2

class QuoridorServer(Quoridor):
	nConnectedClients = 0
	currentClientId = 1

	def __init__(self):
		super().__init__()

	def startConnection(self):
		if self.nConnectedClients < TOTAL_PLAYERS:
			self.nConnectedClients += 1
			return self.nConnectedClients
		return -1