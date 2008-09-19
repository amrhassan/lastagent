
import gtk
import pylast
from stock_setup import *
from custom_widgets import *

class AddDialog(SuperDialog):
	
	def __init__(self, parent, app, target):
		SuperDialog.__init__(self, None, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.CAN_DEFAULT)
		
		self.app = app
		self.target = target
		
		self.setup()
		
		user = self.app.current_user
		user.async_call(self.on_getplaylists_done, user.getPlaylistIDs)
		user.start()
		self.show_waiting()

	
	def setup(self):
		
		#declarations
		self.description_label = gtk.Label()
		self.playlists_combo = PlaylistCombo()
		self.description_label = gtk.Label()
		
		#description_label
		self.description_label.set_line_wrap(True)
		self.description_label.set_text('Adding: %s' %(self.target.toStr()))
		self.description_label.set_alignment(0, 0.5)
		self.description_label.show()
		
		#playlists_combo
		self.playlists_combo.show()
		self.playlists_combo.connect('changed', self.on_playlists_combo_changed)
		
		#self
		self.set_title('Choose a playlist...')
		self.set_border_width(10)
		self.vbox.pack_start(self.description_label, False, False, 5)
		self.vbox.pack_start(self.playlists_combo, False, False, 5)
		self.playlists_combo.set_sensitive(False)
		self.resize(400, 100)
		self.action_area.show_all()
		self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.set_default_response(gtk.RESPONSE_OK)
		self.set_response_sensitive(gtk.RESPONSE_OK, False)
		
	
	def on_getplaylists_done(self, sender, list):
		for entry in list:
			self.playlists_combo.add_playlist(entry['title'], int(entry['size']))
			
		self.playlists = list
		
		self.show_waiting(False)
		self.playlists_combo.set_sensitive(True)
	
	def get_playlist_id(self):
		
		out = None
		
		if self.run() == gtk.RESPONSE_OK:
			out = self.playlists[self.playlists_combo.get_active() - 1]['id']
		
		self.destroy()
		return out
	
	def on_playlists_combo_changed(self, sender):
		if self.playlists_combo.get_active() == 0:
			self.set_response_sensitive(gtk.RESPONSE_OK, False)
		else:
			self.set_response_sensitive(gtk.RESPONSE_OK, True)
			self.set_default_response(gtk.RESPONSE_OK)
