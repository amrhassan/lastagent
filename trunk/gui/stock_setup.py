import gtk

STOCK_LOVE = 'lastagent-love-icon'
STOCK_SHARE = 'lastagent-share-icon'
STOCK_TAG = 'lastagent-tag-icon'
STOCK_LASTAGENT = 'lastagent-app-icon'
STOCK_NETWORK = 'lastagent-network-icon'
STOCK_IDLE_NETWORK = 'lastagent-idle-network-icon'
STOCK_ARTIST = 'lastagent-artist-icon'
STOCK_ALBUM = 'lastagent-album-icon'
STOCK_USER = 'lastagent-user-icon'
STOCK_PLAYLIST = 'lastagent-playlist-icon'

def get_factory():
	
	icons = [
		(STOCK_LOVE, 'gui/images/love.png'),
		(STOCK_TAG, 'gui/images/tag.png'),
		(STOCK_SHARE, 'gui/images/share.png'),
		(STOCK_LASTAGENT, 'gui/images/app.png'),
		(STOCK_NETWORK, 'gui/images/network.ico'),
		(STOCK_IDLE_NETWORK, 'gui/images/network-idle.png'),
		(STOCK_ALBUM, 'gui/images/album.png'),
		(STOCK_USER, 'gui/images/user.png'),
		(STOCK_ARTIST, 'gui/images/artist.png'),
		(STOCK_PLAYLIST, 'gui/images/playlist.png')
		]
	
	factory = gtk.IconFactory()
	
	for stock_id, file in icons:
		pixbuf = gtk.gdk.pixbuf_new_from_file(file)
		iconset = gtk.IconSet(pixbuf)
		factory.add(stock_id, iconset)
	
	return factory
