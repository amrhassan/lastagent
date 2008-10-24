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
import gobject
import pylast
from pylast import Track
import os
import sys
import players.current
import threading
import webbrowser
from share_dialog import ShareDialog
from tag_dialog import TagDialog
from custom_labels import *
from image_store import *
from stock_setup import *
from about_dialog import AboutApp
from custom_widgets import *
from add_dialog import *
from presets_edit_dialog import *
from status_bar import *
from auth_dialog import *
from art_box import *

PROCESS_TAG = 0
PROCESS_LOVE = 1
PROCESS_SHARE = 2
PROCESS_ADD = 3

class MainWindow(gtk.Window):
	
	def __init__(self, application):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		
		self.app = application
		
		self.authenticated = False
		
		self.shown_track = None
		self.shown_artist = None
		self.shown_album = None
		
		self.active_preset = 'preset:' + self.app.presets.get('current_preset', 'general')
		self.presets_dict = {}	#{preset_radio_menuitem: 'preset_name',}
		
		self.hidden = False
		
		get_factory().add_default()
	
	def check_authentication(self):
		if not self.app.user_details.get('session_key', 'user'):
			self.toggle_iconified()
			
			data = AuthDialog(self, self.app).get_user_data()
			
			if not data:
				exit()
			else:
				self.app.user_details.set('name', data['name'], 'user')
				self.app.user_details.set('subscriber', str(data['subscriber']), 'user')
				self.app.user_details.set('session_key', data['key'], 'user')
			
			self.toggle_iconified()
		
		self.app.auth_data = (self.app.api_key, self.app.secret, self.app.user_details.get('session_key', 'user'))
		self.app.current_user = pylast.User(self.app.user_details.get('name', 'user'), *self.app.auth_data)
		self.authenticated = True
	
	def reset_size(self):
		self.resize(self.app.presets.get_int('main_initial_width', self.active_preset), 1)
	
	def setup(self):
		#declarations
		self.main_box = gtk.VBox()
		self.content_box = gtk.HBox(False, 10)
		self.art = ArtBox(self.app)
		self.art_box = gtk.VBox()
		self.track_box = gtk.VBox()
		self.title_label = TitleLabel()
		self.title_box = gtk.HBox()
		self.artist_label = ArtistLabel()
		self.artist_box = gtk.HBox()
		self.by_label = gtk.Label()
		self.not_playing_label = gtk.Label()
		self.track_pane_box = gtk.VBox()
		self.love_button = MainButton()
		self.share_button = MainButton()
		self.tag_button = MainButton()
		self.track_buttons_box = gtk.HBox()
		self.main_buttons_box = gtk.HBox()
		self.love_image = gtk.Image()
		self.share_image = gtk.Image()
		self.tag_image = gtk.Image()
		self.playlist_image = gtk.Image()
		self.share_button = MainButton()
		self.tag_button = MainButton()
		self.playlist_add_button = MainButton()
		self.status_bar = StatusBar()
		self.status_icon = gtk.StatusIcon()
		self.album_label = AlbumLabel()
		self.album_box = gtk.HBox()
		self.waiting_animation = gtk.gdk.PixbufAnimation('gui/images/waiting1.gif')
		self.quit_action = gtk.Action('quit', '_Quit', 'Exit', gtk.STOCK_QUIT)
		self.about_action = gtk.Action('about', '_About', 'About', gtk.STOCK_ABOUT)
		self.love_track_action = gtk.Action('love-track', '_Love', 'Love the currently playing track', STOCK_LOVE)
		self.tag_track_action = gtk.Action('tag-track', '_Tag...', 'Tag the currently playing track', STOCK_TAG)
		self.share_track_action = gtk.Action('share-track', '_Share...', 'Share the currently playing track', STOCK_SHARE)
		self.tag_artist_action = gtk.Action('tag-artist', '_Tag...', 'Tag the artist', STOCK_TAG)
		self.share_artist_action = gtk.Action('share-artist', '_Share...', 'Share the artist', STOCK_SHARE)
		self.tag_album_action = gtk.Action('tag-album', '_Tag...', 'Tag the album', STOCK_TAG)
		self.share_album_action = gtk.Action('share-album', '_Share...', 'Share an album', STOCK_SHARE)
		self.playlist_add_action = gtk.Action('playlist-add', '_Add...', 'Add to playlist', STOCK_PLAYLIST)
		
		
		#self
		self.reset_title()
		self.set_position(gtk.WIN_POS_CENTER)
		self.add(self.main_box)
		self.connect('delete_event', self.on_self_delete)
		self.connect('show', self.on_self_show)
		self.connect('hide', self.on_self_hide)
		self.set_icon(self.app.pixbuf_icon)
		self.deletable = False

		
		#status_icon
		self.status_icon.set_from_pixbuf(self.app.pixbuf_icon)
		self.status_icon.set_visible(True)
		self.status_icon.set_tooltip(self.get_title())
		self.status_icon.connect('activate', self.on_status_icon_activate)
		self.status_icon.connect('popup-menu', self.on_status_icon_popup)
		
		#main_box
		self.main_box.pack_start(self.content_box)
		self.main_box.pack_end(self.status_bar, False)
		self.main_box.show()
		
		#content_box
		self.content_box.pack_start(self.art_box, False, False)
		self.content_box.pack_start(self.track_pane_box)
		self.content_box.set_border_width(10)
		self.content_box.show()
		
		#art_box
		self.art_box.pack_start(self.art, False)
		self.art_box.show()
		
		#art
		self.art.show()
		
		#artist_label
		self.artist_label.set_tag_action(self.tag_artist_action)
		self.artist_label.set_share_action(self.share_artist_action)
		self.artist_label.show()
		
		#title_box
		self.title_box.pack_start(self.title_label, False, False)
		self.title_box.show()
		
		#title_label
		self.title_label.show()
		self.title_label.set_alignment(0, 0.5)
		self.title_label.set_love_action(self.love_track_action)
		self.title_label.set_tag_action(self.tag_track_action)
		self.title_label.set_share_action(self.share_track_action)
		self.title_label.set_add_action(self.playlist_add_action)
		
		#by_label
		self.by_label.set_markup('<b>by </b>')
		self.by_label.show()
		
		#artist_box
		self.artist_box.pack_start(self.by_label, False, False)
		self.artist_box.pack_start(self.artist_label, False, False)
		self.artist_box.show()
		
		#track_box
		self.track_box.pack_start(self.title_box, False, False)
		self.track_box.pack_start(self.artist_box, False, False)
		self.track_box.pack_start(self.album_box, False, False)
		self.track_box.show()
		
		#not_playing_label
		self.not_playing_label.set_markup('<big><b>Not Playing</b></big>')
		self.not_playing_label.set_sensitive(False)
		
		#status_bar
		self.status_bar.set_to_not_playing()
		
		#tag_button
		self.tag_button.set_image(gtk.image_new_from_stock(STOCK_TAG, gtk.ICON_SIZE_BUTTON))
		self.tag_button.connect_object('clicked', gtk.Action.activate, self.tag_track_action)
		self.tag_button.set_normal_label('_Tag')
		self.tag_button.set_smaller_tooltip('Tag')
		self.tag_button.set_focus_on_click(False)
		self.tag_button.show()
		
		#share_button
		self.share_button.set_image(gtk.image_new_from_stock(STOCK_SHARE, gtk.ICON_SIZE_BUTTON))
		self.share_button.connect_object('clicked', gtk.Action.activate, self.share_track_action)
		self.share_button.set_normal_label('_Share')
		self.share_button.set_smaller_tooltip('Share')
		self.share_button.set_focus_on_click(False)
		self.share_button.show()
		
		#playlist_add_button
		self.playlist_add_button.set_image(gtk.image_new_from_stock(STOCK_PLAYLIST, gtk.ICON_SIZE_BUTTON))
		self.playlist_add_button.connect_object('clicked', gtk.Action.activate, self.playlist_add_action)
		self.playlist_add_button.set_normal_label('_Add')
		self.playlist_add_button.set_smaller_tooltip('Add to a playlist')
		self.playlist_add_button.set_focus_on_click(False)
		self.playlist_add_button.show()
		
		#love_button
		self.love_button.set_image(gtk.image_new_from_stock(STOCK_LOVE, gtk.ICON_SIZE_BUTTON))
		self.love_button.connect_object('clicked', gtk.Action.activate, self.love_track_action)
		self.love_button.set_normal_label('_Love')
		self.love_button.set_smaller_tooltip('Love')
		self.love_button.set_focus_on_click(False)
		self.love_button.show()
		
		#track_buttons_box
		self.track_buttons_box.pack_end(self.share_button, False, False, 2)
		self.track_buttons_box.pack_end(self.playlist_add_button, False, False, 2)
		self.track_buttons_box.pack_end(self.tag_button, False, False, 2)
		self.track_buttons_box.pack_end(self.love_button, False, False, 2)
		
		#album_box
		self.album_box.pack_start(self.album_label, False, False)
		self.album_box.show()
		
		#album_label
		self.album_label.set_alignment(0, 0.5)
		self.album_label.set_ellipsize(pango.ELLIPSIZE_END)
		self.album_label.set_tag_action(self.tag_album_action)
		self.album_label.set_share_action(self.share_album_action)
		
		#track_pane_box
		self.track_pane_box.pack_start(self.track_box, False, False)
		self.track_pane_box.pack_start(self.not_playing_label)
		self.track_pane_box.pack_end(self.track_buttons_box, False)
		self.track_pane_box.show()
		
		#quit_action
		self.quit_action.connect('activate', self.on_quit_action_activate)
		
		#about_action
		self.about_action.connect('activate', self.on_about_action_activate)
		
		#love_track_action
		self.love_track_action.connect('activate', self.on_love_track_action_activate)
		
		#tag_track_action
		self.tag_track_action.connect('activate', self.on_tag_track_action_activate)
		
		#share_track_action
		self.share_track_action.connect('activate', self.on_share_track_action_activate)
		
		#tag_artist_action
		self.tag_artist_action.connect('activate', self.on_tag_artist_action_activate)
		
		#share_artist_action
		self.share_artist_action.connect('activate', self.on_share_artist_action_activate)
		
		#tag_album_action
		self.tag_album_action.connect('activate', self.on_tag_album_action_activate)
		
		#share_album_action
		self.share_album_action.connect('activate', self.on_share_album_action_activate)
		
		#playlist_add_action
		self.playlist_add_action.connect('activate', self.on_playlist_add_action_activate)
		
		self.apply_configs()
	
	def reset_title(self):
		if not self.app.current_user:
			self.set_title('%s' %(self.app.name))
		else:
			self.set_title('%s: %s' %(self.app.name, self.app.current_user.getName()))
	
	def _create_tray_menu(self):
		menu = gtk.Menu()
		
		#track menu
		if self.shown_track:
			if self.app.presets.get_bool('menu_show_track', self.active_preset):
				track_item = gtk.ImageMenuItem()
				
				size = self.app.presets.get_int('menu_track_art_size', self.active_preset)
				track_item.set_image(self.art.get_image_resized(size))
				
				vbox = gtk.VBox()
				vbox_dummy1 = gtk.VBox()
				vbox_dummy2 = gtk.VBox()
				artist_l = gtk.Label('by ' + self.shown_track.getArtist().getName())
				artist_l.set_alignment(0, 0.5)
				title_l = gtk.Label()
				title_l.set_markup('<b>' + self.shown_track.getTitle().replace('&', '&amp;') + '</b>')
				title_l.set_alignment(0, 0.5)

				
				vbox.pack_start(vbox_dummy1)
				vbox.pack_start(title_l, False, False)
				vbox.pack_start(artist_l, False, False)
				vbox.pack_start(vbox_dummy2)
				track_item.add(vbox)
				
				
				track_item.connect('button-press-event', self.on_track_menuitem_pressed)
				
				menu.append(track_item)
			else:
				show_item = gtk.ImageMenuItem('Sh_ow')
				show_item.connect('button-press-event', self.on_track_menuitem_pressed)
				menu.append(show_item)
			
			menu.append(gtk.SeparatorMenuItem())
			
			menu.append(self.love_track_action.create_menu_item())
			menu.append(self.tag_track_action.create_menu_item())
			menu.append(self.playlist_add_action.create_menu_item())
			menu.append(self.share_track_action.create_menu_item())
			
			menu.append(gtk.SeparatorMenuItem())
			
			artist_menu = gtk.Menu()
			artist_menu.append(self.tag_artist_action.create_menu_item())
			artist_menu.append(self.share_artist_action.create_menu_item())
			
			artist_item = gtk.ImageMenuItem(self.shown_artist.getName())
			artist_item.set_image(gtk.image_new_from_stock(STOCK_ARTIST, gtk.ICON_SIZE_MENU))
			artist_item.set_submenu(artist_menu)
			menu.append(artist_item)
			
			if self.shown_album:
				#menu.append(gtk.SeparatorMenuItem())
				
				album_item = gtk.ImageMenuItem()
				album_item.set_image(gtk.image_new_from_stock(STOCK_ALBUM, gtk.ICON_SIZE_MENU))
				album_label = gtk.Label(self.shown_album.getTitle())
				album_label.set_alignment(0, 0.5)
				album_label.set_ellipsize(pango.ELLIPSIZE_END)
				album_item.add(album_label)
				
				album_menu = gtk.Menu()
				album_menu.append(self.tag_album_action.create_menu_item())
				album_menu.append(self.share_album_action.create_menu_item())
				
				album_item.set_submenu(album_menu)
				
				menu.append(album_item)
				
			menu.append(gtk.SeparatorMenuItem())
		
		profile_item = gtk.ImageMenuItem('_My Last.fm Page')
		profile_item.set_image(gtk.image_new_from_stock(STOCK_NETWORK, gtk.ICON_SIZE_MENU))
		profile_item.connect('button-press-event', self.on_profile_item_clicked)
		menu.append(profile_item)
		menu.append(gtk.SeparatorMenuItem())
		
		display_item = gtk.ImageMenuItem('Display _Presets')
		display_item.set_image(gtk.image_new_from_stock(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_MENU))
		submenu = gtk.Menu()
		display_item.set_submenu(submenu)
		
		presets = self.app.presets.get('presets', 'general').split(';')
		group = None
		for preset in presets:
			preset_item = gtk.RadioMenuItem(group, preset)
			if preset == self.app.presets.get('current_preset', 'general'):
				preset_item.set_active(True)
			preset_item.connect('button-release-event', self.on_preset_changed)
			self.presets_dict[preset_item] = preset
			if not group:
				group = preset_item
			submenu.append(preset_item)
		
		submenu.append(gtk.SeparatorMenuItem())
		edit_item = gtk.ImageMenuItem('_Edit')
		edit_item.connect('button-release-event', self.on_edit_menu_clicked)
		submenu.append(edit_item)
		
		menu.append(display_item)
		menu.append(gtk.SeparatorMenuItem())
		menu.append(self.about_action.create_menu_item())
		menu.append(self.quit_action.create_menu_item())
		
		menu.show_all()
		
		return menu
	
	def on_profile_item_clicked(self, sender, event):
		url = self.app.current_user.getURL()
		webbrowser.open(url)
	
	def on_preset_changed(self, sender, event):
		preset = self.presets_dict[sender]
		
		self.change_preset(preset)
	
	def change_preset(self, new_preset = None):
		self.active_preset = 'preset:' + new_preset
		
		self.app.presets.set('current_preset', new_preset, 'general')
		self.apply_configs()
	
	def get_playing_data(self):
		"""Returns a (player, track) tuple."""
		
		if not self.authenticated:
			return
		
		player = players.current.getRunning()
		
		if player:
			return (player, Track(player.getArtist(), player.getTitle(), *self.app.auth_data))
		
		return None
	
	def show_not_playing(self, not_playing = True):
		gtk.gdk.threads_enter()
		if not_playing:
			self.not_playing_label.show()
			self.track_box.hide()
			self.track_buttons_box.set_sensitive(False)
			self.album_label.hide()
			self.status_icon.set_tooltip(self.get_title())
			self.status_bar.set_to_not_playing()
			self.art.disable()
		else:
			self.art.enable()
			self.not_playing_label.hide()
			self.track_box.show()
			self.track_buttons_box.set_sensitive(True)
		gtk.gdk.threads_leave()
		
		self.art.show_default()

	def show_track(self):
		self.restart_timer()
		data = self.get_playing_data()
		
		if not data:
			self.show_not_playing()
			
			gtk.gdk.threads_enter()
			self.shown_track = None
			self.shown_album = None
			self.shown_artist = None
			self.reset_size()
			gtk.gdk.threads_leave()
			
			return
		
		player = data[0]
		track = data[1]
		
		if self.shown_track and track._hash() == self.shown_track._hash():
			return
		
		self.art.show_default()
		self.show_not_playing(not_playing = False)
		
		gtk.gdk.threads_enter()
		self.album_label.hide()
		self.artist_label.set_artist(track.getArtist())
		self.title_label.set_track(track)
		
		artist = track.getArtist()
		
		self.shown_track = track
		self.shown_artist = artist
		self.shown_album = None
		self.status_icon.set_tooltip(track.toStr())
		self.status_bar.set_player(player)
		self.reset_size()
		gtk.gdk.threads_leave()
		
		track.async_call(track.getImage, self._get_image_callback, (pylast.IMAGE_LARGE, True))
	
	def restart_timer(self):
		
		interval = float(self.app.settings.get('updating_interval', 'tracker'))
		
		self.timer = threading.Timer(interval, self.show_track)
		self.timer.start()
	
	def _get_image_callback(self, sender, url):
		
		#show album
		if sender.getAlbum().getTitle() and self.app.presets.get_bool('main_show_album', self.active_preset):
			gtk.gdk.threads_enter()
			self.album_label.show()
			self.shown_album = sender.getAlbum()
			self.album_label.set_album(self.shown_album)
			gtk.gdk.threads_leave()
		
		self.art.set_art(url)
	
	def set_status_working(self, process, object):
		
		if process == PROCESS_LOVE:
			text = 'Loving ' + object.toStr() + '...'
		elif process == PROCESS_TAG:
			text = 'Tagging ' + object.toStr() + '...'
		elif process == PROCESS_SHARE:
			text = 'Sharing ' + object.toStr() + '...'
		elif process == PROCESS_ADD:
			text = 'Adding ' + object.toStr() + ' to a playlist...'
		
		#working status is always set from this thread, no need to thread_enter() and thread_leave() it.
		self.status_bar.set_status(text)
		self.status_bar.set_icon_from_animation(self.waiting_animation)
	
	def set_status_success(self, process, object):
		
		if process == PROCESS_LOVE:
			name = 'loved'
		elif process == PROCESS_TAG:
			name = 'tagged'
		elif process == PROCESS_SHARE:
			name = 'shared'
		elif process == PROCESS_ADD:
			name = 'added'
		
		gtk.gdk.threads_enter()
		self.status_bar.set_status('%s was %s successfully.' %(object.toStr(), name), 5.0)
		self.status_bar.set_icon_from_stock(gtk.STOCK_APPLY)
		gtk.gdk.threads_leave()
	
	def set_status_error(self, process, object):
		
		if process == PROCESS_LOVE:
			action = 'loved'
		elif process == PROCESS_TAG:
			action = 'tagged'
		elif process == PROCESS_SHARE:
			action = 'shared'
		elif process == PROCESS_ADD:
			action = 'added'
		
		gtk.gdk.threads_enter()
		self.status_bar.set_status('%s could not be %s.' %(object.toStr(), action), 5.0)
		self.status_bar.set_icon_from_stock(gtk.STOCK_DIALOG_ERROR)
		gtk.gdk.threads_leave()
		
		message = 'An error has occured and %s was not %s.\n\nDetails:\n%s' \
		%(object.toStr(), action, object.last_error().__str__())
		
		mb = MessageBox("Error", message, gtk.STOCK_DIALOG_ERROR, self)
		mb.show()

	def love_callback(self, sender, output):
		if sender.last_error():
			self.set_status_error(PROCESS_LOVE, sender)
		else:
			self.set_status_success(PROCESS_LOVE, sender)
	
	def on_love_track_action_activate(self, sender):
		target = self.shown_track
		
		self.set_status_working(PROCESS_LOVE, target)
		
		target.async_call(target.love, self.love_callback)
	
	def on_share_track_action_activate(self, sender):
		
		self.share(self.shown_track)
	
	def share(self, target):
		
		d = ShareDialog(self, self.app, target)
		
		output = d.get_recipients()
		
		if output:
			self.set_status_working(PROCESS_SHARE, target)
			target.async_call(target.share, self.share_callback, (output[0], output[1]))
	
	def tag_callback(self, sender, output):
		if sender.last_error():
			self.set_status_error(PROCESS_TAG, sender)
		else:
			self.set_status_success(PROCESS_TAG, sender)
	
	def share_callback(self, sender, output):
		if sender.last_error():
			self.set_status_error(PROCESS_SHARE, sender)
		else:
			self.set_status_success(PROCESS_SHARE, sender)
	
	def on_tag_track_action_activate(self, sender):
		
		self.tag(self.shown_track)
	
	def on_tag_artist_action_activate(self, sender):
		self.tag(self.shown_track.getArtist())
	
	def on_share_artist_action_activate(self, sender):
		self.share(self.shown_track.getArtist())
	
	def on_tag_album_action_activate(self, sender):
		if self.shown_album:
			self.tag(self.shown_album)
	
	def on_share_album_action_activate(self, sender):
		if self.shown_album:
			self.share(self.shown_album)
	
	def tag(self, target):
		#target is Track, Artist or Album
		
		td = TagDialog(self, self.app, target)
		
		tag_names = td.get_tags()
		
		if tag_names != None:
			self.set_status_working(PROCESS_TAG, target)
			target.async_call(target.setTags, self.tag_callback, tag_names)
	
	def on_status_icon_activate(self, sender):
		self.toggle_iconified()
	
	def toggle_iconified(self):
		if self.hidden:
			self.present()
		else:
			self.hide()
	
	def on_status_icon_popup(self, statusicon, button, time):
		self._create_tray_menu().popup(None, None, None, button, time)
	
	def on_quit_action_activate(self, sender):
		quit()
	
	def on_self_delete(self, sender, event):
		self.toggle_iconified()
		return True

	def on_about_action_activate(self, sender):
		d = AboutApp(self.app)
		d.run()

	def on_track_menuitem_pressed(self, sender, event):
		print "pressed"
		self.present()
	
	def on_self_hide(self, sender):
		self.hidden = True
	
	def on_self_show(self, sender):
		self.hidden = False
		self.set_keep_above(self.app.presets.get_bool('main_keep_above', self.active_preset))
	
	def on_playlist_add_action_activate(self, sender):
		target = self.shown_track
		
		ad = AddDialog(self, self.app, target)
		
		playlist = ad.get_playlist()
		
		if playlist:
			self.playlist_add(playlist, target)
	
	def playlist_add(self, playlist, track):
		self.set_status_working(PROCESS_ADD, track)
		track.async_call(playlist.addTrack, self.playlist_add_callback, (track,))
	
	def playlist_add_callback(self, sender, output):
		
		if sender.last_error():
			if not int(sender.last_error().getID()) == int(pylast.STATUS_INVALID_PARAMS):
				self.set_status_error(PROCESS_ADD, sender)
				return
		
		self.set_status_success(PROCESS_ADD, sender)
	
	def fire_up(self):
		self.setup()
		self.show()
		self.show_track()
		self.check_authentication()
		self.reset_title()
		
		if '--hidden' in sys.argv:
			self.toggle_iconified()
	
	def apply_configs(self):
		
		#self
		self.set_opacity(self.app.presets.get_float('main_opacity', self.active_preset))
		self.set_keep_above(self.app.presets.get_bool('main_keep_above', self.active_preset))
		self.set_property('skip-taskbar-hint', self.app.presets.get_bool('main_skip_taskbar', self.active_preset))
		self.set_resizable(self.app.presets.get_bool('main_resizable', self.active_preset))
		self.set_decorated(self.app.presets.get_bool('main_decorated', self.active_preset))
		self.reset_size()
		
		#status_bar
		if self.app.presets.get_bool('main_show_statusbar', self.active_preset):
			self.status_bar.show_all()
		else:
			self.status_bar.hide()
		
		#track_box_buttons
		if self.app.presets.get_bool('main_show_buttons', self.active_preset):
			self.track_buttons_box.show()
		else:
			self.track_buttons_box.hide()
		
		#labels
		if self.app.presets.get_bool('main_show_artist', self.active_preset):
			self.artist_box.show()
		else:
			self.artist_box.hide()
		
		if self.app.presets.get_bool('main_show_title', self.active_preset):
			self.title_box.show()
		else:
			self.title_box.hide()
		
		if self.app.presets.get_bool('main_show_album', self.active_preset):
			self.album_box.show()
		else:
			self.album_box.hide()
		
		#art
		if self.app.presets.get_bool('main_show_art', self.active_preset):
			self.art_box.show()
		else:
			self.art_box.hide()
		
		#buttons
		buttons = (self.love_button, self.tag_button, self.share_button, self.playlist_add_button)
		for button in buttons:
			if self.app.presets.get_bool('main_smaller_buttons', self.active_preset):
				button.make_smaller()
			else:
				button.make_normal()
		
		#to reset the art
		self.art.set_size(self.app.presets.get_int('main_art_dimension', self.active_preset))
		self.art.reset()

	def on_edit_menu_clicked(self, sender, event):
		d = EditPresets(self, self.app, self.apply_configs, self.change_preset)
		d.show()
