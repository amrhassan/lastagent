
import pydcop
import os

class Amarok():
	
	def __init__(self):
		self.isRunning()
	
	def isRunning(self):
		if os.popen('pidof amarokapp').read().strip():
			self.amarok = pydcop.DCOPApplication('amarok')
			return True
		else:
			self.amarok = None
			return False

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
