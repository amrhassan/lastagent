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

import ini
import os
import gui.auth_wizard
import gui.main_window
import gtk
import pylast

API_KEY =		'ecc0d2ded1ab6c21f1c9716a47476e45'
API_SECRET = 	'861595fdeeaf6142def95a0317482251'

class Application(object):
	
	def __init__(self):
		
		self.version = '0.1.0'
		self.name = 'Last Agent'
		self.author = 'Amr Hassan'
		self.comment = 'A Last.fm music tracker for Linux'
		self.pixbuf_icon = gtk.gdk.pixbuf_new_from_file('gui/images/app.png')
		self.waiting_animation = gtk.gdk.PixbufAnimation('gui/images/waiting1.gif')
		
		self.config_dir = os.path.expanduser('~/.lastagent/')
		self.cache_dir = os.path.join('/', self.config_dir, 'cache')
		
		if not os.path.exists(self.config_dir):
			os.mkdir(self.config_dir)
		
		self.settings = ini.INI(os.path.join('/', self.config_dir, 'settings.config'))

	
	def run(self):
		
		if not self.settings.get('session_key', None, 'user'):
			wiz = gui.auth_wizard.AuthWizard(API_KEY, API_SECRET, self.settings)
			wiz.show()
		else:
			self.auth_data = (API_KEY, API_SECRET, self.settings.get('session_key', None, 'user'))
			self.current_user = pylast.User(self.settings.get('name', '', 'user'), *self.auth_data)
			
			main = gui.main_window.MainWindow(self)
			
			main.fire_up()
		
		gtk.gdk.threads_init() 
		gtk.main()
