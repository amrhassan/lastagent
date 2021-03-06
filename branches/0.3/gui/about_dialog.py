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
import webbrowser

class AboutApp(gtk.AboutDialog):
	def __init__(self, app):
		
		gtk.AboutDialog.__init__(self)
		
		gtk.about_dialog_set_url_hook(self.on_click_url, None)
		
		self.set_name(app.name)
		self.set_version(app.version)
		self.set_copyright(app.author)
		self.set_comments(app.comment)
		self.set_license(open('LICENSE').read())
		self.set_wrap_license(True)
		self.set_website('http://lastagent.googlecode.com/')
		self.set_authors(('Amr Hassan (amr.hassan@gmail.com)',))
		self.set_artists((
			'Chris Gorvan (www.gorvan.com)\n\tApplication icons are taken from the "Last.fm icons 2" set.\n',
			'Last.fm web site and official client icon designers\n\tThe rest of the icons.\n',
			'Amarok, Banshee, Audacious and Rhythmbox Icon designers\n\tThe Icons of Amarok, Banshee, Audacious and Rhythmbox.\n',
			))
		self.set_logo(app.pixbuf_icon)
		self.set_icon(app.pixbuf_icon)
		self.connect('response', self.on_response)
		

	def on_response(self, sender, response):
		sender.destroy()
	
	def on_click_url(self, sender, url, data):
		webbrowser.open(url)

