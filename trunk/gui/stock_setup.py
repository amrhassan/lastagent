import gtk

STOCK_LOVE = 'lastagent-love-icon'
STOCK_SHARE = 'lastagent-share-icon'
STOCK_TAG = 'lastagent-tag-icon'
STOCK_LASTAGENT = 'lastagent-app-icon'

def get_factory():
	
	icons = [
		(STOCK_LOVE, 'gui/images/love.png'),
		(STOCK_TAG, 'gui/images/tag.png'),
		(STOCK_SHARE, 'gui/images/share.png'),
		(STOCK_LASTAGENT, 'gui/images/app_red.ico')
		]
	
	factory = gtk.IconFactory()
	
	for stock_id, file in icons:
		pixbuf = gtk.gdk.pixbuf_new_from_file(file)
		iconset = gtk.IconSet(pixbuf)
		factory.add(stock_id, iconset)
	
	return factory
