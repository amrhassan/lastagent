import py2deb

NAME = 'pylast'
VERSION = '0.2b9'
DESCRIPTION = 'Python bindings for last.fm webservices 2.0'
LICENSE = 'gpl'
DEPENDS = 'python'
SECTION = 'python'
URL = 'http://code.google.com/p/pylast/'
AUTHOR = 'Amr Hassan'
EMAIL = 'amr.hassan@gmail.com'
ARCHITECTURE = 'all'
CHANGES = open('changes.txt').read()

app = py2deb.Py2deb(NAME, DESCRIPTION, LICENSE, DEPENDS, SECTION, ARCHITECTURE, URL, AUTHOR, EMAIL)

app['/usr/lib/python2.5/site-packages'] = ['pylast.py',]

print app.generate(VERSION, CHANGES, True, False)
