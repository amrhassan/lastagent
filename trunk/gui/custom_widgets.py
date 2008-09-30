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

class SuperDialog(gtk.Dialog):
	def __init__(self, title = None, parent = None, flags = 0, buttons = None):
		
		gtk.Dialog.__init__(self, title, parent, flags, buttons)
		
		self.waiting_image = gtk.image_new_from_animation(gtk.gdk.PixbufAnimation('gui/images/waiting1.gif'))
		self.action_area.pack_start(self.waiting_image, False, False)
		hbox = gtk.HBox()
		self.action_area.pack_start(hbox, True, True)
		hbox.show()
		self.waiting_image.set_alignment(0, 0.5)
		self.show_waiting(False)
	
	def show_waiting(self, show = True):
		self.waiting_image.show()

	
	def hide_waiting(self):
		self.waiting_image.hide()

class PlaylistCombo(gtk.ComboBox):
	def __init__(self):
		gtk.ComboBox.__init__(self)
		
		self.p_model = gtk.ListStore(str, str)
		name_renderer = gtk.CellRendererText()
		plays_renderer = gtk.CellRendererText()
		
		self.set_model(self.p_model)
		
		self.pack_start(name_renderer, True)
		self.pack_start(plays_renderer, False)
		self.add_attribute(name_renderer, 'text', 0)
		self.add_attribute(plays_renderer, 'text', 1)
		
		self.add_playlist('(None)', None)
		self.set_active(0)
	
	def add_playlist(self, name, size):
		
		if size == None:
			size = ''
		elif size == 0:
			size = '(empty)'
		elif size == 1:
			size = '1 track'
		elif size > 1:
			size = str(size) + ' tracks'
		
		self.p_model.append([name, size])

class StatusBar(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)
		
		sep = gtk.HSeparator()
		self.pack_start(sep, False, False)
		sep.show()
		
		self.hbox = gtk.HBox()
		self.pack_start(self.hbox, False, False)
		self.hbox.set_border_width(3)
		self.hbox.show()
		
		self.icon = gtk.Image()
		self.hbox.pack_start(self.icon, False, False)
		self.icon.show()
		
		self.label = gtk.Label()
		self.hbox.pack_start(self.label, True, True, 5)
		self.label.set_alignment(0, 0.5)
		self.label.show()
		
		self.current_message_id = 0
	
	def set_icon_from_stock(self, stock_id):
		self.icon.set_from_stock(stock_id, gtk.ICON_SIZE_MENU)
	
	def set_default_icon_from_stock(self, stock_id):
		self.default_stock = stock_id
	
	def set_default_status(self, status):
		self.default_status = status
	
	def reset_to_default(self, timer_id):
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
	

class MessageBox(gtk.Dialog):
	def __init__(self, title, message, icon, parent):
		gtk.Dialog.__init__(self, title, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.CAN_DEFAULT)
		
		#declarations
		self.hbox = gtk.HBox()
		self.icon = gtk.Image()
		self.message_label = gtk.Label()
		
		#self
		self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		self.vbox.pack_start(self.hbox, False, False)
		self.resize(400, 100)
		self.connect('response', self._on_response)	
		
		#hbox
		self.hbox.set_border_width(10)
		self.hbox.pack_start(self.icon, False, False)
		self.hbox.pack_start(self.message_label, True, True, 10)
		self.hbox.show()
		
		#message_label
		self.message_label.set_alignment(0, 0.5)
		self.message_label.set_text(message)
		self.message_label.set_line_wrap(True)
		self.message_label.show()
		
		#icon
		self.icon.set_from_stock(icon, gtk.ICON_SIZE_DIALOG)
		self.icon.show()
	
	def _on_response(self, sender, response):
		self.destroy()

class ErrorMessageBox(MessageBox):
	def __init__(self, title, message, parent):
		MessageBox.__init__(self, title, message, gtk.STOCK_DIALOG_ERROR, parent)

class MainButton(gtk.Button):
	def __init__(self):
		gtk.Button.__init__(self)
		self.normal_label = ''
		self.smaller_tooltip = ''
		self.make_normal()
	
	def set_smaller_tooltip(self, tooltip):
		self.smaller_tooltip = tooltip
	
	def set_normal_label(self, label):
		self.normal_label = label
	
	def make_normal(self):
		self.set_size_request(75, -1)
		self.set_property('has-tooltip', False)
		self.set_label(self.normal_label)
		self.set_relief(gtk.RELIEF_NORMAL)
	
	def make_smaller(self):
		self.set_relief(gtk.RELIEF_NONE)
		self.set_label('')
		self.set_tooltip_text(self.smaller_tooltip)
		self.set_size_request(-1, -1)

def get_hboxed(widget, expand = True, fill = True, padding = 0):
	box = gtk.HBox()
	box.pack_start(widget, expand, fill, padding)
	box.show_all()
	
	return box

def get_vboxed(widget, expand = True, fill = True, padding = 0):
	box = gtk.VBox()
	box.pack_start(widget, expand, fill, padding)
	box.show_all()
	
	return box

class InputBox(gtk.Dialog):
	def __init__(self, parent, title = '', message = '', default_input = ''):
		gtk.Dialog.__init__(self, title, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
		
		self.message = message
		self.default_input = default_input
		
		self.setup()
	
	def set_message(self, message):
		self.message = message
		self.message_label.set_message(message)
	
	def setup(self):
		#declarations
		self.message_label = gtk.Label()
		self.input_entry = gtk.Entry()
		self.container = gtk.VBox()
		
		#message_label
		self.message_label.set_text(self.message)
		self.message_label.set_alignment(0, 0.5)
		self.message_label.show()
		
		#input_entry
		self.input_entry.set_text(self.default_input)
		self.input_entry.show()
		
		#self
		self.container.set_border_width(10)
		self.resize(400, 1)
		self.vbox.pack_start(self.container)
		self.container.show()
		self.container.pack_start(self.message_label, False, False)
		self.container.pack_start(self.input_entry, False, False, 10)
		self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.set_default_response(gtk.RESPONSE_OK)
	
	def get_input(self):
		
		response = self.run()
		
		if response == gtk.RESPONSE_OK:
			self.destroy()
			return self.input_entry.get_text()
		else:
			self.destroy()
			return self.default_input
