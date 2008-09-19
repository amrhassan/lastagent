
import dbus
import os

class Banshee():
	
	def __init__(self):
		
		self.player = None
		
		self.bus = dbus.SessionBus()
		
		self.isRunning()	#to set self.player
	
	def isRunning(self):
		if os.popen('pidof banshee-1').read().strip():		
			if not self.player:
				self.player = self.bus.get_object("org.bansheeproject.Banshee", "/org/bansheeproject/Banshee/PlayerEngine")
			return True
		else:
			self.player = None
			return False

	def isPlaying(self):
		return self.player.GetCurrentState() == 'playing'
	
	def getArtist(self):
		if self.isRunning() and self.isPlaying():
			return unicode(self.player.GetCurrentTrack()['artist'])
		else:
			return None
	
	def getTitle(self):
		if self.isRunning() and self.isPlaying():
			return unicode(self.player.GetCurrentTrack()['name'])
		else:
			return None
