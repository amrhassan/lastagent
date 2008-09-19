
import amarok
import banshee
import audacious

def getRunning():
	"""Returns an instance of Player or None."""
	
	available_players = (
	amarok.Amarok(),
	banshee.Banshee(),
	audacious.Audacious()
	)
	
	for player in available_players:
		if player.isRunning() and player.isPlaying():
			return player
	
	return None
