import os
import py2deb
from os.path import join, split

NAME = 'lastagent'
VERSION = '0.2.0'
DESCRIPTION = 'A Last.fm music tracker for Linux'
LICENSE = 'gpl'
DEPENDS = 'python, python-dbus, python-gtk2, python-sexy'
SECTION = 'python'
URL = 'http://lastagent.tuxfamily.org'
AUTHOR = 'Amr Hassan'
EMAIL = 'amr.hassan@gmail.com'
ARCHITECTURE = 'all'
CHANGES = ''

app = py2deb.Py2deb(NAME, DESCRIPTION, LICENSE, DEPENDS, SECTION, ARCHITECTURE, URL, AUTHOR, EMAIL)

root = '/usr/share/lastagent'

forbidden_dirs = ('.svn', '.py2deb_build_folder')
forbidden_files = ('geany_run_script.sh', 'lastagent.desktop', '_tmp-lastagent', '_packager.py', 'INSTALL', 'installer')
files = {}
files[root] = list()

def add_dir(path):
	for i in os.listdir(path):
		
		if os.path.isdir(join(path, i)):
			if not i in forbidden_dirs:
				add_dir(join(path, i))
		else:
			file_name = split(path)[1]
			
			if (not i in forbidden_files) and (not file_name.endswith('~')):
				
				file_path = join(path, i).strip()
				files[root].append(file_path)


add_dir('.')

app['/usr/bin'] = ['./lastagent']
app['/usr/share/applications'] = ['./lastagent.desktop']
app['/usr/lib/python2.5/site-packages'] = ['/media/Infernos/Projikts/Python/pylast/trunk/pylast.py']

for path in files.keys():
	app[path] = files[path]

app.generate(VERSION, CHANGES, True, False)

os.system('sudo dpkg -i *.deb')

os.system('mv *.deb ../package/ -f -v')
os.system('mv *.rpm ../package/ -f -v')
