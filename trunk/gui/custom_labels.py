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
import webbrowser
import pango
from stock_setup import *

class LinkLabel(gtk.EventBox):
	def __init__(self):
		gtk.EventBox.__init__(self)
		
		self.label = gtk.Label()
		self.add(self.label)
		self.label.show()
		self.text = ''
		
		self.love_action = None
		self.tag_action = None
		self.share_action = None
		self.add_action = None
		
		self.open_url_action = gtk.Action('open-url', 'Go to _Last.fm page', '', STOCK_NETWORK)
		
		self.connect('button-release-event', self.on_clicked)
		self.connect('enter-notify-event', self.on_mouse_enter)
		self.connect('leave-notify-event', self.on_mouse_leave)
		self.open_url_action.connect('activate', self._on_open_url_action_activate)
	
	def _on_open_url_action_activate(self, sender):
		self.open_url()
	
	def set_alignment(self, xalign, yalign):
		self.label.set_alignment(xalign, yalign)
	
	def reset_text(self):
		self._set_markup(self.text)
	
	def enable_underline(self):
		self._set_markup('<u>' + self.text + '</u>')
	
	def enable_bold(self):
		self._set_markup('<b>' + self.text + '</b>')
	
	def enable_big(self):
		self._set_markup('<big>' + self.text + '</big>')
	
	def set_text(self, text):
		self.text = text
		self._set_markup(text)
		self.set_tooltip_text(self.label.get_text() + ' (right click for options)')
	
	def _set_markup(self, markup):
		markup = markup.replace('&', '&amp;')
		self.label.set_markup(markup)
	
	def set_url(self, url):
		self.url = url
		
		self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))

	def open_url(self):
		webbrowser.open(self.url)
	
	def on_clicked(self, sender, event):
		if event.button == 1:
			self.open_url()
		elif event.button == 3:
			self._create_menu().popup(None, None, None, event.button, event.get_time())
	
	def on_mouse_enter(self, sender, event):
		self.enable_underline()
	
	def on_mouse_leave(self, sender, event):
		self.reset_text()
	
	def set_love_action(self, action):
		self.love_action = action
	
	def set_tag_action(self, action):
		self.tag_action = action
	
	def set_add_action(self, action):
		self.add_action = action
	
	def set_share_action(self, action):
		self.share_action = action
	
	def _create_menu(self):
		menu = gtk.Menu()
		
		more_than_web = False
		
		if self.love_action:
			menu.append(self.love_action.create_menu_item())
			more_than_web = True
		if self.tag_action:
			menu.append(self.tag_action.create_menu_item())
			more_than_web = True
		if self.add_action:
			menu.append(self.add_action.create_menu_item())
			more_than_web = True
		if self.share_action:
			menu.append(self.share_action.create_menu_item())
			more_than_web = True
		
		if more_than_web:
			menu.append(gtk.SeparatorMenuItem())
		
		menu.append(self.open_url_action.create_menu_item())
		
		menu.show_all()
		
		return menu

class AlbumLabel(LinkLabel):
	def __init__(self):
		LinkLabel.__init__(self)
	
	def set_album(self, album):
		self.set_text(album.getTitle())
		self.set_url(album.getURL())
		
		#self.label.set_ellipsize(pango.ELLIPSIZE_END)

class TitleLabel(LinkLabel):
	def __init__(self):
		LinkLabel.__init__(self)
	
	def set_track(self, track):
		self.set_text('<b><big>' + track.getTitle() + '</big></b>')
		self.set_url(track.getURL())

class ArtistLabel(LinkLabel):
	def __init__(self):
		LinkLabel.__init__(self)
	
	def set_artist(self, artist):
		self.set_text('<b>' + artist.toStr() + '</b>')
		self.set_url(artist.getURL())
