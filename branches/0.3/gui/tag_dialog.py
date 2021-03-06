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
from safe_threading import *

class TagDialog(SuperDialog):
	
	def __init__(self, parent, app, target):
		SuperDialog.__init__(self, None, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.CAN_DEFAULT)
		
		self.app = app
		self.target = target
		
		self.okays = [False, False, False]	#A weird way to make sure that the next three functions were done.
		
		self.setup()
		
		if self.app.settings.get_bool('autocomplete_from_track_toptags', 'tagging'):
			self.target.async_call(self.target.getTopTags, self.on_gettoptags_done)
		else:
			self.okays[0] = True
		
		if self.app.settings.get_bool('autocomplete_from_user_toptags', 'tagging'):
			self.target.async_call(self.app.current_user.getTopTags, self.on_getfavtags_done)
		else:
			self.okays[1] = True
		
		self.target.async_call(self.target.getTags, self.on_gettags_done)
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
		self.list.set_entry_allowed_chars('[a-zA-Z0-9]', (':', '-', ' ',','))
	
	def on_gettags_done(self, sender, tags):
		
		if sender.last_error():
			return
		
		for tag in tags:
			threads_lock()
			self.list.add_list_string(tag.getName())
			threads_unlock()
		
		self.okays[2] = True
		self._check_okays()
	
	def _check_okays(self):
		for o in self.okays:
			if not o:
				return
		
		threads_lock()
		self.list.set_sensitive(True)
		self.set_response_sensitive(gtk.RESPONSE_OK, True)
		self.list.add_entry.grab_focus()
		self.hide_waiting()
		threads_unlock()
		
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
			threads_lock()
			self.list.add_completion_string(tag.getName(), 'Top Tags')
			threads_unlock()
		
		self.okays[0] = True
		self._check_okays()
	
	def on_getfavtags_done(self, sender, output):
		for tag in output:
			threads_lock()
			self.list.add_completion_string(tag.getName(), 'Your Favorite Tags')
			threads_unlock()
		
		self.okays[1] = True
		self._check_okays()
