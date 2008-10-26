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
from custom_widgets import *

class EditPresets(gtk.Dialog):
	def __init__(self, parent, app, apply_func, change_preset_func):
		gtk.Dialog.__init__(self, 'Edit Presets', parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.CAN_DEFAULT)
		
		self.app = app
		self.apply_func = apply_func
		self.change_preset = change_preset_func
		self.bool_options = []
		self.int_options = []
		self.setup()
	
	def setup(self):
		#declarations
		self.top_box = gtk.HBox()
		self.top_label = gtk.Label()
		self.top_combo = gtk.combo_box_new_text()
		self.top_add = gtk.Button()
		#self.top_rename = gtk.Button()
		self.top_remove = gtk.Button()
		self.options_container = gtk.VBox()
		
		#self
		self.vbox.pack_start(self.top_box, False, False, 10)
		self.vbox.pack_start(gtk.HSeparator(), False, False)
		self.vbox.pack_start(self.options_container)
		self.options_container.set_border_width(10)
		self.connect('response', self.on_self_response)
		self.register_bool_option('main_show_artist', "Show the track's _Artist name.")
		self.register_bool_option('main_show_title', "Show the track's _Title.")
		self.register_bool_option('main_show_album', "Show the track's A_lbum (if available).")
		self.register_bool_option('main_show_buttons', "Show buttons.")
		self.register_bool_option('main_smaller_buttons', "_Smaller buttons.")
		self.register_bool_option('main_show_art', "Show the album art (if available).")
		self.register_int_option('main_art_dimension', "Size of the album art: ")
		self.register_bool_option('main_resizable', "_Resizable main window (doesn't autoresize).")
		self.register_int_option('main_initial_width', 'Initial window width (if resizable).')
		self.register_bool_option('main_decorated', "Show the window's _borders.")
		self.register_bool_option('main_skip_taskbar', "Skip the _taskbar.")
		self.register_bool_option('main_keep_above', "Keep _above.")
		self.register_bool_option('main_show_statusbar', "Show the stat_us bar.")
		self.register_bool_option('menu_show_track', "Show the track in popup menu (when playing).")
		self.register_int_option('menu_track_art_size', "Size of the album art in popup menu: ")
		
		self.set_border_width(10)
		self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		
		#top_box
		self.top_box.pack_start(self.top_label, False, False)
		self.top_box.pack_start(self.top_combo)
		self.top_box.pack_start(self.top_add, False, False)
		##self.top_box.pack_start(self.top_rename, False, False)
		self.top_box.pack_start(self.top_remove, False, False)
		
		#top_label
		self.top_label.set_text('Preset: ')
		
		#top_combo
		self.top_combo.connect('changed', self.on_combo_change)
		
		#top_rename
		##self.top_rename.set_label('_Rename...')
		##self.top_rename.set_image(gtk.image_new_from_stock(gtk.STOCK_EDIT, gtk.ICON_SIZE_BUTTON))
		##self.top_rename.connect('clicked', self.on_rename_clicked)
		
		#top_remove
		self.top_remove.set_label('_Delete')
		self.top_remove.set_image(gtk.image_new_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_BUTTON))
		self.top_remove.connect('clicked', self.on_remove_clicked)
		
		#top_add
		self.top_add.set_label('_New...')
		self.top_add.set_image(gtk.image_new_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_BUTTON))
		self.top_add.connect('clicked', self.on_add_clicked)
		
		self.load_presets()
		self.show_all()
	
	def register_bool_option(self, name, label):
		option = BoolOption(self.app.presets, self.get_selected_preset, name, label, self.apply_func)
		self.bool_options.append(option)
		self.options_container.pack_start(option, False, False)

	def register_int_option(self, name, label):
		option = IntOption(self.app.presets, self.get_selected_preset, name, label, self.apply_func)
		self.int_options.append(option)
		self.options_container.pack_start(option, False, False)
	
	def load_presets(self):
		#clear the old names if available, first
		self.top_combo.set_model(gtk.ListStore(str))
		
		self.presets = self.app.presets.get('presets', 'general').split(';')
		for preset in self.presets:
			self.top_combo.append_text(preset)
		
		current = self.app.presets.get('current_preset', 'general')
		self.top_combo.set_active(self.presets.index(current))
	
	def load_preset(self, preset_name):
		self.selected_preset = preset_name
		
		#load BoolOptions
		for op in self.bool_options:
			op.reset()
		
		#load IntOptions
		for op in self.int_options:
			op.reset()
	
	def on_combo_change(self, sender):
		new = self.presets[sender.get_active()]
		self.load_preset(new)
		self.change_preset(new)
	
	def get_selected_preset(self):
		return self.selected_preset
	
	def on_self_response(self, sender, response):
		self.destroy()
	
	"""
	def on_rename_clicked(self, sender):
		index = self.top_combo.get_active()
		old_name = self.presets[index]
		
		ib = InputBox(self, 'Rename preset', 'Enter the new name for the preset:', old_name)
		new_name = ib.get_input()
		
		if new_name != old_name:
			self.presets[index] = new_name
			self.app.presets.set('presets', ';'.join(self.presets), 'general')
			if self.app.presets.get('current_preset', 'general') == old_name:
				self.app.presets.set('current_preset', new_name, 'general')
			self.load_presets()
	"""
	
	def on_remove_clicked(self, sender):
		if len(self.presets) == 1:
			ErrorMessageBox('Could not delete preset', "Could not delete this preset, since it's the only one.\nYou have to have at least one.", self).run()
			return
		
		removed = self.get_selected_preset()
		self.presets.remove(removed)
		self.app.presets.set('presets', ';'.join(self.presets), 'general')
		if self.app.presets.get('current_preset', 'general') == removed:
			self.app.presets.set('current_preset', self.presets[0], 'general')
			self.apply_func()
		self.load_presets()

	def on_add_clicked(self, sender):
		new_name = InputBox(self, 'New Preset', 'Please enter the name of the new preset:').get_input()
		
		if new_name.strip() != '':
			if new_name in self.presets:
				ErrorMessageBox('Could not add preset', "Could not add the preset because one already exists with that name.", self).run()
				return
			
			self.presets.append(new_name)
			self.app.presets.set('presets', ';'.join(self.presets), 'general')
			self.load_presets()
	
