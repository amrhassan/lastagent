
import dbus
import os

def shell(command):
	return os.popen(command).read().strip()

class Audacious():
	
	def __init__(self):
		pass
	
	def isRunning(self):
		if shell('pidof audacious'):
			return True
		else:
			return False

	def isPlaying(self):
		return shell('audtool playback-status') == 'playing'
	
	def getArtist(self):
		if self.isRunning() and self.isPlaying():
			return unicode(shell('audtool current-song').split('-')[0].strip())
		else:
			return None
	
	def getTitle(self):
		if self.isRunning() and self.isPlaying():
			return unicode(shell('audtool current-song').split('-')[1].strip())
		else:
			return None
