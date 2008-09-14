
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
		
		self.version = '0.10'
		self.name = 'Last Agent'
		self.author = 'Amr Hassan'
		self.comment = 'A Last.fm music tracker for Linux'
		self.pixbuf_icon = gtk.gdk.pixbuf_new_from_file('gui/images/app_red.ico')
		
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
			main.show()
		
		gtk.gdk.threads_init() 
		gtk.main()

a = Application()
a.run()
