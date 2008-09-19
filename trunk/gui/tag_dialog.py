
import gtk
from cacher import Cacher
import pylast
from editable_list import EditableList
from stock_setup import *
from custom_widgets import *

class TagDialog(SuperDialog):
	
	def __init__(self, parent, app, target):
		SuperDialog.__init__(self, None, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.CAN_DEFAULT)
		
		self.app = app
		self.target = target
		
		self.setup()
		
		self.target.async_call(self.on_gettoptags_done, self.target.getTopTags)
		self.target.async_call(self.on_gettoptags_done, self.app.current_user.getTopTags)
		self.target.async_call(self.on_gettags_done, self.target.getTags)
		self.target.start()
		self.show_waiting()

	
	def setup(self):
		
		#declarations
		self.description_label = gtk.Label()
		self.tags_entry = gtk.Entry()
		self.list = EditableList()
		
		#self
		self.set_title('Edit Tags...')
		self.set_border_width(10)
		self.vbox.pack_start(self.list, True, True, 5)
		self.resize(400, 300)
		self.action_area.show_all()
		self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.set_default_response(gtk.RESPONSE_OK)
		self.set_response_sensitive(gtk.RESPONSE_OK, False)
		
		
		#list
		self.list.set_description('Tagging: ' + self.target.toStr())
		self.list.set_sensitive(False)
		self.list.set_items_stock_id(STOCK_TAG)
		self.list.set_entry_max_length(256)
		self.list.set_entry_allowed_chars('[a-zA-Z0-9]', (':', '-', ' '))
	
	def on_gettags_done(self, sender, tags):
		
		if sender.last_error():
			self.tags_entry.set_text(sender.last_error().__str__())
			return
		
		for tag in tags:
			self.list.add_list_string(tag.getName())
		
		self.list.set_sensitive(True)
		
		self.set_response_sensitive(gtk.RESPONSE_OK, True)
		self.list.add_entry.grab_focus()
		
		self.show_waiting(False)
	
	def get_tags(self):
		
		out = None
		
		if self.run() == gtk.RESPONSE_OK:
			tags = self.list.get_list()
			tag_names = []
			for tag in tags:
				tag_names.append(tag.strip())
			out = tag_names
		
		self.destroy()
		return out
	
	def on_gettoptags_done(self, sender, output):
		for tag in output:
			self.list.add_completion_string(tag.getName())
