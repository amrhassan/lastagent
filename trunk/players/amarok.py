
import pydcop

import player

class Amarok(player.Player):
	
	def __init__(self):
		self.amarok = pydcop.DCOPApplication('amarok')
	
	def isRunning(self):
		return "amarok" in pydcop.apps()

	def isPlaying(self):
		return self.amarok.player.isPlaying()
	
	def getArtist(self):
		if self.isRunning() and self.isPlaying():
			return self.amarok.player.artist()
		else:
			return None
	
	def getTitle(self):
		if self.isRunning() and self.isPlaying():
			return self.amarok.player.title()
		else:
			return None
