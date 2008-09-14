
import amarok
import banshee

def getRunning():
	"""Returns an instance of Player or None."""
	
	available_players = (amarok.Amarok(), banshee.Banshee())
	
	for player in available_players:
		if player.isRunning() and player.isPlaying():
			return player
	
	return None
