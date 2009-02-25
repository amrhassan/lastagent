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

def get_default(value_name, section = None):
	values = {
		'current_preset': 'Default',
		'presets': 'Default;Smaller;No Art;Even Smaller;Just Buttons',
		'updating_interval': 1,
		'main_show_album': True,
		'main_keep_above': True,
		'main_opacity': 1.0,
		'main_skip_taskbar': True,
		'main_resizable': True,
		'main_decorated': True,
		'main_show_statusbar': True,
		'main_show_buttons': True,
		'main_show_artist': True,
		'main_show_title': True,
		'main_show_album': True,
		'main_show_art': True,
		'main_show_bio': True,
		'main_initial_width': 550,
		'main_smaller_buttons': False,
		'menu_show_track': True,
		'menu_track_art_size': 40,
		'main_art_dimension': 174,
		'autocomplete_from_track_toptags': True,
		'autocomplete_from_user_toptags': True,
		'autocomplete_from_friends': True,
		'icon_color': 'blue',
		'run_on_session_startup': False,
		'main_bio_use_scrollbars': True,
		'main_bio_use_small_text': True,
	}
	
	section_values = {
		'preset:Smaller':{
			'main_art_dimension': 88,
			'main_smaller_buttons': True,
			'main_initial_width': 390,
			'main_resizable': True,
			'main_show_bio': False,
		},
		
		'preset:Even Smaller':{
			'main_art_dimension': 80,
			'main_smaller_buttons': True,
			'main_show_statusbar': False,
			'main_decorated': False,
			'main_show_album': False,
			'main_show_bio': False,
			'main_resizable': False,
		},
		
		'preset:Just Buttons':{
			'main_show_art': False,
			'main_smaller_buttons': True,
			'main_show_statusbar': False,
			'main_decorated': False,
			'main_show_album': False,
			'main_show_artist': False,
			'main_show_title': False,
			'main_show_bio': False,
			'main_resizable': False,
		},
		
		'preset:No Art':{
			'main_show_art': False,
			'main_initial_width': 350,
			'main_resizable': True,
			'main_smaller_buttons': True,
			'main_show_bio': False,
		},
	}
	
	if section and section in section_values.keys():
		if value_name in section_values[section].keys():
			return section_values[section][value_name]
	
	if value_name in values.keys():
		return values[value_name]
	else:
		return ''
	
