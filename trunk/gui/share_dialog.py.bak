
import gtk
from cacher import Cacher
import pylast

class ShareDialog(gtk.Dialog):
	
	def __init__(self, parent, app, target):
		gtk.Dialog.__init__(self, None, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.CAN_DEFAULT)
		
		self.app = app
		self.target = target
		
		self.setup()
	
	def setup(self):
		
		#declarations
		self.description_label = gtk.Label()
		self.users_entry = gtk.Entry()
		self.message_entry = gtk.Entry()
		self.message_label = gtk.Label()
		
		#self
		self.set_title('Share: ' + self.target.toStr())
		self.set_border_width(10)
		self.vbox.pack_start(self.description_label, False, False)
		self.vbox.pack_start(self.users_entry, False, False, 10)
		self.vbox.pack_start(self.message_label, False, False)
		self.vbox.pack_start(self.message_entry, False, False, 10)
		
		self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.set_default_response(gtk.RESPONSE_OK)
		self.resize(500, 10)
		
		#description_label
		self.description_label.set_text("Enter usernames or emails seperated by commas:")
		self.description_label.set_alignment(0, 0.5)
		self.description_label.show()
		
		#message_label
		self.message_label.set_text('Enter an optional message:')
		self.message_label.set_alignment(0, 0.5)
		self.message_label.show()
		
		#users_entry
		self.users_entry.show()
		
		#message_entry
		self.message_entry.show()
	
	def get_recipients(self):
		
		if self.run() == gtk.RESPONSE_OK:
			out = None
			if len(self.users_entry.get_text()):
				out = (self.users_entry.get_text().split(','), self.message_entry.get_text())
		else:
			out = None
		
		self.destroy()
		return out
