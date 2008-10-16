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

import pygtk
pygtk.require('2.0')

import ini
import os
import gui.main_window
import gtk
import gobject
import pylast
import webbrowser
import default_values

API_KEY =		'ecc0d2ded1ab6c21f1c9716a47476e45'
API_SECRET = 	'861595fdeeaf6142def95a0317482251'

NAME = 'Last Agent'
AUTHOR = 'Amr Hassan'
COMMENT = 'A Last.fm music tracker for Linux'
VERSION = '0.2.05'


class Application(object):
	
	def __init__(self):
		self.config_dir = os.path.expanduser('~/.lastagent/')
		self.cache_dir = os.path.join('/', self.config_dir, 'cache')
		
		if not os.path.exists(self.config_dir):
			os.mkdir(self.config_dir)
		
		self.presets = ini.INI(os.path.join('/', self.config_dir, 'display.conf'), default_values.get_default)
		self.user_details = ini.INI(os.path.join('/', self.config_dir, 'user.conf'), default_values.get_default)
		self.settings = ini.INI(os.path.join('/', self.config_dir, 'settings.conf'), default_values.get_default)
		
		self.version = VERSION
		self.name = NAME
		self.author = AUTHOR
		self.comment = COMMENT
		self.pixbuf_icon = gtk.gdk.pixbuf_new_from_file('gui/images/app_' + self.settings.get('icon_color', 'general') + '.png')
		self.waiting_animation = gtk.gdk.PixbufAnimation('gui/images/waiting1.gif')
		
		#To make Last Agent work on session startup
		os.system('cp -f lastagent.hidden.desktop ~/.config/autostart/')

	
	def run(self):
		
		self.api_key = API_KEY
		self.secret = API_SECRET
		self.current_user = None
		
		gobject.threads_init()
		gtk.gdk.threads_init()
		
		main = gui.main_window.MainWindow(self)			
		main.fire_up()
		
		gtk.main()
