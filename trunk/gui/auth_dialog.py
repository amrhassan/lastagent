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
import pylast
import threading
import webbrowser


class AuthDialog(gtk.Dialog):
	def __init__(self, parent, app):
		gtk.Dialog.__init__(self, None, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.CAN_DEFAULT)
				
		self.app = app
		
		self.sg = pylast.SessionGenerator(app.api_key, app.secret)
		
		self.setup()
	
	def setup(self):
		#declarations
		self.main_box = gtk.HBox()
		self.icon = gtk.Image()
		self.icon_box = gtk.VBox()
		self.pane = gtk.VBox()
		self.welcome_label = gtk.Label()
		self.text_label = gtk.Label()
		self.url_box = gtk.HBox()
		self.url_entry = gtk.Entry()
		self.url_button = gtk.Button()
		self.status_label = gtk.Label()
		
		#self
		self.set_title('Authentication Required')
		self.vbox.pack_start(self.main_box)
		self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		
		#main_box
		self.main_box.set_border_width(10)
		self.main_box.pack_start(self.icon_box, False, False)
		self.main_box.pack_start(self.pane)
		
		#icon_box
		self.icon_box.pack_start(self.icon, False, False)
		
		#icon
		self.icon.set_from_stock(gtk.STOCK_DIALOG_AUTHENTICATION, gtk.ICON_SIZE_DIALOG)
		
		#pane
		self.pane.pack_start(self.welcome_label, False, False)
		self.pane.pack_start(self.text_label, False, False, 5)
		self.pane.pack_start(self.url_box, False, False, 6)
		self.pane.pack_start(self.status_label, False, False)
		
		#welcome_label
		self.welcome_label.set_alignment(0, 0.5)
		self.welcome_label.set_markup('<big><b>Welcome</b></big>')
		
		#text_label
		self.text_label.set_alignment(0, 0.5)
		self.text_label.set_line_wrap(True)
		self.text_label.set_text("In order for Last Agent to be able to access your profile, you have to authorize it at Last.fm's website.\nPlease click on the link below to open the authorization page.")
		
		#url_box
		self.url_box.pack_start(self.url_button, False, False)
		self.url_box.pack_start(self.url_entry)
		self.url_box.set_sensitive(False)
		
		#url_entry
		self.url_entry.set_property('editable', False)
		
		
		#url_button
		self.url_button.set_image(gtk.image_new_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_MENU))
		self.url_button.set_label('_Open Link')
		self.url_button.connect('clicked', self._on_url_button_clicked)
		
		#status_label
		self.status_label.set_alignment(0, 0.5)
		
		self.do_token()
		self.show_all()
	
	def _on_url_button_clicked(self, sender):
		webbrowser.open(self.auth_url)
	
	def do_token(self):
		self.set_status('Receiving authorization token')
		
		self.sg.async_call(self.do_token_callback, self.sg.getToken)
		self.sg.start()
	
	def do_token_callback(self, sender, token):
		if sender.last_error():
			self.sg.async_call(self.do_token_callback, self.sg.getToken)
			self.sg.start()
			print "Retrying to get token..."
			return
		
		self.token = token
		self.auth_url = self.sg.getAuthURL(token)
		
		gtk.gdk.threads_enter()
		self.url_entry.set_text(self.auth_url)
		self.url_box.set_sensitive(True)
		gtk.gdk.threads_leave()
		
		self.sg.async_call(None, self.do_get_data)
		self.sg.start()

	
	def do_get_data(self):
		self.set_status('Waiting for you to authorize Last Agent')
		data = self.sg.getSessionData(self.token)
		
		if self.sg.last_error():
			self.sg.clear_errors()
			timer = threading.Timer(1, self.do_get_data)
			timer.start()
			print "Retrying to receive Session Data..."
			return
		
		self.set_status('Configuring Last Agent. Please Wait')
		self.user_data = data
		self.response(gtk.RESPONSE_OK)
	
	def set_status(self, msg):
		self.status_label.set_markup('<b>Status:</b> ' + msg + '...')
	
	def get_user_data(self):
		
		out = None
		
		if self.run() == gtk.RESPONSE_OK:
			out = self.user_data
		
		self.destroy()
		return out
