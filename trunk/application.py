#!/usr/bin/env python

import configs
import os
import gui.auth_wizard
import gtk

API_KEY =		'ecc0d2ded1ab6c21f1c9716a47476e45'
API_SECRET = 	'861595fdeeaf6142def95a0317482251'

class Application(object):
	
	def __init__(self):
		self.config_dir = os.path.expanduser('~/.lastAgent/')
		
		if not os.path.exists(self.config_dir):
			os.mkdir(self.config_dir)
		
		self.settings = configs.Configs(self.config_dir + 'settings.config')
		
		self.run()
	
	def run(self):
		if self.settings.get('authenticated', 'false') == 'false':
			wiz = gui.auth_wizard.AuthWizard(API_KEY, API_SECRET, self.settings)
			wiz.show()
		
		
		gtk.gdk.threads_init() 
		gtk.main()
	

a = Application()
