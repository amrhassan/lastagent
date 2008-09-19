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
import gobject
import sexy
import re

class EditableList(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)
		
		self.filter_add_entry = False
		
		self.setup()
	
	def set_description(self, text):
		self.description_label.set_text(text)
	
	def set_items_stock_id(self, stock_id):
		self.treeview_pixbufrenderer.set_property('stock-id', stock_id)
	
	def _match_func(self, completion, key, iter, column):
		model = completion.get_model()
		text = model.get_value(iter, column)
		
		if text.lower().startswith(key.lower()):
			return True
		return False
	
	def setup(self):
		#declarations
		self.description_label = gtk.Label()
		self.add_entry = sexy.IconEntry()
		self.completion = gtk.EntryCompletion()
		self.completion_model = gtk.ListStore(str)
		self.treeview = gtk.TreeView()
		self.treeview_model = gtk.ListStore(str)
		self.treeview_column = gtk.TreeViewColumn()
		self.treeview_textrenderer = gtk.CellRendererText()
		self.treeview_pixbufrenderer = gtk.CellRendererPixbuf()
		self.treeview_viewport = gtk.Viewport()
		self.treeview_scrolled = gtk.ScrolledWindow()
		self.remove_box = gtk.HBox()
		self.remove_button = gtk.Button()
		self.instruction_label = gtk.Label()
		
		#add_entry
		self.add_entry.set_completion(self.completion)
		self.add_entry.connect('changed', self._on_add_entry_changed)
		self.add_entry.connect('activate', self._on_add_entry_activate)
		self.add_entry.set_icon(1, gtk.image_new_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_MENU))
		self.add_entry.connect('icon-released', self._on_add_icon_clicked)
		self.add_entry.connect('insert-text', self._on_add_entry_insert)
		
		#completion
		self.completion.set_model(self.completion_model)
		self.completion.set_text_column(0)
		self.completion.set_inline_completion(True)
		##self.completion.set_popup_completion(False)
		self.completion.set_match_func(self._match_func, 0)
		
		#self
		self.pack_start(self.description_label, False, False)
		self.pack_start(self.add_entry, False, False, 3)
		self.pack_start(self.treeview_scrolled, True, True, 5)
		self.pack_start(self.remove_box, False, False, 2)
		
		#treeview_viewport
		self.treeview_viewport.add(self.treeview)
		
		#treeview_scrolled
		self.treeview_scrolled.add(self.treeview_viewport)
		self.treeview_scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		#description_label
		self.description_label.set_alignment(0, 0.5)
		self.description_label.set_line_wrap(True)
		
		#treeview
		self.treeview.set_model(self.treeview_model)
		self.treeview.append_column(self.treeview_column)
		self.treeview.set_headers_visible(False)
		
		#treeview_column
		self.treeview_column.pack_start(self.treeview_pixbufrenderer, False)
		self.treeview_column.pack_start(self.treeview_textrenderer)
		self.treeview_column.add_attribute(self.treeview_textrenderer, 'text', 0)
		
		#remove_box
		self.remove_box.pack_end(self.remove_button, False, False)
		
		#remove_button
		self.remove_button.set_image(gtk.image_new_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU))
		self.remove_button.set_label('_Remove Selected')
		self.remove_button.connect('clicked', self._on_remove_button_clicked)
		
		self.show_all()
	
	def _on_add_entry_insert(self, entry, new, new_text_length, position):
		
		if not self.filter_add_entry:
			return
		
		accept = False
		
		if re.match(self.entry_char_pattern, new):
			accept = True
		
		if new in self.entry_char_list:
			accept = True
		
		if not accept:
			entry.stop_emission('insert-text')
	
	def set_entry_max_length(self, max_length):
		self.add_entry.set_max_length(max_length)
	
	def set_entry_allowed_chars(self, pattern, extra_list):
		self.entry_char_pattern = pattern
		self.entry_char_list = extra_list
		
		self.filter_add_entry = True

	def add_completion_string(self, string):
		self.completion_model.append((string,))	

	def add_completion_strings(self, *strings):
		for string in strings:
			self.add_completion_string(string)
	
	def add_list_string(self, string):
		if len(string.strip()):
			self.treeview_model.append((string,))
	
	def _on_add_entry_changed(self, entry):
		text = entry.get_text()
		
		i = text.rfind(',')
		if i >= 0:
			addition = text[0:i].strip()
			self.add_list_string(addition)
			text = text[i+1:]
			entry.set_text(text)
	
	def _on_add_entry_activate(self, entry):
		entry.set_text(entry.get_text() + ',')
	
	def _on_add_icon_clicked(self, sender, x, y):
		self.add_entry.activate()
	
	def _on_remove_button_clicked(self, button):
		selected_path = self.treeview.get_cursor()[0]
		
		if selected_path:
			iter = self.treeview_model.get_iter(selected_path)
			self.treeview_model.remove(iter)
	
	def get_list(self):
		
		iter = self.treeview_model.get_iter_first()
		
		list = []
		while iter:
			list.append(self.treeview_model.get_value(iter, 0))
			iter = self.treeview_model.iter_next(iter)
		
		return list

"""
e = EditableList('enter your stuff:')

e.add_completion_strings('amr', 'hassan', 'omnia', 'mama')

w = gtk.Window()
w.set_border_width(10)
w.add(e)

e.show()
w.show()

gtk.main()

"""
