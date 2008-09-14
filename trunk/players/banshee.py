
import dbus
import os

class Banshee():
	
	def __init__(self):
		self.bus = dbus.SessionBus()
		
		self.isRunning()	#to set self.banshee
	
	def isRunning(self):
		if os.popen('pidof banshee-1').read().strip():		
			self.banshee = self.bus.get_object("org.bansheeproject.Banshee", "/org/bansheeproject/Banshee/PlayerEngine")
			return True
		else:
			self.banshee = None
			return False

	def isPlaying(self):
		return self.banshee.GetCurrentState() == 'playing'
	
	def getArtist(self):
		if self.isRunning() and self.isPlaying():
			return unicode(self.banshee.GetCurrentTrack()['artist'])
		else:
			return None
	
	def getTitle(self):
		if self.isRunning() and self.isPlaying():
			return unicode(self.banshee.GetCurrentTrack()['name'])
		else:
			return None
