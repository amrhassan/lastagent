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
import pylast
from stock_setup import *
from custom_widgets import *
from custom_labels import *

class AddDialog(SuperDialog):
	
	def __init__(self, parent, app, target):
		SuperDialog.__init__(self, None, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.CAN_DEFAULT)
		
		self.app = app
		self.target = target
		
		self.setup()
		
		user = self.app.current_user
		user.async_call(user.getPlaylists, self.on_getplaylists_done)
		self.show_waiting()

	
	def setup(self):
		
		#declarations
		self.description_label = gtk.Label()
		self.playlists_combo = PlaylistCombo()
		self.description_label = gtk.Label()
		self.edit_button = gtk.Button()
		self.edit_button_box = gtk.HBox()
		
		#description_label
		self.description_label.set_line_wrap(True)
		self.description_label.set_text('Adding: %s' %(self.target.toStr()))
		self.description_label.set_alignment(0, 0.5)
		self.description_label.show()
		
		#playlists_combo
		self.playlists_combo.show()
		self.playlists_combo.connect('changed', self.on_playlists_combo_changed)
		
		#edit_button
		self.edit_button.set_label('Edit your playlists')
		self.edit_button.set_image(gtk.image_new_from_stock(gtk.STOCK_EDIT, gtk.ICON_SIZE_MENU))
		self.edit_button.connect('clicked', self.on_edit_button_clicked)
		self.edit_button.show()
		
		#edit_button_box
		self.edit_button_box.pack_end(self.edit_button, False, False)
		self.edit_button_box.show()
		
		#self
		self.set_title('Choose a playlist...')
		self.set_border_width(10)
		self.vbox.pack_start(self.description_label, False, False, 5)
		self.vbox.pack_start(self.playlists_combo, False, False)
		self.vbox.pack_start(self.edit_button_box, False, False, 5)
		self.playlists_combo.set_sensitive(False)
		self.resize(400, 100)
		self.action_area.show_all()
		self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.set_default_response(gtk.RESPONSE_OK)
		self.set_response_sensitive(gtk.RESPONSE_OK, False)
		
	
	def on_getplaylists_done(self, sender, list):
		for playlist in list:
			self.playlists_combo.add_playlist(playlist.getTitle(), playlist.getSize())
			
		self.playlists = list
		
		self.hide_waiting()
		self.playlists_combo.set_sensitive(True)
		self.playlists_combo.grab_focus()
		if len(list) == 1:
			self.playlists_combo.set_active(1)
	
	def get_playlist(self):
		
		out = None
		
		if self.run() == gtk.RESPONSE_OK:
			out = self.playlists[self.playlists_combo.get_active() - 1]
		
		self.destroy()
		return out
	
	def on_playlists_combo_changed(self, sender):
		if self.playlists_combo.get_active() == 0:
			self.set_response_sensitive(gtk.RESPONSE_OK, False)
		else:
			self.set_response_sensitive(gtk.RESPONSE_OK, True)
			self.set_default_response(gtk.RESPONSE_OK)
	
	def on_edit_button_clicked(self, button):
		import webbrowser
		webbrowser.open(self.app.current_user.getURL() + '/library/playlists')
