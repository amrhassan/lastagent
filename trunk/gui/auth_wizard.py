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
import ini
import pylast
import webbrowser
import os

class AuthWizard(object):
	
	def __init__(self, api_key, secret, app):
		
		self.api_key = api_key
		self.secret = secret
		
		self.app = app
		
		self.order = (self.do_intro, self.do_token, self.do_auth, self.do_retrieve, self.do_done)
		self.order_index = -1
	
	def execute_next(self):
		self.order_index += 1
		call = self.order[self.order_index]
		
		self.proceed_off()
		self.redo_off()
		
		call()
	
	def execute_same(self):
		call = self.order[self.order_index]
		
		self.proceed_off()
		self.redo_off()
		
		call()
	
	def set_image(self, stock_id):
		self.main_image.set_from_stock(stock_id, gtk.ICON_SIZE_DIALOG)
		self.main_image.show()
	
	def clear_context(self):
		for widget in self.context_container.get_children():
			self.context_container.remove(widget)
	
	def add_context(self, widget):
		self.context_container.pack_start(widget, True, False, 10)
		widget.show()
	
	def add_context_text(self, message):
		label = gtk.Label(message)
		label.set_line_wrap(True)
		self.add_context(label)
	
	def show_error(self, message):
		self.clear_context()
		self.add_context_text(message)
		self.set_image(gtk.STOCK_DIALOG_ERROR)
		
		self.redo_on()
	
	def do_intro(self):
		self.set_image(gtk.STOCK_DIALOG_INFO)
		self.add_context_text('Welcome to the Authentication Wizard.\nPlease press Forward to start...')
		
		self.proceed_on()
	
	def do_token(self):
		self.set_image(gtk.STOCK_NETWORK)
		self.clear_context()
		self.add_context_text('Requesting token from last.fm.\nPlease Wait...')
		
		self.proceed_off()
		
		generator = pylast.SessionGenerator(self.api_key, self.secret)
		generator.async_call(self.token_callback, generator.getToken)	
		generator.start()

	def token_callback(self, sender, token):
		if sender.last_error():
			self.show_error(sender.last_error())
		else:
			self.token = token
			self.clear_context()
			self.add_context_text('Token requested successfully.\nPress Forward to continue...')
			self.proceed_on()
			self.forward_button.clicked()

	def do_auth(self):
		self.set_image(gtk.STOCK_DIALOG_AUTHENTICATION)
		self.clear_context()
		self.add_context_text("Please open the following URL in your web browser and complete the authentication process by giving %s the permission to submit changes to your profile.\nHaving done that, kindly press Forward.")
		e = gtk.Entry()
		url = pylast.SessionGenerator(self.api_key, self.secret).getAuthURL(self.token)
		self.auth_url = url
		e.set_text(url)
		e.show()
		b = gtk.Button('_Open in Browser')
		b.set_image(gtk.image_new_from_stock(gtk.STOCK_EXECUTE, gtk.ICON_SIZE_BUTTON))
		b.connect('clicked', self.on_open_in_browser_clicked)
		b.show()
		box = gtk.HBox()
		box.pack_start(e)
		box.pack_start(b, False)
		box.show()
		self.context_container.pack_start(box, False, False, 10)
		b.grab_focus()
	
	def do_retrieve(self):
		self.set_image(gtk.STOCK_NETWORK)
		self.clear_context()
		self.add_context_text('Retrieving user data from last.fm.\nPlease Wait...')
		
		self.proceed_off()
		
		g = pylast.SessionGenerator(self.api_key, self.secret)
		g.async_call(self.retrieve_callback, g.getSessionData, self.token)
		g.start()
	
	def retrieve_callback(self, sender, output):
		if sender.last_error():
			self.order_index -= 1
			self.show_error(sender.last_error())
		else:
			self.app.user_details.set('name', output['name'], 'user')
			self.app.user_details.set('subscriber', str(output['subscriber']), 'user')
			self.app.user_details.set('session_key', output['key'], 'user')
			
			self.proceed_on()
			self.forward_button.clicked()
	
	def do_done(self):
		self.clear_context()
		self.set_image(gtk.STOCK_DIALOG_INFO)
		self.add_context_text('User data has been retrieved successfully.\nPress Finish and restart %s.' % self.app.name)
		self.quit_button.set_label('_Finish')
		self.quit_button.set_image(gtk.image_new_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_BUTTON))
		self.quit_button.grab_focus()
		
		self.proceed_off()
	
	def show(self):
		#dialog
		self.dialog = gtk.Dialog('Authentication Wizard', None, gtk.DIALOG_DESTROY_WITH_PARENT)
		self.dialog.set_border_width(10)
		self.dialog.resize(450, 200)
		
		#redo_button
		self.redo_button = gtk.Button('back', gtk.STOCK_REDO)
		self.redo_button.connect('clicked', self.on_redo_button_clicked)
		self.dialog.action_area.pack_start(self.redo_button)
		self.redo_button.show()
		
		#forward_button
		self.forward_button = gtk.Button('next', gtk.STOCK_GO_FORWARD)
		self.forward_button.connect('clicked', self.on_forward_button_clicked)	
		self.dialog.action_area.pack_start(self.forward_button)
		self.forward_button.show()
		
		#quit_button
		self.quit_button = gtk.Button('quit', gtk.STOCK_QUIT)
		self.dialog.action_area.pack_start(self.quit_button)
		self.quit_button.connect('clicked', self.on_quit_button_clicked)
		self.quit_button.show()
		
		#containers
		self.main_container = gtk.HBox()
		self.main_image = gtk.Image()
		self.set_image(gtk.STOCK_MISSING_IMAGE)
		self.main_container.pack_start(self.main_image, False, True, 30)
		self.context_container = gtk.VBox()
		self.main_container.pack_start(self.context_container)
		self.main_container.show()
		self.context_container.show()
		
		self.dialog.vbox.pack_start(self.main_container)
		
		self.execute_next()
		
		self.dialog.show()
	
	
	def on_forward_button_clicked(self, button):
		self.execute_next()
	
	def on_redo_button_clicked(self, button):
		self.execute_same()
	
	def on_quit_button_clicked(self, button):
		self.dialog.destroy()
		gtk.main_quit()
		quit()
	
	def on_open_in_browser_clicked(self, button):
		webbrowser.open(self.auth_url)
		self.proceed_on()
		
	def proceed_on(self):
		self.forward_button.set_sensitive(True)
		self.forward_button.grab_focus()
	
	def proceed_off(self):
		self.forward_button.set_sensitive(False)
	
	def redo_on(self):
		self.redo_button.set_sensitive(True)
		self.redo_button.grab_focus()
	
	def redo_off(self):
		self.redo_button.set_sensitive(False)
