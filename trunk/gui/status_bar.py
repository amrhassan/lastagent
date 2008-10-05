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
import threading

class StatusBar(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)
		
		sep = gtk.HSeparator()
		self.pack_start(sep, False, False)
		sep.show()
		
		self.outer_hbox = gtk.HBox()
		self.pack_start(self.outer_hbox, False, False)
		
		self.hbox = gtk.HBox()
		self.outer_hbox.pack_start(self.hbox, True, True, 5)
		self.hbox.set_border_width(3)
		self.hbox.show()
		
		self.icon = gtk.Image()
		self.hbox.pack_start(self.icon, False, False)
		self.icon.show()
		
		self.label = gtk.Label()
		self.hbox.pack_start(self.label, True, True, 5)
		self.label.set_alignment(0, 0.5)
		self.label.show()
		
		self.buttons_hbox = gtk.HBox()
		self.prev_button = gtk.Button()
		self.play_button = gtk.Button()
		self.pause_button = gtk.Button()
		self.next_button = gtk.Button()
		
		self.buttons_hbox.pack_start(self.prev_button, False, False)
		self.buttons_hbox.pack_start(self.play_button, False, False)
		self.buttons_hbox.pack_start(self.pause_button, False, False)
		self.buttons_hbox.pack_start(self.next_button, False, False)
		self.hbox.pack_end(self.buttons_hbox, False, False)
		
		self.play_button.set_image(gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU))
		self.play_button.connect('clicked', self._on_play_clicked)
		self.pause_button.set_image(gtk.image_new_from_stock(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_MENU))
		self.pause_button.connect('clicked', self._on_pause_clicked)
		self.prev_button.set_image(gtk.image_new_from_stock(gtk.STOCK_MEDIA_PREVIOUS, gtk.ICON_SIZE_MENU))
		self.prev_button.connect('clicked', self._on_prev_clicked)
		self.next_button.set_image(gtk.image_new_from_stock(gtk.STOCK_MEDIA_NEXT, gtk.ICON_SIZE_MENU))
		self.next_button.connect('clicked', self._on_next_clicked)
		
		for button in (self.prev_button, self.play_button, self.pause_button, self.next_button):
			button.set_focus_on_click(False)
			button.set_relief(gtk.RELIEF_NONE)
		
		self.current_message_id = 0
		self.player = None
	
	def _on_play_clicked(self, sender):
		self.player.play()
	
	def _on_pause_clicked(self, sender):
		self.player.pause()
	
	def _on_prev_clicked(self, sender):
		self.player.prev()
	
	def _on_next_clicked(self, sender):
		self.player.next()
	
	def set_icon_from_stock(self, stock_id):
		self.icon.set_from_stock(stock_id, gtk.ICON_SIZE_MENU)
	
	def _set_default_icon_from_stock(self, stock_id):
		self.default_stock = stock_id
	
	def _set_default_status(self, status):
		self.default_status = status
	
	def reset_to_default(self, timer_id = None):
		if not timer_id:
			timer_id = self.current_message_id

		if timer_id == self.current_message_id:
			self.set_icon_from_stock(self.default_stock)
			self.set_status(self.default_status)
	
	def set_icon_from_animation(self, pixbufanimation):
		self.icon.set_from_animation(pixbufanimation)
	
	def set_status(self, text, timeout = None):
		self.label.set_text(text)
		
		if timeout:
			#to prevent longer timeouts from overlapping shorter ones.
			self.current_message_id += 1
			timer = threading.Timer(timeout, self.reset_to_default, (self.current_message_id,))
			timer.start()
	
	def set_player(self, player):
		self.player = player
		self._set_default_status("%s (Playing)" %player.getName())
		self._set_default_icon_from_stock(player.getIconStackName())
		self.label.set_sensitive(True)
		self.icon.set_sensitive(True)
		if self.player.hasControls():
			self.buttons_hbox.set_sensitive(True)
		
		self.reset_to_default()
	
	def set_to_not_playing(self):
		
		if not self.player or not self.player.isRunning():
			self.player = None
			self._set_default_icon_from_stock('lastagent-idle-network-icon')
			self.set_icon_from_stock('lastagent-idle-network-icon')
			self.buttons_hbox.set_sensitive(False)
			self._set_default_status('Not Playing')
			self.set_status('Not Playing')
			self.label.set_sensitive(False)
			self.icon.set_sensitive(False)
		else:
			self._set_default_status('%s (Stopped)' %self.player.getName())
		
		self.reset_to_default()
