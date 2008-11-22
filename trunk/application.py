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
import webbrowser
import default_values

REQURIRED_PYLAST = '= 0.2.18'

def pylast_check(required):
	pylast_url = 'http://pylast.googlecode.com/'
	
	try:
		import pylast
	except ImportError, e:
		print "Messing Dependency: Pylast %s!\nGrab it from %s" %(required, pylast_url)
		exit()
	
	greater = False
	equal = False
	smaller = False
	
	if '>' in required:
		greater = True
	if '<' in required:
		smaller = True
	if '=' in required:
		equal = True
	
	required = required[required.find(' ')+1:]
	
	def compare(a, b):
		"""Takes two versions as strings and compares them.
		Returns 1 if b > a, -1 if b < a, 0 if b == a."""
		
		a = a.split('.')
		b = b.split('.')
		
		for i in range(0, len(a)):
			if int(b[i]) > int(a[i]):
				#greater
				return 1
			elif int(b[i]) < int(a[i]):
				#smaller
				return -1
		
		#equal
		return 0
	
	c = compare(required, pylast.__version__)
	
	if c==1 and greater:
		pass
	elif c==-1 and smaller:
		pass
	elif c==0 and equal:
		pass
	else:
		print "Messing Dependency: Pylast %s!\nGrab it from %s" %(required, pylast_url)
		exit()

pylast_check(REQURIRED_PYLAST)

API_KEY =		'ecc0d2ded1ab6c21f1c9716a47476e45'
API_SECRET = 	'861595fdeeaf6142def95a0317482251'

NAME = 'Last Agent'
AUTHOR = 'Amr Hassan'
COMMENT = 'A Last.fm music tracker for Linux'
VERSION = '0.3.02'


class Application(object):
	
	def __init__(self):
		
		self.config_dir = os.path.expanduser('~/.lastagent/')
		self.cache_dir = os.path.join('/', self.config_dir, 'cache')
		
		if not os.path.exists(self.config_dir):
			os.mkdir(self.config_dir)
		
		self.presets = ini.INI(os.path.join('/', self.config_dir, 'display.new.conf'), default_values.get_default)
		self.user_details = ini.INI(os.path.join('/', self.config_dir, 'user.conf'), default_values.get_default)
		self.settings = ini.INI(os.path.join('/', self.config_dir, 'settings.conf'), default_values.get_default)
		
		self.version = VERSION
		self.name = NAME
		self.author = AUTHOR
		self.comment = COMMENT
		self.pixbuf_icon = gtk.gdk.pixbuf_new_from_file('gui/images/app_' + self.settings.get('icon_color', 'general') + '.png')
		self.waiting_animation = gtk.gdk.PixbufAnimation('gui/images/waiting1.gif')
		
		if self.settings.get_bool('run_on_session_startup', 'general'):
			os.system('cp -f lastagent.hidden.desktop ~/.config/autostart/')
		else:
			os.system('rm -f ~/.config/autostart/lastagent.hidden.desktop')
	
	def run(self):
		
		self.api_key = API_KEY
		self.secret = API_SECRET
		self.current_user = None
		
		gobject.threads_init()
		gtk.gdk.threads_init()
		
		main = gui.main_window.MainWindow(self)			
		main.fire_up()
		
		gtk.main()