class BoolOption(gtk.CheckButton):
	def __init__(self, ini, selected_preset_func, name, label, apply_func):
		gtk.CheckButton.__init__(self, label = label)
		
		self.ini = ini
		self.ini_name = name
		self.get_selected_preset = selected_preset_func
		self.apply = apply_func
		self.connect('toggled', self._on_self_toggled)
	
	def _on_self_toggled(self, sender):
		self.ini.set(self.ini_name, self.get_active(), 'preset:' + self.get_selected_preset())
		
		if self.ini.get('current_preset', 'general') == self.get_selected_preset():
			self.apply()
	
	def reset(self):
		self.set_active(self.ini.get_bool(self.ini_name, 'preset:' + self.get_selected_preset()))

class IntOption(gtk.HBox):
	def __init__(self, ini, selected_preset_func, name, label, apply_func):
		gtk.HBox.__init__(self)
		
		self.ini = ini
		self.ini_name = name
		self.get_selected_preset = selected_preset_func
		self.apply = apply_func
		
		self.adj = gtk.Adjustment(0, 0, 999, 1, 10, 10)
		self.spin = gtk.SpinButton(self.adj)
		self.label = gtk.Label(label)
		self.label.set_alignment(0, 0.5)
		self.pack_start(self.label, True, True, 23)
		self.pack_start(self.spin, False, False)
		
		self.adj.connect('value-changed', self._on_value_changed)
	
	def _on_value_changed(self, sender):
		self.ini.set(self.ini_name, int(self.spin.get_value()), 'preset:' + self.get_selected_preset())
		
		if self.ini.get('current_preset', 'general') == self.get_selected_preset():
			self.apply()

	def reset(self):
		self.adj.set_value(self.ini.get_int(self.ini_name, 'preset:' + self.get_selected_preset()))
