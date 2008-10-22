# -*- coding: utf-8 -*-
#
# pylast - A Last.fm Music Tracker for Linux.
# Copyright (C) 2008-2009  Amr Hassan
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

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
		if self.app.settings.get_bool('autocomplete_from_friends', 'sharing'):
			user.async_call(user.getFriends, self.on_getfriends_done)
		self.show_waiting()
	
	def on_getfriends_done(self, sender, friends):
		for friend in friends:
			self.list.add_completion_string(friend.getName(), 'Friends')
		
		to_enable = [self.list, self.message_entry, self.message_label]
		for i in to_enable:
			i.set_sensitive(True)
		
		self.set_response_sensitive(gtk.RESPONSE_OK, True)
		self.set_default_response(gtk.RESPONSE_OK)
		self.list.add_entry.grab_focus()
		self.hide_waiting()
	
	def setup(self):
		
		#declarations
		self.list = EditableList()
		self.message_entry = gtk.Entry()
		self.message_label = gtk.Label()
		self.message_box = gtk.VBox()
		
		#self
		self.set_title('Edit users...')
		self.set_border_width(10)
		self.vbox.pack_start(self.list)
		self.vbox.pack_start(self.message_box, False, False, 5)
		
		#message_box
		self.message_box.pack_start(self.message_label, False, False)
		self.message_box.pack_start(self.message_entry, False, False, 2)
		
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
