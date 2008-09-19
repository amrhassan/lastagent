
import gtk
from cacher import Cacher
import pylast
from editable_list import EditableList
from stock_setup import *
from custom_widgets import *


class ShareDialog(SuperDialog):
	
	def __init__(self, parent, app, target):
		SuperDialog.__init__(self, None, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.CAN_DEFAULT)
		
		self.app = app
		self.target = target
		
		self.setup()
		
		user = self.app.current_user
		user.async_call(self.on_getfriends_done, user.getFriends)
		user.start()
		self.show_waiting()
	
	def on_getfriends_done(self, sender, friends):
		for friend in friends:
			self.list.add_completion_string(friend.getName())
		
		to_enable = [self.list, self.message_entry, self.message_label]
		for i in to_enable:
			i.set_sensitive(True)
		
		self.set_response_sensitive(gtk.RESPONSE_OK, True)
		self.set_default_response(gtk.RESPONSE_OK)
		self.list.add_entry.grab_focus()
		self.show_waiting(False)
	
	def setup(self):
		
		#declarations
		self.list = EditableList()
		self.message_entry = gtk.Entry()
		self.message_label = gtk.Label()
		
		#self
		self.set_title('Edit users...')
		self.set_border_width(10)
		self.vbox.pack_start(self.list)
		self.vbox.pack_start(self.message_label, False, False)
		self.vbox.pack_start(self.message_entry, False, False, 10)
		
		self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.set_response_sensitive(gtk.RESPONSE_OK, False)
		self.resize(400, 350)
		
		#message_label
		self.message_label.set_text('Enter an optional message:')
		self.message_label.set_alignment(0, 0.5)
		self.message_label.set_sensitive(False)
		
		#list
		self.list.set_description('Sharing: ' + self.target.toStr())
		self.list.set_items_stock_id(STOCK_USER)
		self.list.set_sensitive(False)
		
		#message_entry
		self.message_entry.show()
		self.message_entry.set_sensitive(False)
		
		self.show_all()
	
	def get_recipients(self):
		
		out = None
		
		if self.run() == gtk.RESPONSE_OK:
			users = self.list.get_list()
			if len(users):
				out = [users, self.message_entry.get_text()]
		
		self.destroy()
		return out
